import re
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


class DeepDiveSubjectLockTests(unittest.TestCase):
    def test_command_locks_subject_and_rejects_substitution(self):
        text = (ROOT / ".opencode" / "commands" / "deepdive.md").read_text(
            encoding="utf-8"
        )
        normalized = re.sub(r"\s+", " ", text).lower()

        for phrase in (
            "$arguments",
            "authoritative research request (preserve verbatim)",
            "subject lock",
            "do not replace it with an adjacent product",
            "clarifying question",
            "subject-consistency check",
            "answer about an adjacent subject as a failed report",
        ):
            self.assertIn(phrase, normalized)

    def test_skill_applies_subject_lock_before_research(self):
        text = (
            ROOT / ".agents" / "skills" / "evidence-research" / "SKILL.md"
        ).read_text(encoding="utf-8")
        normalized = re.sub(r"\s+", " ", text).lower()

        self.assertIn("immutable subject lock", normalized)
        self.assertIn("do not substitute a nearby product", normalized)
        self.assertIn("discard and correct any adjacent-subject result", normalized)


if __name__ == "__main__":
    unittest.main()
