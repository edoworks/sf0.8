import fnmatch
import json
from pathlib import Path
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


if __name__ == "__main__":
    unittest.main()
