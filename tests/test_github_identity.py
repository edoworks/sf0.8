import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validate_github_identity", ROOT / "scripts/validate-github-identity.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class GithubIdentityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.policy = json.loads(
            (ROOT / ".factory/github-identity-policy.json").read_text()
        )

    def test_suffix_matching_is_case_insensitive(self):
        self.assertTrue(MODULE.allowed_login("helloFOCULOOM", self.policy))

    def test_non_matching_login_is_rejected(self):
        self.assertFalse(MODULE.allowed_login("octocat", self.policy))
        self.assertFalse(MODULE.allowed_login("foculoomish", self.policy))
        self.assertFalse(MODULE.allowed_login(None, self.policy))

    def test_snapshot_rejects_any_unauthorized_action_actor(self):
        snapshot = {
            "organization": "edoworks",
            "members": ["hellofoculoom"],
            "collaborators": ["hellofoculoom"],
            "reviewers": ["external-user"],
            "bypass_actors": ["hellofoculoom"],
        }
        errors = MODULE.snapshot_errors(snapshot, self.policy)
        self.assertEqual(errors, ["unauthorized login in reviewers: 'external-user'"])

    def test_snapshot_rejects_reviewer_as_bypass_actor(self):
        snapshot = {
            "organization": "foculoom",
            "members": ["hellofoculoom", "supportfoculoom"],
            "collaborators": ["hellofoculoom", "supportfoculoom"],
            "reviewers": ["supportfoculoom"],
            "bypass_actors": ["hellofoculoom", "supportfoculoom"],
        }
        errors = MODULE.snapshot_errors(snapshot, self.policy)
        self.assertEqual(
            errors,
            ["bypass_actors must exactly match exclusive_bypass_actors"],
        )


if __name__ == "__main__":
    unittest.main()
