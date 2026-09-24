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
        repo_names = ("edoworks/sf0.8", "edoworks/factory", "edoworks/product-a", "edoworks/sf0.7", "edoworks/sf0.5", "edoworks/nownest")
        for pattern, action in issue_rules:
            without_repo = pattern
            for repo in repo_names:
                without_repo = without_repo.replace(repo, "")
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

    def test_metadata_reconciliation_writes_are_narrow_asks(self):
        rules = self.fixture["rules"]
        asks = (
            'gh repo edit edoworks/rung --homepage "https://edoworks.com/rung/"',
            'gh repo edit edoworks/asc-client --description "Deprecated standalone source: use the versioned asc artifact in edoworks/artifacts."',
            'gh repo edit edoworks/factory-constitution --description "Deprecated standalone source: use the versioned constitution artifact in edoworks/artifacts."',
            'gh pr create --repo edoworks/asc-client --base main --head feature/metadata-reconciliation-52 --title "docs: reconcile deprecated asc source metadata (#52)" --body-file .factory/issue-comments/issue-52-asc-pr.md',
            'gh pr create --repo edoworks/factory-constitution --base main --head feature/metadata-reconciliation-52 --title "docs: reconcile deprecated constitution source metadata (#52)" --body-file .factory/issue-comments/issue-52-constitution-pr.md',
        )
        for command in asks:
            with self.subTest(command=command):
                self.assertEqual(resolve(rules, command), "ask")

        denied = (
            "gh repo edit edoworks/rung --description unexpected",
            "gh repo edit edoworks/asc-client --homepage https://example.com",
            "gh repo edit edoworks/factory-constitution --visibility private",
            'gh repo edit edoworks/rung --homepage "https://edoworks.com/rung/" --visibility private',
            'gh pr create --repo edoworks/asc-client --base main --head feature/metadata-reconciliation-52 --title "docs: reconcile deprecated asc source metadata (#52)" --body-file .factory/issue-comments/issue-52-asc-pr.md --repo other/repo',
            'gh pr create --repo edoworks/asc-client-malicious --base main --head feature/metadata-reconciliation-52 --title "docs: reconcile deprecated asc source metadata (#52)" --body-file .factory/issue-comments/issue-52-asc-pr.md',
        )
        for command in denied:
            with self.subTest(command=command):
                self.assertEqual(resolve(rules, command), "deny")

        allowed_reads = (
            "gh pr view 1 --repo edoworks/asc-client --json number,state,mergeable,reviewDecision,headRefOid,baseRefOid,url,mergedAt,mergeCommit",
            "gh pr checks 1 --repo edoworks/asc-client --watch",
            "gh pr view 1 --repo edoworks/factory-constitution --json number,state,mergeable,reviewDecision,headRefOid,baseRefOid,url,mergedAt,mergeCommit",
            "gh pr checks 1 --repo edoworks/factory-constitution --watch",
        )
        for command in allowed_reads:
            with self.subTest(command=command):
                self.assertEqual(resolve(rules, command), "allow")

    def test_nownest_pr_review_path_is_repo_scoped(self):
        rules = self.fixture["rules"]
        commands = (
            "gh pr create --repo edoworks/nownest --base main --head feature/nownest-v0 --draft",
            "gh pr view 1 --repo edoworks/nownest --json state",
            "gh pr checks 1 --repo edoworks/nownest --watch",
            "gh pr ready 1 --repo edoworks/nownest",
        )
        for command in commands:
            with self.subTest(command=command):
                self.assertEqual(resolve(rules, command), "allow")
                self.assertEqual(resolve(rules, command.replace("edoworks/nownest", "other/nownest")), "deny")

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
        checked_in = json.loads((ROOT / ".opencode-config" / "opencode.jsonc").read_text())["permission"]["bash"]
        def covered(pattern):
            return pattern.startswith(("gh issue", "gh api", "gh pr", "gh repo"))

        actual = [(pattern, action) for pattern, action in resolved.items() if covered(pattern)]
        expected = [(pattern, action) for pattern, action in self.fixture["rules"] if covered(pattern)]
        self.assertEqual(actual, expected)
        relevant = lambda pattern: any(
            repository in pattern
            for repository in ("edoworks/rung", "edoworks/asc-client", "edoworks/factory-constitution")
        )
        source = [(pattern, action) for pattern, action in checked_in.items() if relevant(pattern)]
        expected_source = [(pattern, action) for pattern, action in self.fixture["rules"] if relevant(pattern)]
        self.assertEqual(source, expected_source)


if __name__ == "__main__":
    unittest.main()
