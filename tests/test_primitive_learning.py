import copy
import json
import unittest
from pathlib import Path

from scripts.primitive_discovery import apply_learning_to_opportunities, validate_learning_record
from scripts.tool_opportunities import derived_stage


ROOT = Path(__file__).parents[1]


class PrimitiveLearningTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inventory = json.loads((ROOT / ".factory/capability-primitive-inventory.json").read_text())
        cls.ledger = json.loads((ROOT / ".factory/tool-opportunity-ledger.json").read_text())

    def result(self, **overrides):
        value = {
            "result_id": "learning-1",
            "primitive_id": "primitive:rendit-deterministic-workflow",
            "opportunity_ids": ["shovel:deterministic-rendering-workflow"],
            "user": "external tester",
            "workflow": "render a social asset",
            "job_to_be_done": "repeatably produce a reviewed asset",
            "frequency": "weekly",
            "friction": "manual re-rendering",
            "combinations": [],
            "problem_observed": True,
            "usage_observed": True,
            "repeated_use": False,
            "economic_value_observed": False,
            "value_created": "UNKNOWN",
            "payment_signal": {"stage": "INTEREST"},
            "consent": {"status": "recorded"},
            "synthetic": False,
        }
        value.update(overrides)
        return value

    def test_learning_record_requires_explicit_evidence_booleans(self):
        errors = validate_learning_record(self.result())
        self.assertEqual(errors, [])
        broken = self.result(problem_observed="yes")
        self.assertTrue(any("problem_observed" in error for error in validate_learning_record(broken)))

    def test_external_problem_updates_opportunity_but_interest_does_not_update_payment(self):
        updated = apply_learning_to_opportunities(copy.deepcopy(self.ledger), self.result())
        candidate = next(item for item in updated["candidates"] if item["id"] == "shovel:deterministic-rendering-workflow")
        self.assertEqual(candidate["external_evidence"]["status"], "PRESENT")
        self.assertEqual(candidate["economic_evidence"]["status"], "UNKNOWN")
        self.assertEqual(derived_stage(candidate), "EXTERNAL_EVIDENCE")

    def test_payment_requires_strong_observed_stage(self):
        updated = apply_learning_to_opportunities(copy.deepcopy(self.ledger), self.result(payment_signal={"stage": "PURCHASE"}, economic_value_observed=True))
        candidate = next(item for item in updated["candidates"] if item["id"] == "shovel:deterministic-rendering-workflow")
        self.assertEqual(candidate["economic_evidence"]["status"], "PRESENT")
        self.assertEqual(candidate["external_evidence"]["status"], "PRESENT")

    def test_unknown_opportunity_is_rejected(self):
        with self.assertRaises(ValueError):
            apply_learning_to_opportunities(copy.deepcopy(self.ledger), self.result(opportunity_ids=["missing"]))

    def test_duplicate_learning_result_is_rejected(self):
        inventory = copy.deepcopy(self.inventory)
        inventory["capabilities"][1]["learning_records"] = ["learning-1"]
        from scripts.primitive_discovery import apply_learning
        with self.assertRaises(ValueError):
            apply_learning(inventory, self.result())


if __name__ == "__main__":
    unittest.main()
