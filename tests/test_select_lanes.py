import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
SPEC = importlib.util.spec_from_file_location("select_lanes", ROOT / "scripts/select-lanes.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class SelectLaneTests(unittest.TestCase):
    def test_ready_lane_continues_around_blocked_lane(self):
        result = MODULE.select_ready_lanes({
            "lanes": [
                {"work": "blocked release", "state": "BLOCKED_EXTERNAL", "resource": "apple", "priority": 1},
                {"work": "ready archaeology", "state": "READY", "resource": "read-only", "priority": 2},
            ]
        })
        self.assertEqual(result["selected"], ["ready archaeology"])
        self.assertEqual(result["idle_despite_ready_work"], 0)

    def test_conflicting_ready_lane_is_not_started(self):
        result = MODULE.select_ready_lanes({
            "active_resources": ["shared-artifacts"],
            "lanes": [{"work": "unsafe", "state": "READY", "resource": "shared-artifacts", "priority": 1}],
        })
        self.assertEqual(result["selected"], [])
        self.assertEqual(result["idle_despite_ready_work"], 1)

    def test_known_idle_does_not_claim_portfolio_completeness(self):
        result = MODULE.select_ready_lanes({
            "lanes": [],
            "portfolio": {
                "discovery_confidence": "INCOMPLETE",
                "unreconciled_product_candidates": 1,
            },
        })
        self.assertEqual(result["known_ready_work_idle"], 0)
        self.assertEqual(result["idle_despite_ready_work"], 0)
        self.assertFalse(result["portfolio_complete"])
        self.assertEqual(result["unreconciled_product_candidates"], 1)


if __name__ == "__main__":
    unittest.main()
