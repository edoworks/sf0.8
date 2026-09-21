import unittest
from pathlib import Path


CONTINUATION = Path.home() / ".config/opencode/commands/continue-sf08.md"


class ContinuationContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not CONTINUATION.is_file():
            raise AssertionError(f"missing continuation contract: {CONTINUATION}")
        cls.text = CONTINUATION.read_text(encoding="utf-8")

    def test_blocked_substep_does_not_end_authorized_work(self):
        required = (
            "Do not stop merely because one requested step is blocked",
            "Continue with independent, authorized local implementation",
            "Before ending a turn, check for the next eligible lane",
        )
        for phrase in required:
            self.assertIn(phrase, self.text)

    def test_human_authority_boundaries_remain_explicit(self):
        for phrase in (
            "human-authority",
            "security",
            "privacy",
            "destructive",
            "external-publication/release",
            "budget",
        ):
            self.assertIn(phrase, self.text)

    def test_scope_preflight_covers_external_checkouts_and_stale_worktrees(self):
        for phrase in (
            "read-only scope preflight",
            "git worktree list --porcelain",
            "working_root",
            "source_of_truth",
            "detached or prunable worktrees",
            "Do not silently discard",
            "clean, prune, or",
            "ignore a dirty or stale path",
        ):
            self.assertIn(phrase, self.text)


if __name__ == "__main__":
    unittest.main()
