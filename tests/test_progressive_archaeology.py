import unittest

from scripts.progressive_archaeology import classify, triage


class ProgressiveArchaeologyTests(unittest.TestCase):
    def test_metadata_triage_deduplicates_and_caps_deep_analysis(self):
        candidates = [
            {"product_id": "released", "bundle_ids": ["com.example.released"], "distribution_states": ["Ready for Sale"]},
            {"product_id": "released-copy", "bundle_ids": ["com.example.released"], "distribution_states": ["Ready for Sale"]},
            *({"product_id": f"unknown-{index}"} for index in range(135)),
        ]
        result = triage(candidates, max_deep_candidates=4)
        self.assertEqual(result["candidate_count"], 137)
        self.assertLessEqual(result["selected_deep_count"], 4)
        self.assertTrue(any(row["classification"] == "DUPLICATE" for row in result["rows"]))
        self.assertTrue(all(not row["deletion_eligible"] for row in result["rows"]))
        self.assertTrue(all(row["classification"] == "UNKNOWN" or row["deep_analysis_selected"] for row in result["rows"] if row["deep_analysis_eligible"]))

    def test_classification_uses_release_and_rejection_metadata(self):
        self.assertEqual(classify({"distribution_states": ["Ready for Sale"]}), "RELEASED PRODUCT")
        self.assertEqual(classify({"distribution_states": ["Developer Rejected"]}), "REJECTED SUBMISSION")
        self.assertEqual(classify({"product_id": "prototype-experiment"}), "MEANINGFUL EXPERIMENT")


if __name__ == "__main__":
    unittest.main()
