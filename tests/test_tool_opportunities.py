import json
import unittest
from pathlib import Path

from scripts.tool_opportunities import derived_stage, validate_candidate, validate_ledger


ROOT = Path(__file__).parents[1]


class ToolOpportunityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ledger = json.loads((ROOT / ".factory/tool-opportunity-ledger.json").read_text())

    def test_initial_ledger_is_valid(self):
        self.assertEqual(validate_ledger(self.ledger), [])

    def test_internal_usage_does_not_advance_external_stage(self):
        candidate = self.ledger["candidates"][0]
        self.assertEqual(derived_stage(candidate), "REUSE")
        self.assertNotEqual(candidate["external_evidence"]["status"], "PRESENT")

    def test_repetition_must_not_remain_signal(self):
        candidate = dict(self.ledger["candidates"][0])
        candidate["frequency"] = {"count": 3, "scope": "test"}
        candidate["stage"] = "SIGNAL"
        self.assertTrue(any("advance beyond SIGNAL" in error for error in validate_candidate(candidate)))

    def test_prototype_requires_external_and_economic_evidence(self):
        candidate = dict(self.ledger["candidates"][3])
        candidate["lifecycle"] = "PROTOTYPE"
        candidate["stage"] = "PRODUCT_HYPOTHESIS"
        self.assertTrue(any("economic stages" in error for error in validate_candidate(candidate)))

    def test_duplicate_signal_reference_is_rejected(self):
        broken = json.loads(json.dumps(self.ledger))
        broken["signals"][0]["candidate_id"] = "missing"
        self.assertTrue(any("unknown candidate" in error for error in validate_ledger(broken)))
