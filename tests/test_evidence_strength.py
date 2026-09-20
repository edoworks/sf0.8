import unittest

from scripts.evidence_strength import evidence_levels, validate_levels


class EvidenceStrengthTests(unittest.TestCase):
    def test_simulated_evidence_does_not_claim_real_world_verification(self):
        levels = evidence_levels({"evidence": {"tests": True, "simulator": True}})
        self.assertEqual(levels["local_implementation"], "UNIT_TESTED")
        self.assertEqual(levels["simulator"], "SIMULATED")
        self.assertEqual(levels["real_world"], "UNVERIFIED")
        self.assertEqual(validate_levels(levels), [])
