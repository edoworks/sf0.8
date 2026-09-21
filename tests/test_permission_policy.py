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
                if "edoworks/factory" in pattern and pattern.startswith("gh issue create "):
                    self.assertEqual(action, "allow", pattern)
                else:
                    self.assertEqual(action, "ask", pattern)

        for number in (52, 53, 999999):
            self.assertEqual(resolve(self.fixture["rules"], f"gh issue close --repo edoworks/sf0.8 {number}"), "ask")
            self.assertEqual(resolve(self.fixture["rules"], f"gh issue close --repo other/repo {number}"), "deny")
            self.assertEqual(resolve(self.fixture["rules"], f"gh issue close --repo edoworks/sf0.8-malicious {number}"), "deny")

    def test_pr_creation_is_repo_first_and_scoped(self):
        rules = self.fixture["rules"]
        command = "gh pr create --repo edoworks/sf0.8 --base main --head feature/test --title test --body-file pr.md"
        self.assertEqual(resolve(rules, command), "allow")
        self.assertEqual(resolve(rules, command.replace("edoworks/sf0.8", "other/repo")), "deny")
        self.assertEqual(resolve(rules, "gh pr create --title test --repo edoworks/sf0.8"), "deny")

    def test_focusgate_pr_review_path_is_repo_scoped(self):
        rules = self.fixture["rules"]
        commands = (
            "gh pr create --repo edoworks/focusgate --base main --head feature/focusgate-v0 --draft",
            "gh pr view 1 --repo edoworks/focusgate --json state",
            "gh pr checks 1 --repo edoworks/focusgate --watch",
            "gh pr ready 1 --repo edoworks/focusgate",
        )
        for command in commands:
            with self.subTest(command=command):
                self.assertEqual(resolve(rules, command), "allow")
                self.assertEqual(resolve(rules, command.replace("edoworks/focusgate", "other/focusgate")), "deny")

    def test_owner_org_integration_path_is_allowed_without_broad_push_permission(self):
        rules = self.fixture["rules"]
        feature_push = "git -c credential.helper= -c credential.helper='!gh auth git-credential' push --no-follow-tags origin HEAD:refs/heads/feature/test"
        self.assertEqual(resolve(rules, feature_push), "allow")
        self.assertEqual(resolve(rules, feature_push.replace("feature/test", "main")), "ask")
        for repository in ("edoworks/sf0.8", "edoworks/product-a", "foculoom/vorynce"):
            with self.subTest(repository=repository, order="number-first"):
                self.assertEqual(resolve(rules, f"gh pr merge 80 --repo {repository} --merge --delete-branch"), "allow")
            with self.subTest(repository=repository, order="repo-first"):
                self.assertEqual(resolve(rules, f"gh pr merge --repo {repository} 80 --merge --delete-branch"), "allow")

        for repository in ("other/repo", "edoworks-malicious/repo", "foculoom-malicious/repo"):
            with self.subTest(repository=repository):
                self.assertEqual(resolve(rules, f"gh pr merge --repo {repository} 80 --merge"), "deny")

        self.assertEqual(resolve(rules, "gh pr merge --repo edoworks/sf0.8 80 --merge --admin"), "deny")
        self.assertEqual(resolve(rules, "gh pr merge 80 --repo foculoom/vorynce --squash --admin"), "deny")

    @unittest.skipUnless(shutil.which("opencode"), "opencode is not installed")
    def test_resolved_opencode_github_rules_match_fixture(self):
        result = subprocess.run(["opencode", "debug", "config", "--pure"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        resolved = json.loads(result.stdout)["permission"]["bash"]
        def covered(pattern):
            return pattern.startswith(("gh issue", "gh api", "gh pr"))

        actual = [(pattern, action) for pattern, action in resolved.items() if covered(pattern)]
        expected = [(pattern, action) for pattern, action in self.fixture["rules"] if covered(pattern)]
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
