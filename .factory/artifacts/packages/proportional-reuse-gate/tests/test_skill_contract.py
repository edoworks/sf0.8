import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


class SkillContractTests(unittest.TestCase):
    def test_skill_has_valid_frontmatter_and_boundaries(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertRegex(skill, r"\A---\nname: proportional-reuse-gate\n")
        self.assertIn("description:", skill)
        self.assertIn("Never install, execute, publish, release, or upstream", skill)
        self.assertIn("Unknown licensing is a blocker", skill)
        self.assertRegex(skill, r"(?m)^---\n\n# Proportional Reuse Gate\n")

    def test_examples_are_complete_and_deterministic(self):
        cases = json.loads((ROOT / "examples/decision-cases.json").read_text(encoding="utf-8"))
        self.assertEqual(len(cases), 4)
        for case in cases:
            self.assertRegex(case["decision"], r"^(REUSE|BUILD_NEW|BLOCKED)$")
            self.assertIn(case["classification"], {"product-specific", "internal-reusable", "public-reusable", "upstream-candidate"})
            self.assertIsInstance(case["matches"], list)
            self.assertTrue(case["reason"].strip())


if __name__ == "__main__":
    unittest.main()
