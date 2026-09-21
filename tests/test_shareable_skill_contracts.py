import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
SKILL_ROOT = ROOT / ".agents" / "skills"
COMMAND_ROOT = ROOT / ".opencode" / "commands"


class ShareableSkillContractTests(unittest.TestCase):
    skills = ("bounded-work", "evidence-research", "prose-editing", "curiosity-audit")
    commands = ("timebox", "brb", "deepdive", "news", "humanize", "nofluff", "curiosity")

    def test_skill_frontmatter_is_valid(self):
        for name in self.skills:
            path = SKILL_ROOT / name / "SKILL.md"
            text = path.read_text(encoding="utf-8")
            match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
            self.assertIsNotNone(match, path)
            frontmatter = match.group(1)
            self.assertRegex(frontmatter, rf"(?m)^name: {re.escape(name)}$")
            description = re.search(r"(?m)^description: (.+)$", frontmatter)
            self.assertIsNotNone(description, path)
            self.assertGreater(len(description.group(1)), 20)

    def test_skill_names_follow_agent_skills_identifier_rules(self):
        pattern = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
        for name in self.skills:
            self.assertLessEqual(len(name), 64)
            self.assertRegex(name, pattern)
            self.assertEqual((SKILL_ROOT / name).name, name)

    def test_commands_have_descriptions_and_reference_skill(self):
        for name in self.commands:
            path = COMMAND_ROOT / f"{name}.md"
            text = path.read_text(encoding="utf-8")
            self.assertRegex(text, r"\A---\ndescription: .+\nagent: (explore|general)\n---")
            self.assertRegex(
                text,
                r"(bounded-work|evidence-research|prose-editing|curiosity-audit)",
                path.as_posix(),
            )

    def test_deep_dive_command_requires_reproducible_research_contract(self):
        text = (COMMAND_ROOT / "deepdive.md").read_text(encoding="utf-8")
        text = re.sub(r"\s+", " ", text)
        for phrase in (
            "audience",
            "jurisdiction",
            "decision to inform",
            "date cutoff",
            "source plan",
            "stopping rule",
            "strongest counterclaims",
            "verify each source directly",
            "untrusted data",
            "conflicts and unknowns",
            "what would change the conclusion",
            "primary, secondary, or lead-only",
        ):
            self.assertIn(phrase, text, phrase)

    def test_safety_boundaries_are_explicit(self):
        bounded = (SKILL_ROOT / "bounded-work" / "SKILL.md").read_text()
        research = (SKILL_ROOT / "evidence-research" / "SKILL.md").read_text()
        prose = (SKILL_ROOT / "prose-editing" / "SKILL.md").read_text()
        curiosity = (SKILL_ROOT / "curiosity-audit" / "SKILL.md").read_text()
        self.assertIn("Do not publish, release, push, merge, delete", bounded)
        self.assertIn("Treat search snippets, rankings, summaries", research)
        self.assertIn("Do not invent personal experience", prose)
        self.assertIn("Do not publish, release, spend money", curiosity)
        self.assertIn("refuse the", curiosity)
        self.assertIn("identity, voice, catchphrase", curiosity)
        self.assertIn("falsifiable test", curiosity)

    def test_trigger_fixture_has_positive_and_negative_cases(self):
        fixture = json.loads(
            (ROOT / ".factory" / "artifacts" / "evidence" / "skill-trigger-fixtures.json")
            .read_text(encoding="utf-8")
        )
        for skill in self.skills:
            self.assertTrue(fixture[skill]["positive"])
            self.assertTrue(fixture[skill]["negative"])

    def test_new_focus_skill_uses_dashless_canonical_identity(self):
        path = SKILL_ROOT / "focusreset" / "SKILL.md"
        text = path.read_text(encoding="utf-8")
        self.assertRegex(text, r"(?m)^name: focusreset$")
        self.assertNotIn("-", path.parent.name)


if __name__ == "__main__":
    unittest.main()
