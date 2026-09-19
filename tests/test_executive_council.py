import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("executive_council", ROOT / "scripts" / "executive_council.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class ExecutiveCouncilTests(unittest.TestCase):
    def test_first_review_has_exactly_five_lenses_and_real_counts(self):
        review = MODULE.review()
        self.assertEqual(tuple(review["lenses"]), MODULE.LENSES)
        self.assertEqual(review["evidence"]["portfolio"]["candidates"]["value"], 49)
        self.assertEqual(review["evidence"]["portfolio"]["ready_for_review"]["value"], 0)
        self.assertEqual(review["evidence"]["portfolio"]["blocked"]["value"], 1)
        self.assertEqual(review["evidence"]["portfolio"]["shelved"]["value"], 11)

    def test_unknown_financials_are_not_fabricated(self):
        economics = MODULE.review()["evidence"]["economics"]
        self.assertEqual(economics["revenue"]["value"], "UNKNOWN")
        self.assertEqual(economics["contribution_margin"]["value"], "UNKNOWN")

    def test_conflicting_lifecycle_sources_fail_closed(self):
        review = MODULE.review()
        conflicts = review["evidence"]["conflicts"]
        self.assertEqual(conflicts[0]["status"], "BLOCKED_UNRESOLVED_SOURCE_CONFLICT")
        self.assertFalse(any(item["text"].startswith("Product A lifecycle is settled") for item in review["lenses"]["CEO"]["claims"]))

    def test_validator_rejects_composite_health_score(self):
        review = MODULE.review()
        review["synthesis"]["text"] = "Company health score is 87/100"
        self.assertTrue(any("composite health" in error for error in MODULE.validate(review)))

    def test_render_is_compact_and_has_founder_boundary(self):
        rendered = MODULE.render(MODULE.review())
        self.assertIn("# FOCULOOM - DAILY EXECUTIVE REVIEW", rendered)
        self.assertIn("## HUMAN DECISIONS", rendered)
        self.assertLess(len(rendered.splitlines()), 60)


if __name__ == "__main__":
    unittest.main()
