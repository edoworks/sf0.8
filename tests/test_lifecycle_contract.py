import json
import unittest
from pathlib import Path

from scripts.lifecycle_contract import deletion_errors, transition_allowed


ROOT = Path(__file__).parents[1]


class LifecycleContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = json.loads((ROOT / ".factory/lifecycle-contract.json").read_text())

    def test_safe_archive_path_is_explicit(self):
        self.assertTrue(transition_allowed(self.contract, "DORMANT", "KNOWLEDGE_EXTRACTED"))
        self.assertTrue(transition_allowed(self.contract, "KNOWLEDGE_EXTRACTED", "ARCHIVED"))
        self.assertFalse(transition_allowed(self.contract, "DORMANT", "DELETION_CANDIDATE"))

    def test_deletion_requires_all_preservation_evidence_and_authority(self):
        errors = deletion_errors(self.contract, {"state": "DELETION_CANDIDATE"})
        self.assertIn("unique_knowledge", errors)
        self.assertIn("human_authorization", errors)

    def test_human_authorized_delete_cannot_be_self_authorized(self):
        evidence = {field: True for field in self.contract["deletion_requirements"]}
        evidence.update({"state": "DELETION_CANDIDATE", "human_authorized_delete": True})
        self.assertIn("DELETION_CANDIDATE cannot self-authorize deletion", deletion_errors(self.contract, evidence))

    def test_unknown_candidate_fails_closed_and_evidence_is_boolean(self):
        evidence = {field: "yes" for field in self.contract["deletion_requirements"]}
        evidence["state"] = "UNKNOWN"
        errors = deletion_errors(self.contract, evidence)
        self.assertIn("UNKNOWN candidates cannot become deletion-eligible", errors)
        self.assertIn("unique_knowledge", errors)


if __name__ == "__main__":
    unittest.main()
