import copy
import json
import unittest
from pathlib import Path

from scripts.primitive_discovery import (
    apply_learning,
    classify,
    validate_learning_record,
    validate_inventory,
    validate_record,
)


ROOT = Path(__file__).parents[1]


class PrimitiveDiscoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inventory = json.loads((ROOT / ".factory/capability-primitive-inventory.json").read_text())

    def test_inventory_is_valid(self):
        self.assertEqual(validate_inventory(self.inventory), [])

    def test_internal_usage_does_not_become_external_demand(self):
        record = next(item for item in self.inventory["capabilities"] if item["id"] == "primitive:ci-status-evidence")
        self.assertEqual(record["evidence"]["usage"]["status"], "PRESENT")
        self.assertEqual(record["evidence"]["problem"]["status"], "UNKNOWN")
        self.assertEqual(classify(record), "INSUFFICIENT_EVIDENCE")

    def test_problem_evidence_does_not_become_payment_evidence(self):
        record = copy.deepcopy(next(item for item in self.inventory["capabilities"] if item["id"] == "primitive:rendit-deterministic-workflow"))
        self.assertEqual(classify(record), "DEVELOPER_PRIMITIVE")
        self.assertEqual(record["evidence"]["payment"]["status"], "UNKNOWN")
        record["evidence"]["usage"]["status"] = "UNKNOWN"
        self.assertEqual(classify(record), "INSUFFICIENT_EVIDENCE")

    def test_sensitive_capability_cannot_be_authorized_by_inventory(self):
        record = copy.deepcopy(next(item for item in self.inventory["capabilities"] if item["id"] == "primitive:ecosystem-validators"))
        record["externalization"]["status"] = "HUMAN_AUTHORIZED"
        self.assertTrue(any("cannot be authorized" in error for error in validate_record(record)))

    def test_learning_updates_only_observed_levels(self):
        result = {
            "result_id": "observation-1",
            "primitive_id": "primitive:rendit-deterministic-workflow",
            "user": "external tester",
            "workflow": "render a social asset",
            "job_to_be_done": "repeatably produce a reviewed asset",
            "frequency": "weekly",
            "friction": "manual re-rendering",
            "combinations": [],
            "problem_observed": True,
            "usage_observed": True,
            "repeated_use": True,
            "economic_value_observed": False,
            "value_created": "time saved UNKNOWN",
            "payment_signal": {"stage": "INTEREST"},
            "consent": {"status": "recorded"},
            "synthetic": False,
        }
        updated = apply_learning(self.inventory, result)
        record = next(item for item in updated["capabilities"] if item["id"] == result["primitive_id"])
        self.assertEqual(record["evidence"]["usage"]["status"], "PRESENT")
        self.assertEqual(record["evidence"]["retention"]["status"], "PRESENT")
        self.assertEqual(record["evidence"]["payment"]["status"], "ABSENT")

    def test_synthetic_learning_is_rejected(self):
        errors = validate_learning_record({"synthetic": True})
        self.assertIn("synthetic learning cannot update external evidence", errors)


if __name__ == "__main__":
    unittest.main()
