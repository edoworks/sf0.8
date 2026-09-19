import fnmatch
import json
from pathlib import Path
import re
import shutil
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]


def resolve(rules, command):
    decision = "ask"
    for pattern, action in rules:
        if fnmatch.fnmatchcase(command, pattern):
            decision = action
    return decision


class PermissionPolicyFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fixture_path = ROOT / "tests" / "permission_policy_fixture.json"
        cls.fixture = json.loads(fixture_path.read_text())

    def test_expected_commands_resolve_to_their_boundary(self):
        rules = self.fixture["rules"]
        for expected, commands in self.fixture["expectations"].items():
            for command in commands:
                with self.subTest(expected=expected, command=command):
                    self.assertEqual(resolve(rules, command), expected)

    def test_compound_command_does_not_inherit_an_allow_rule(self):
        rules = self.fixture["rules"]
        for separator in (";", "&&", "||", "|"):
            command = f"git status {separator} git push --force origin main"
            with self.subTest(separator=separator):
                self.assertEqual(resolve(rules, command), "deny")

    def test_issue_mutations_are_repo_scoped_asks_without_issue_literals(self):
        issue_rules = [(pattern, action) for pattern, action in self.fixture["rules"] if pattern.startswith("gh issue")]
        for pattern, action in issue_rules:
            without_repo = pattern.replace("edoworks/sf0.8", "")
            self.assertIsNone(re.search(r"\b\d+\b", without_repo), pattern)
            if pattern.startswith(("gh issue create ", "gh issue comment ", "gh issue close ")):
                self.assertEqual(action, "ask", pattern)

        for number in (52, 53, 999999):
            self.assertEqual(resolve(self.fixture["rules"], f"gh issue close --repo edoworks/sf0.8 {number}"), "ask")
            self.assertEqual(resolve(self.fixture["rules"], f"gh issue close --repo other/repo {number}"), "deny")
            self.assertEqual(resolve(self.fixture["rules"], f"gh issue close --repo edoworks/sf0.8-malicious {number}"), "deny")

    @unittest.skipUnless(shutil.which("opencode"), "opencode is not installed")
    def test_resolved_opencode_issue_rules_match_fixture(self):
        result = subprocess.run(["opencode", "debug", "config", "--pure"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        resolved = json.loads(result.stdout)["permission"]["bash"]
        actual = [(pattern, action) for pattern, action in resolved.items() if pattern.startswith(("gh issue", "gh api"))]
        expected = [(pattern, action) for pattern, action in self.fixture["rules"] if pattern.startswith(("gh issue", "gh api"))]
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
