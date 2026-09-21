import copy
import json
import unittest
from pathlib import Path

from scripts.primitive_discovery import apply_reach_signal, validate_reach_signal


ROOT = Path(__file__).parents[1]


class PrimitiveReachTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inventory = json.loads((ROOT / ".factory/capability-primitive-inventory.json").read_text())

    def signal(self, **overrides):
        value = {
            "signal_id": "reach-1",
            "primitive_id": "primitive:reusefirst",
            "signal_type": "DOWNLOAD",
            "observed_at": "2026-09-20T00:00:00Z",
            "artifact_revision": "reusefirst/v1.2.1",
            "source": "owner-provided-release-record",
            "audience": "UNKNOWN",
            "consent": {"status": "NOT_APPLICABLE"},
            "verified_execution": False,
            "workflow": "UNKNOWN",
            "job_to_be_done": "UNKNOWN",
        }
        value.update(overrides)
        return value

    def test_download_is_reach_only(self):
        updated = apply_reach_signal(copy.deepcopy(self.inventory), self.signal())
        record = next(item for item in updated["capabilities"] if item["id"] == "primitive:reusefirst")
        self.assertEqual(len(updated["reach_signals"]), 1)
        self.assertEqual(record["evidence"]["usage"]["status"], "PRESENT")
        self.assertEqual(record["external_usage_evidence"], [])

    def test_verified_non_founder_execution_records_external_use(self):
        signal = self.signal(
            signal_id="use-1",
            signal_type="VERIFIED_EXECUTION",
            source="consented-workflow-report",
            audience="NON_FOUNDER",
            consent={"status": "OPT_IN"},
            verified_execution=True,
            workflow="artifact review",
            job_to_be_done="check a proposed reuse decision",
        )
        updated = apply_reach_signal(copy.deepcopy(self.inventory), signal)
        record = next(item for item in updated["capabilities"] if item["id"] == "primitive:reusefirst")
        self.assertEqual(record["external_usage_evidence"], ["use-1"])

    def test_download_cannot_claim_execution(self):
        errors = validate_reach_signal(self.signal(verified_execution=True))
        self.assertTrue(any("cannot claim verified execution" in error for error in errors))

    def test_founder_execution_is_not_external_use(self):
        errors = validate_reach_signal(self.signal(
            signal_type="VERIFIED_EXECUTION",
            audience="FOUNDER",
            consent={"status": "OPT_IN"},
            verified_execution=True,
            workflow="artifact review",
            job_to_be_done="check a proposed reuse decision",
        ))
        self.assertTrue(any("non-founder" in error for error in errors))

    def test_duplicate_reach_signal_is_rejected(self):
        inventory = apply_reach_signal(copy.deepcopy(self.inventory), self.signal())
        with self.assertRaises(ValueError):
            apply_reach_signal(inventory, self.signal())


if __name__ == "__main__":
    unittest.main()
