import json
import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


def load_validator():
    path = ROOT / "scripts/validate-education-evidence.py"
    spec = importlib.util.spec_from_file_location("validate_education_evidence", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class EducationEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record = json.loads((ROOT / ".factory/artifacts/evidence/education-opportunity-discovery.json").read_text())
        cls.validator = load_validator()

    def test_current_concepts_are_not_validated(self):
        self.assertEqual({item["state"] for item in self.record["hypotheses"]}, {"HYPOTHESIS", "PARKED"})
        self.assertEqual(self.validator.validate(self.record), [])

    def test_missing_competitive_substitution_is_rejected(self):
        broken = json.loads(json.dumps(self.record))
        del broken["hypotheses"][0]["substitution"]["current_workaround"]
        self.assertTrue(any("current_workaround" in error for error in self.validator.validate(broken)))

    def test_learning_and_monetization_contract_is_explicit(self):
        contract = self.record["experiment_contract"]
        self.assertIn("NOVEL_TRANSFER_TASK", contract["learning_gate"])
        self.assertIn("48_HOUR_RETEST", contract["learning_gate"])
        self.assertTrue(contract["no_subscription_default"])
        self.assertTrue(contract["behavior_change_evidence"])

    def test_frontier_rejects_synthetic_results(self):
        result = {
            "result_id": "r1", "hypothesis_id": "proof-tiles", "experiment_id": "E1-proof-tiles",
            "participant_source": "INTERNAL_REASONING", "synthetic": True, "observations": ["imagined"],
            "behavior_change": {}, "learning_evidence": {}, "payment_signal": {"stage": "INTEREST"}, "consent": {},
        }
        errors = self.validator.validate_frontier(result) if hasattr(self.validator, "validate_frontier") else []
        self.assertTrue(errors)


if __name__ == "__main__":
    unittest.main()
