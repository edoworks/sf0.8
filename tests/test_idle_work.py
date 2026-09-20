import json
import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]

from scripts.idle_work import discover_idle_work, select_work, validate_waiting_report

VALIDATOR_SPEC = importlib.util.spec_from_file_location("validate_idle_work", ROOT / "scripts/validate-idle-work.py")
VALIDATOR = importlib.util.module_from_spec(VALIDATOR_SPEC)
assert VALIDATOR_SPEC.loader is not None
VALIDATOR_SPEC.loader.exec_module(VALIDATOR)


class IdleWorkTests(unittest.TestCase):
    def test_product_a_blocked_does_not_hide_safe_factory_work(self):
        report = discover_idle_work(ROOT)
        self.assertEqual(report["status"], "READY_WORK_FOUND")
        self.assertTrue(any(item["category"] in {"portfolio", "hygiene", "validation"} for item in report["eligible_candidates"]))

    def test_human_decision_and_reuse_candidate_are_classified_separately(self):
        report = discover_idle_work(ROOT)
        self.assertTrue(any(item["id"].startswith("reuse:") for item in report["candidates_found"]))
        blocked = [item for item in report["candidates_rejected_or_blocked"] if item["candidate"].startswith("reuse:")]
        self.assertTrue(blocked)

    def test_provider_failure_cannot_claim_exhaustion(self):
        report = discover_idle_work(ROOT, providers={"lanes": lambda _: (_ for _ in ()).throw(RuntimeError("offline"))})
        self.assertEqual(report["status"], "READY_WORK_FOUND")
        self.assertFalse(report["waiting_dependency_legal"])
        self.assertTrue(any(item["status"] == "ERROR" for item in report["provider_results"]))
        report["status"] = "WAITING_DEPENDENCY"
        self.assertTrue(validate_waiting_report(report))

    def test_waiting_requires_zero_eligible_candidates(self):
        report = discover_idle_work(ROOT)
        report["status"] = "WAITING_DEPENDENCY"
        report["waiting_dependency_legal"] = True
        self.assertTrue(validate_waiting_report(report))

    def test_only_irreversible_or_human_work_can_wait(self):
        empty = lambda _: []
        report = discover_idle_work(ROOT, providers={"portfolio": empty, "lanes": empty, "reuse": empty, "hygiene": empty, "knowledge": empty, "rejections": empty, "verification": empty, "ci": empty})
        self.assertEqual(report["status"], "WAITING_DEPENDENCY")
        self.assertEqual(validate_waiting_report(report), [])

    def test_cost_ceiling_is_explicit_and_can_legally_wait(self):
        expensive = lambda _: [{
            "id": "expensive", "title": "expensive", "category": "factory",
            "source": "fixture", "priority": 1, "value": "HIGH", "urgency": "HIGH",
            "reversibility": "HIGH", "risk": "LOW", "cost": 6.0,
            "required_authority": "NONE", "dependencies": [], "scope": "bounded",
            "evidence": ["fixture"], "expected_validation": ["fixture"], "state": "READY",
        }]
        empty = lambda _: []
        report = discover_idle_work(ROOT, budget=5.0, providers={"portfolio": empty, "lanes": empty, "reuse": empty, "hygiene": empty, "knowledge": empty, "rejections": empty, "verification": expensive, "ci": empty})
        self.assertEqual(report["status"], "WAITING_DEPENDENCY")
        self.assertTrue(any("cost budget" in item["reason"] for item in report["candidates_rejected_or_blocked"]))

    def test_irreversible_work_is_not_eligible(self):
        destructive = lambda _: [{
            "id": "delete", "title": "delete", "category": "hygiene",
            "source": "fixture", "priority": 1, "value": "HIGH", "urgency": "HIGH",
            "reversibility": "LOW", "risk": "HIGH", "cost": 0.0,
            "required_authority": "HUMAN", "dependencies": [], "scope": "delete",
            "evidence": ["fixture"], "expected_validation": ["fixture"], "state": "READY",
        }]
        empty = lambda _: []
        report = discover_idle_work(ROOT, providers={"portfolio": empty, "lanes": empty, "reuse": empty, "hygiene": destructive, "knowledge": empty, "rejections": empty, "verification": empty, "ci": empty})
        self.assertEqual(report["status"], "WAITING_DEPENDENCY")
        self.assertTrue(report["waiting_dependency_legal"])

    def test_selected_work_is_deterministic_and_bounded(self):
        first = select_work(discover_idle_work(ROOT))
        second = select_work(discover_idle_work(ROOT))
        self.assertEqual(first["id"], second["id"])
        self.assertTrue(first["scope"])
        self.assertTrue(first["expected_validation"])

    def test_manifest_loads_extensible_provider_functions(self):
        report = discover_idle_work(ROOT)
        sources = set(report["sources_searched"])
        self.assertTrue({"portfolio", "knowledge", "rejections", "ci"}.issubset(sources))
        self.assertTrue(any(item["id"] == "rejections:historical-comparison" for item in report["candidates_found"]))

    def test_report_validator_accepts_dogfood_evidence(self):
        report = json.loads((ROOT / ".factory/artifacts/evidence/idle-work-dogfood.json").read_text())
        self.assertEqual(VALIDATOR.validate_report(report), [])

    def test_dependency_change_deterministically_resumes_work(self):
        blocked = lambda _: [{
            "id": "dependency", "title": "dependency", "category": "factory",
            "source": "fixture", "priority": 1, "value": "HIGH", "urgency": "HIGH",
            "reversibility": "HIGH", "risk": "LOW", "cost": 0.0,
            "required_authority": "NONE", "dependencies": ["pending"], "scope": "bounded",
            "evidence": ["fixture"], "expected_validation": ["fixture"], "state": "READY",
        }]
        empty = lambda _: []
        providers = {"portfolio": empty, "lanes": empty, "reuse": empty, "hygiene": blocked, "knowledge": empty, "rejections": empty, "verification": empty, "ci": empty}
        self.assertEqual(discover_idle_work(ROOT, providers=providers)["status"], "WAITING_DEPENDENCY")
        providers["hygiene"] = lambda _: [dict(blocked(None)[0], dependencies=[])]
        resumed = discover_idle_work(ROOT, providers=providers)
        self.assertEqual(resumed["status"], "READY_WORK_FOUND")
        self.assertEqual(select_work(resumed)["id"], "dependency")

    def test_serialized_report_keeps_restart_selection(self):
        report = discover_idle_work(ROOT)
        restored = json.loads(json.dumps(report))
        self.assertEqual(select_work(report)["id"], select_work(restored)["id"])


if __name__ == "__main__":
    unittest.main()
