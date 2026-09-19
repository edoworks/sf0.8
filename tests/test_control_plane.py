import importlib.util
import json
import subprocess
import unittest
from pathlib import Path
from unittest.mock import Mock

from scripts.ecosystem_gates import (
    completion_state,
    discover_registry,
    validate_change_record,
    validate_consumer_evidence,
    validate_reuse_registry,
    validate_work_start,
)
from scripts.control_plane import capability_preflight

ROOT = Path(__file__).parents[1]


def load_review_module():
    spec = importlib.util.spec_from_file_location("review_contract", ROOT / "scripts/validate-review-contract.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ControlPlaneTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = json.loads((ROOT / ".factory/artifacts/reuse-registry.json").read_text())

    def test_cold_agent_discovers_before_apple_build(self):
        task = ROOT / ".factory/artifacts/evidence/cold-agent/apple-preflight-task.json"
        result = subprocess.run(["python3", "scripts/start-work.py", str(task)], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["decision"], "CONSUME_EXISTING")
        self.assertIn("apple-distribution-preflight", payload["matches"])

    def test_material_entrypoint_blocks_before_reuse_when_issue_is_unbound(self):
        task = ROOT / ".factory/artifacts/evidence/cold-agent/material-without-issue.json"
        result = subprocess.run(["python3", "scripts/start-work.py", str(task)], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["decision"], "BLOCKED")
        self.assertEqual(payload["control_plane"]["stage"], "issue_requirement")

    def test_material_work_fails_before_reuse_when_issue_write_is_denied(self):
        runner = Mock(side_effect=[
            subprocess.CompletedProcess([], 0, "hellofoculoom\n", ""),
            subprocess.CompletedProcess([], 1, "", "permission denied"),
        ])
        result = capability_preflight(
            {"material": True, "change_units": 4},
            repo="edoworks/sf0.8",
            issue={"number": 50, "url": "https://github.com/edoworks/sf0.8/issues/50", "repo": "edoworks/sf0.8", "canonical": True, "created_or_reused": True, "write_probe": "probe"},
            runner=runner,
        )
        self.assertEqual(result["decision"], "BLOCKED")
        self.assertEqual(result["stage"], "write_capability")
        self.assertEqual(runner.call_count, 2)

    def test_identity_is_not_write_readiness(self):
        runner = Mock(side_effect=[
            subprocess.CompletedProcess([], 0, "hellofoculoom\n", ""),
            subprocess.CompletedProcess([], 1, "", "permission denied"),
        ])
        result = capability_preflight(
            {"material": True},
            repo="edoworks/sf0.8",
            issue={"number": 50, "url": "https://github.com/edoworks/sf0.8/issues/50", "repo": "edoworks/sf0.8", "canonical": True, "created_or_reused": True, "write_probe": "probe"},
            runner=runner,
        )
        self.assertEqual(result["stage"], "write_capability")

    def test_successful_preflight_binds_material_work(self):
        runner = Mock(side_effect=[
            subprocess.CompletedProcess([], 0, "hellofoculoom\n", ""),
            subprocess.CompletedProcess([], 0, "https://github.com/edoworks/sf0.8/issues/50#comment\n", ""),
        ])
        result = capability_preflight(
            {"material": True},
            repo="edoworks/sf0.8",
            issue={"number": 50, "url": "https://github.com/edoworks/sf0.8/issues/50", "repo": "edoworks/sf0.8", "canonical": True, "created_or_reused": True, "write_probe": "probe"},
            runner=runner,
        )
        self.assertEqual(result["decision"], "PASS")
        self.assertEqual(result["binding"]["issue_number"], 50)

    def test_unrelated_issue_is_rejected_before_write(self):
        runner = Mock()
        result = capability_preflight(
            {"material": True}, repo="edoworks/sf0.8",
            issue={"number": 49, "url": "https://github.com/edoworks/sf0.8/issues/49", "repo": "edoworks/sf0.8", "canonical": True, "created_or_reused": True, "write_probe": "probe"},
            expected_issue={"number": 50, "url": "https://github.com/edoworks/sf0.8/issues/50"}, runner=runner,
        )
        self.assertEqual(result["decision"], "BLOCKED")
        self.assertEqual(result["stage"], "binding")
        runner.assert_not_called()

    def test_identity_without_canonical_marker_is_not_binding(self):
        runner = Mock(side_effect=[subprocess.CompletedProcess([], 0, "hellofoculoom\n", "")])
        result = capability_preflight(
            {"material": True}, repo="edoworks/sf0.8",
            issue={"number": 50, "url": "https://github.com/edoworks/sf0.8/issues/50", "repo": "edoworks/sf0.8", "created_or_reused": True, "write_probe": "probe"}, runner=runner,
        )
        self.assertEqual(result["stage"], "binding")
        self.assertEqual(runner.call_count, 0)

    def test_deliberate_duplicate_is_blocked_at_work_start(self):
        result = validate_work_start({"capability": "Apple distribution preflight", "change_units": 12, "decision": "BUILD_NEW"}, self.registry)
        self.assertEqual(result["decision"], "BLOCKED")
        self.assertTrue(any("existing capability" in error for error in result["errors"]))

    def test_missing_and_fabricated_completion_disposition_is_blocked(self):
        missing = validate_change_record(["scripts/new-tool.py"], {"change_units": 1, "reuse": {"searched": 1, "compatible": 0, "reason": "new"}, "contribution": {"classification": "product-specific"}})
        fabricated = validate_change_record(["scripts/new-tool.py"], {"change_units": 1, "reuse": {"searched": 1, "compatible": 0, "reason": "new"}, "contribution": {"classification": "product-specific"}, "shareability": {"disposition": "PRODUCT_ONLY", "evidence": ""}})
        self.assertEqual(missing["decision"], "BLOCKED")
        self.assertEqual(fabricated["decision"], "BLOCKED")

    def test_registry_rejects_missing_schema_and_stale_consumer_evidence(self):
        broken = json.loads(json.dumps(self.registry))
        del broken["artifacts"][0]["verification_evidence"]
        self.assertTrue(any("verification_evidence" in error for error in validate_reuse_registry(broken)))
        stale = json.loads(json.dumps(self.registry))
        stale["artifacts"][0]["consumer_evidence"] = ["scripts/no-longer-here.py"]
        self.assertTrue(any("does not exist" in error for error in validate_consumer_evidence(stale, ROOT)))

    def test_rule_of_two_public_safety_duplicate_and_zero_consumer_guards(self):
        internal = self.registry["artifacts"][1]
        one_consumer = json.loads(json.dumps(internal))
        one_consumer["consumers"] = ["one"]
        one_consumer["consumer_evidence"] = ["scripts/validate-apple-distribution.py"]
        self.assertTrue(validate_reuse_registry({"artifacts": [one_consumer], "metrics": {}}))
        zero = json.loads(json.dumps(internal))
        zero["consumers"] = []
        self.assertTrue(any("zero consumers" in error for error in validate_reuse_registry({"artifacts": [zero], "metrics": {}})))
        public = json.loads(json.dumps(self.registry["artifacts"][0]))
        public["secrets_private_data"] = True
        self.assertTrue(any("private/security" in error for error in validate_reuse_registry({"artifacts": [public], "metrics": {}})))

    def test_upstream_and_product_only_cannot_bypass_analysis(self):
        upstream = json.loads(json.dumps(self.registry["artifacts"][0]))
        upstream["id"] = "upstream"
        upstream["disposition"] = "UPSTREAM_CANDIDATE"
        upstream["equivalent_public_capability"] = True
        upstream.pop("external_capability_evidence", None)
        self.assertTrue(any("external capability evidence" in error for error in validate_reuse_registry({"artifacts": [upstream], "metrics": {}})))
        product_only = validate_change_record(["scripts/new-tool.py"], {"change_units": 1, "reuse": {"searched": 1, "compatible": 0, "reason": "new"}, "contribution": {"classification": "product-specific"}, "shareability": {"disposition": "PRODUCT_ONLY", "evidence": "product-specific"}})
        self.assertTrue(any("reuse analysis" in error for error in product_only["errors"]))

    def test_historical_candidates_are_not_disposable_and_knowledge_has_provenance(self):
        manifests = json.loads((ROOT / ".factory/artifacts/portfolio-archaeology/preservation-manifests.json").read_text())["manifests"]
        self.assertTrue(manifests)
        self.assertTrue(all(item["deletion_authorized"] is False for item in manifests))
        knowledge = json.loads((ROOT / ".factory/artifacts/portfolio-archaeology/knowledge-records.json").read_text())["records"]
        self.assertTrue(all(item.get("source") for item in knowledge))

    def test_portfolio_reconciliation_distinguishes_absence_from_deletion(self):
        record = json.loads((ROOT / ".factory/artifacts/portfolio-archaeology/portfolio-reconciliation.json").read_text())
        statuses = {item["id"]: item["status"] for item in record["entries"]}
        self.assertEqual(statuses["edoworks/trycycle"], "NOT_LOCALLY_OBSERVED")
        self.assertIn("Rung", " ".join(record["urgent_findings_preserved"]))

    def test_review_requires_aggressive_implementation_handoff(self):
        module = load_review_module()
        complete = json.loads((ROOT / ".factory/artifacts/evidence/review-contract/complete.json").read_text())
        self.assertEqual([], module.validate_review(complete))
        incomplete = dict(complete)
        del incomplete["implementation_prompt"]
        self.assertTrue(any("implementation_prompt" in error for error in module.validate_review(incomplete)))

    def test_blocked_issue_reconciliation_prevents_done_and_resume_is_deterministic(self):
        blocked = json.loads((ROOT / ".factory/artifacts/evidence/control-plane/issue-49-reconciliation.json").read_text())
        blocked["issue"]["reconciled"] = False
        blocked["issue"]["remote_state"] = "open"
        blocked["state"] = "CONTROL_PLANE_BLOCKED"
        blocked["done"] = False
        blocked["control_plane_blocker"] = "fixture permission denial"
        state = completion_state(blocked)
        self.assertEqual(state["state"], "CONTROL_PLANE_BLOCKED")
        self.assertFalse(state["done"])
        resumed = json.loads(json.dumps(blocked))
        resumed["issue"]["reconciled"] = True
        self.assertEqual(completion_state(resumed)["state"], "DONE")
        self.assertEqual(resumed["idempotency_key"], blocked["idempotency_key"])

    def test_explicit_blocker_states_can_never_be_done(self):
        for blocker in ("BLOCKED_EXTERNAL", "BLOCKED_HUMAN", "BLOCKED_SECURITY", "WAITING_DEPENDENCY", "FAILED"):
            state = completion_state({"implementation": "complete", "blocker_state": blocker})
            self.assertEqual(state["state"], blocker)
            self.assertFalse(state["done"])

    def test_waiting_dependency_requires_machine_exhaustion_evidence(self):
        missing = completion_state({"blocker_state": "WAITING_DEPENDENCY"})
        self.assertFalse(missing["done"])
        self.assertTrue(missing["errors"])
        exhausted = completion_state({
            "blocker_state": "WAITING_DEPENDENCY",
            "idle_exhaustion": {
                "provider_results": [{"status": "PASS"}],
                "eligible_count": 0,
                "waiting_dependency_legal": True,
            },
        })
        self.assertEqual(exhausted["errors"], [])

    def test_waiting_dependency_fails_closed_when_provider_failed(self):
        result = completion_state({
            "blocker_state": "WAITING_DEPENDENCY",
            "idle_exhaustion": {
                "provider_results": [{"status": "ERROR"}],
                "eligible_count": 0,
                "waiting_dependency_legal": False,
            },
        })
        self.assertTrue(result["errors"])

    def test_ci_cannot_skip_core_validators(self):
        workflow = (ROOT / ".github/workflows/checks.yml").read_text()
        for command in ("validate-ecosystem.py", "validate-reuse-registry.py", "validate-apple-distribution.py", "validate-control-plane.py", "validate-review-contract.py", "test_*.py"):
            self.assertIn(command, workflow)


if __name__ == "__main__":
    unittest.main()
