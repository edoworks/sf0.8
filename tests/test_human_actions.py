import json
import unittest
from pathlib import Path

from scripts.human_actions import attention_order, ordered_actions, validate_queue


ROOT = Path(__file__).parents[1]


class HumanActionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.queue = json.loads((ROOT / ".factory/human-action-queue.json").read_text())

    def test_canonical_queue_is_structured_and_valid(self):
        self.assertEqual(validate_queue(self.queue), [])
        self.assertTrue(self.queue["no_aggregate_score"])

    def test_order_keeps_dimensions_explicit(self):
        ordered = ordered_actions(self.queue)
        self.assertEqual(ordered[0]["id"], "education-e1-proof-tiles")
        self.assertNotEqual(attention_order(ordered[0]), attention_order(ordered[-1]))
        self.assertNotIn("score", ordered[0])


if __name__ == "__main__":
    unittest.main()
