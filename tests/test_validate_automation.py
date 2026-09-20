import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validate_automation", ROOT / "scripts/validate-automation.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class AutomationContractTests(unittest.TestCase):
    def test_checked_in_contract_is_valid(self):
        criteria = MODULE.json.loads((ROOT / ".factory/automation/release-criteria.json").read_text())
        bundle = MODULE.json.loads((ROOT / ".factory/automation/evidence-bundle.json").read_text())
        errors, manifests = MODULE.load_sources(criteria)
        self.assertEqual([], errors)
        self.assertEqual([], MODULE.validate_bundle(bundle, criteria))
        self.assertGreater(len(manifests), 1)
        self.assertEqual(0, MODULE.summarize(manifests)["UNJUSTIFIED_MANUAL"])
        customer_zero = MODULE.json.loads((ROOT / ".factory/customer-zero.json").read_text())
        self.assertEqual([], MODULE.validate_customer_zero(customer_zero, manifests))

    def test_escape_requires_physical_reason_and_evidence(self):
        criterion = {
            "schema_version": 2,
            "criteria": [{
                "id": "haptic", "source": "AC-1", "requirement": "haptic", "classification": "DEVICE",
                "production_blocker": False, "claim": "haptic", "evidence": []
            }],
        }
        errors = MODULE.validate_criteria(criterion)
        self.assertTrue(any("why_automation_is_insufficient" in error for error in errors))

    def test_automated_criterion_is_machine_verifiable_by_default(self):
        criterion = {
            "schema_version": 2,
            "criteria": [{
                "id": "migration", "source": "REQ-014", "requirement": "migration", "classification": "AUTOMATED",
                "production_blocker": True, "claim": "migration", "evidence": []
            }],
        }
        self.assertEqual([], MODULE.validate_criteria(criterion))


if __name__ == "__main__":
    unittest.main()
