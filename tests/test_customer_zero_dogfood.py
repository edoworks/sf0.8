import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


class CustomerZeroDogfoodTests(unittest.TestCase):
    def test_dogfood_evidence_is_pinned_and_verified(self):
        evidence = json.loads(
            (ROOT / ".factory/artifacts/evidence/reusefirst-customer-zero-dogfood.json").read_text()
        )
        self.assertEqual(evidence["status"], "VERIFIED")
        self.assertEqual(evidence["revision"], "30e588b4dc0d869da9b58a01d91c22d6f4931361")
        self.assertEqual(
            {item["consumer"] for item in evidence["consumers"]},
            {"factory", "product-a", "vorynce", "intent-compiler-modeled"},
        )
        self.assertEqual(evidence["negative_case"]["decision"], "BLOCKED")

if __name__ == "__main__":
    unittest.main()
