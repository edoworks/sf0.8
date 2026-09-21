import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


class PublicationStateReconciliationTests(unittest.TestCase):
    def test_reusefirst_records_reconciled_release_after_dogfood(self):
        record = json.loads((ROOT / ".factory/artifacts/publication-state-reconciliation.json").read_text())["records"][0]
        self.assertEqual(record["artifact"], "reusefirst")
        self.assertEqual(record["status"], "RECONCILED")
        self.assertTrue(record["factory_publication_approved"])
        self.assertEqual(record["factory_authorization"], "OWNER_APPROVED")


if __name__ == "__main__":
    unittest.main()
