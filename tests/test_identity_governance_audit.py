import json
from pathlib import Path
import re
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / ".factory/artifacts/evidence/identity-governance"
sys.path.insert(0, str(ROOT / "scripts"))
import identity_governance_report
import public_identity
from human_actions import ordered_actions, validate_queue


class IdentityGovernanceAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = json.loads((ROOT / ".factory/identity-registry.json").read_text())
        cls.matrix = json.loads((EVIDENCE / "final-matrix.json").read_text())
        cls.queue = json.loads((ROOT / ".factory/human-action-queue.json").read_text())

    def test_matrix_is_deterministic_and_covers_registry(self):
        self.assertEqual(identity_governance_report.build_matrix(self.registry), self.matrix)
        ids = {row["id"] for row in self.matrix["rows"]}
        expected = {self.registry["legal_entity"]["entity_id"]}
        expected |= {item["entity_id"] for item in self.registry["identities"]}
        expected |= {item["entity_id"] for item in self.registry["domains"]}
        self.assertEqual(expected, ids)
        self.assertEqual(len(self.registry["domains"]), sum(row["kind"] == "DOMAIN" for row in self.matrix["rows"]))
        required = {"display_name", "role", "lifecycle", "trademark_state", "domain", "release_blocker", "required_action"}
        self.assertTrue(all(required <= set(row) for row in self.matrix["rows"]))

    def test_required_human_actions_exist_without_displacing_first_action(self):
        expected = {
            "identity-ca-sos-verification", "identity-beverly-hills-disposition",
            "identity-dba-fbn-review", "identity-uspto-foculoom-review",
            "identity-uspto-skiplet-review", "identity-uspto-veilsort-review",
            "identity-edoworks-clearance", "identity-vorynce-name-review",
            "identity-docketloom-name-review", "identity-rung-name-review",
            "identity-private-address-remediation", "identity-product-public-state-reconciliation",
        }
        self.assertEqual([], validate_queue(self.queue))
        self.assertTrue(expected <= {item["id"] for item in self.queue["actions"]})
        self.assertEqual("education-e1-proof-tiles", ordered_actions(self.queue)[0]["id"])

    def test_scanner_report_is_sanitized(self):
        report = json.loads((EVIDENCE / "scanner-report.json").read_text())
        self.assertEqual("BLOCKED", report["status"])
        self.assertGreater(report["blocker_count"], 0)
        allowed = {"code", "severity", "classification", "path", "line", "identity", "redacted_identifier"}
        self.assertTrue(all(set(item) == allowed for item in report["findings"]))
        self.assertTrue(all(not Path(item["path"]).is_absolute() for item in report["findings"]))

    def test_structured_observations_are_scanner_compatible(self):
        observations = json.loads((EVIDENCE / "observations.json").read_text())
        fixture = ROOT / "tests/fixtures/public-identity/pass/public.md"
        report = public_identity.scan([fixture], self.registry, observations=observations, mode="audit")
        self.assertEqual("BLOCKED", report["status"])
        self.assertIn("PRIVATE_ADDRESS_PATTERN", {item["code"] for item in report["findings"]})

    def test_address_evidence_stores_paths_only(self):
        record = json.loads((EVIDENCE / "address-exposure-paths.json").read_text())
        self.assertEqual("PROHIBITED", record["value_storage"])
        self.assertTrue(all(set(item) == {"source", "path", "finding_count"} for item in record["current_worktree_paths"]))
        self.assertEqual(6, len(record["stale_reference_review_paths"]))

    def test_product_surface_audit_covers_required_products(self):
        inventory = json.loads((EVIDENCE / "source-inventory.json").read_text())
        source_ids = {item["id"] for item in inventory["sources"]}
        self.assertTrue({
            "veilsort-app-site", "skiplet-app-site", "docketloom-app-site",
            "vorynce-app-site", "nownest-source", "rung-source-site",
        } <= source_ids)
        report = (ROOT / "docs/identity-governance-audit-2026-09-23.md").read_text()
        for name in ("Veilsort", "Skiplet", "Docketloom", "Vorynce", "NowNest", "Rung"):
            self.assertIn(name, report)

    def test_audit_artifacts_contain_no_sensitive_values_or_unsupported_legal_conclusions(self):
        json_paths = list(EVIDENCE.glob("*.json"))
        for path in json_paths:
            json.loads(path.read_text())
        paths = json_paths + [ROOT / "docs/identity-governance-audit-2026-09-23.md"]
        text = "\n".join(path.read_text() for path in paths)
        self.assertNotIn("/Users/", text)
        self.assertNotRegex(text, re.compile(r"\b\d{1,6}\s+[A-Za-z0-9][A-Za-z0-9 .'-]{1,48}\s(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr|Court|Ct|Way)\b", re.IGNORECASE))
        self.assertNotRegex(text, re.compile(r"(?<!\w)(?:\+?1[ .-]?)?\(?\d{3}\)?[ .-]\d{3}[ .-]\d{4}(?!\w)"))
        for phrase in ("legally cleared", "registration confirmed", "safe to use", "no infringement", "valid trademark registration"):
            self.assertNotIn(phrase, text.casefold())

    def test_root_cause_records_name_mechanical_guards(self):
        for name in ("address-propagation-5whys.json", "public-state-drift-5whys.json", "release-gate-fail-open-5whys.json"):
            record = json.loads((EVIDENCE / name).read_text())
            self.assertTrue(record["stop_reason"])
            self.assertIn("scanner", record["recurrence_guard"].casefold())


if __name__ == "__main__":
    unittest.main()
