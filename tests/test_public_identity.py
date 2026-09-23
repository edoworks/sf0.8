import copy
from datetime import date
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import public_identity as MODULE


class PublicIdentityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = json.loads((ROOT / ".factory/identity-registry.json").read_text())

    def scan_text(self, text, patterns=None, mode="release", observations=None, overrides=None):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "surface.md").write_text(text)
            return MODULE.scan([root], self.registry, patterns or [], observations, overrides, mode, today=date(2026, 9, 23))

    def test_passing_fixture(self):
        root = ROOT / "tests/fixtures/public-identity/pass"
        observations = json.loads((root / "observations.json").read_text())
        report = MODULE.scan([root / "public.md"], self.registry, observations=observations, mode="release")
        self.assertEqual("PASS", report["status"])

    def test_unregistered_mark_cannot_use_registered_symbol(self):
        report = self.scan_text("FOCULOOM\u00ae software")
        self.assertIn("UNAUTHORIZED_REGISTERED_SYMBOL", {item["code"] for item in report["findings"]})

    def test_application_cannot_be_called_registration(self):
        report = self.scan_text("FOCULOOM is a registered trademark.")
        self.assertIn("APPLICATION_DESCRIBED_AS_REGISTERED", {item["code"] for item in report["findings"]})

    def test_negative_registration_search_claim_is_not_a_registration_claim(self):
        report = self.scan_text("No registered trademark found for NowNest.")
        self.assertNotIn("APPLICATION_DESCRIBED_AS_REGISTERED", {item["code"] for item in report["findings"]})

    def test_negative_claim_for_one_mark_does_not_suppress_another_mark(self):
        report = self.scan_text("FOCULOOM is not a registered trademark; SKIPLET is a registered trademark.")
        findings = [item for item in report["findings"] if item["code"] == "APPLICATION_DESCRIBED_AS_REGISTERED"]
        self.assertTrue(any(item["identity"] == "trademark:99731845" for item in findings))

    def test_canonical_name_registered_symbol_covers_unfiled_identity(self):
        report = self.scan_text("EDOWORKS\u00ae")
        self.assertIn("UNAUTHORIZED_REGISTERED_SYMBOL", {item["code"] for item in report["findings"]})

    def test_textual_trademark_state_claim_is_checked(self):
        report = self.scan_text("SKIPLET trademark status: REGISTERED")
        self.assertIn("TRADEMARK_STATE_CLAIM", {item["code"] for item in report["findings"]})

    def test_private_pattern_is_blocked_and_never_emitted(self):
        secret = "123 Private Example Road"
        report = self.scan_text(f"Mail: {secret}", [secret])
        encoded = json.dumps(report)
        self.assertIn("PRIVATE_ADDRESS_PATTERN", encoded)
        self.assertNotIn(secret, encoded)

    def test_likely_public_street_address_is_blocked_without_approval(self):
        report = self.scan_text("Visit 500 Market Street for help.")
        self.assertIn("PUBLIC_STREET_ADDRESS_UNAPPROVED", {item["code"] for item in report["findings"]})

    def test_owner_and_seller_conflicts_are_hard_blockers(self):
        observations = {"surfaces": [{"identity": "product:nownest", "owner": "Other Corp", "seller": "Different Corp"}]}
        report = self.scan_text("", observations=observations)
        self.assertTrue({"OWNER_CONFLICT", "SELLER_CONFLICT"} <= {item["code"] for item in report["findings"]})

    def test_registered_agent_is_not_an_approved_owner_or_seller(self):
        agent = self.registry["legal_entity"]["registered_agent_name"]
        observations = {"surfaces": [{"identity": "product:nownest", "owner": agent, "seller": agent}]}
        report = self.scan_text("", observations=observations)
        self.assertTrue({"OWNER_CONFLICT", "SELLER_CONFLICT"} <= {item["code"] for item in report["findings"]})

    def test_applicant_owner_is_not_globally_approved_for_products(self):
        applicant = next(item["owner_name"] for item in self.registry["trademarks"] if item["mark"] == "FOCULOOM")
        report = self.scan_text(f"NowNest owner: {applicant}")
        self.assertIn("OWNER_CONFLICT", {item["code"] for item in report["findings"]})

    def test_noncanonical_contact_is_warning_not_pass(self):
        report = self.scan_text("Email other@example.com or call 415-555-1212.")
        self.assertEqual("WARN", report["status"])
        self.assertEqual(0, report["blocker_count"])

    def test_structured_disagreements_are_detected(self):
        observations = {"comparisons": [
            {"identity": "product:nownest", "field": field, "expected": "canonical", "observed": "different"}
            for field in ("lifecycle", "pricing", "platform", "features", "privacy", "function")
        ]}
        report = self.scan_text("", observations=observations)
        codes = {item["code"] for item in report["findings"]}
        self.assertEqual({f"{field.upper()}_CONTRADICTION" for field in ("lifecycle", "pricing", "platform", "features", "privacy", "function")}, codes)

    def test_hard_blocker_override_is_rejected(self):
        override = {"id": "o1", "code": "OWNER_CONFLICT", "authorization_reference": "decision-1", "rationale": "test", "expires_on": "2026-10-01", "scope": "*"}
        report = self.scan_text("owner: Other Corp", overrides=[override])
        self.assertEqual("REJECTED_HARD_BLOCKER", report["override_audit"][0]["status"])
        self.assertEqual("BLOCKED", report["status"])

    def test_expired_and_unknown_overrides_are_rejected(self):
        overrides = [
            {"id": "expired", "code": "NONCANONICAL_PUBLIC_EMAIL", "authorization_reference": "decision-1", "rationale": "test", "expires_on": "2026-09-22", "scope": "*"},
            {"id": "unknown", "code": "MADE_UP", "authorization_reference": "decision-2", "rationale": "test", "expires_on": "2026-10-01", "scope": "*"},
        ]
        report = self.scan_text("other@example.com", overrides=overrides)
        statuses = {item["status"] for item in report["override_audit"]}
        self.assertEqual({"REJECTED_EXPIRED", "REJECTED_UNKNOWN_CODE"}, statuses)

    def test_eligible_override_is_audited_and_applied(self):
        override = {"id": "o1", "code": "NONCANONICAL_PUBLIC_EMAIL", "authorization_reference": "decision-1", "rationale": "approved campaign alias", "expires_on": "2026-10-01", "scope": "release"}
        report = self.scan_text("other@example.com", overrides=[override])
        self.assertEqual("PASS", report["status"])
        self.assertEqual("APPLIED", report["override_audit"][0]["status"])

    def test_output_contract_contains_no_snippets_or_absolute_roots(self):
        report = self.scan_text("FOCULOOM\u00ae secret surrounding words")
        finding = report["findings"][0]
        self.assertEqual({"code", "severity", "classification", "path", "line", "identity", "redacted_identifier"}, set(finding))
        self.assertFalse(Path(finding["path"]).is_absolute())
        self.assertNotIn("surrounding", json.dumps(report))

    def test_structured_observation_cannot_emit_absolute_path_or_unknown_identity(self):
        observations = {"comparisons": [{
            "path": "/private/example/surface.json", "identity": "private-person-name",
            "field": "privacy", "expected": "a", "observed": "b",
        }]}
        report = self.scan_text("", observations=observations)
        finding = report["findings"][0]
        self.assertEqual("surface.json", finding["path"])
        self.assertEqual("UNKNOWN", finding["identity"])

    def test_release_cli_exits_nonzero_for_blocker(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "surface.md"
            path.write_text("FOCULOOM\u00ae")
            result = subprocess.run(
                [sys.executable, "scripts/validate-public-identity.py", "--mode", "release", str(path)],
                cwd=ROOT, capture_output=True, text=True,
            )
        self.assertEqual(1, result.returncode)
        self.assertNotIn(str(path.parent), result.stdout)

    def test_release_cli_exits_nonzero_for_warning(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "surface.md"
            path.write_text("Contact other@example.com")
            result = subprocess.run(
                [sys.executable, "scripts/validate-public-identity.py", "--mode", "release", str(path)],
                cwd=ROOT, capture_output=True, text=True,
            )
        self.assertEqual(1, result.returncode)

    def test_checked_in_stale_address_fixture_blocks_release(self):
        fixture = ROOT / "tests/fixtures/public-identity/fail"
        result = subprocess.run(
            [sys.executable, "scripts/validate-public-identity.py", "--mode", "release", "--private-pattern-file", str(fixture / "private-patterns.txt"), str(fixture / "stale-address.md")],
            cwd=ROOT, capture_output=True, text=True,
        )
        self.assertEqual(1, result.returncode)
        self.assertIn("PRIVATE_ADDRESS_PATTERN", result.stdout)
        self.assertNotIn("987 Fixture Residence Road", result.stdout)

    def test_checked_in_false_registered_symbol_fixture_blocks_release(self):
        fixture = ROOT / "tests/fixtures/public-identity/fail/false-registered-symbol.md"
        result = subprocess.run(
            [sys.executable, "scripts/validate-public-identity.py", "--mode", "release", str(fixture)],
            cwd=ROOT, capture_output=True, text=True,
        )
        self.assertEqual(1, result.returncode)
        self.assertIn("UNAUTHORIZED_REGISTERED_SYMBOL", result.stdout)

    def test_checked_in_owner_conflict_fixture_blocks_release(self):
        fixture = ROOT / "tests/fixtures/public-identity/fail"
        result = subprocess.run(
            [sys.executable, "scripts/validate-public-identity.py", "--mode", "release", "--observations", str(fixture / "owner-conflict.json"), str(fixture / "owner-conflict.md")],
            cwd=ROOT, capture_output=True, text=True,
        )
        self.assertEqual(1, result.returncode)
        self.assertIn("OWNER_CONFLICT", result.stdout)
        self.assertIn("SELLER_CONFLICT", result.stdout)


if __name__ == "__main__":
    unittest.main()
