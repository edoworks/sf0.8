import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path

from scripts.recovery import classify_blocker, recovery_decision, search_solutions, validate_solution_sources

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

VALIDATOR_SPEC = importlib.util.spec_from_file_location("validate_recovery", ROOT / "scripts/validate-recovery.py")
VALIDATOR = importlib.util.module_from_spec(VALIDATOR_SPEC)
assert VALIDATOR_SPEC and VALIDATOR_SPEC.loader
VALIDATOR_SPEC.loader.exec_module(VALIDATOR)

class RecoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = json.loads((ROOT / ".factory/recovery/solutions.json").read_text())
        cls.sources = json.loads((ROOT / ".factory/recovery/sources.json").read_text())

    def test_current_public_surface_solution_is_discovered(self):
        matches = search_solutions("public URL canonical routing live HTTP check", self.registry, self.sources, objective_id="current_rung_incident")
        self.assertEqual(matches[0]["id"], "sf08-public-surface-preflight")
        self.assertEqual(matches[0]["compatibility"], "directly_compatible")

    def test_sibling_pr_solution_is_discovered_semantically(self):
        matches = search_solutions("create GitHub pull request after direct branch push", self.registry, self.sources, objective_id="current_rung_incident")
        self.assertEqual(matches[0]["id"], "foculoom-reviewed-pr-workflow")
        self.assertIn("pull_request", matches[0]["matched_terms"])

    def test_proven_compatible_solution_outranks_unknown_candidate(self):
        registry = copy.deepcopy(self.registry)
        speculative = copy.deepcopy(registry["solutions"][0])
        speculative["id"] = "speculative-pr-builder"
        speculative["disposition"] = "BUILD_NEW"
        speculative["authority_state"] = "UNKNOWN"
        speculative["compatibility"]["current_rung_incident"] = "unknown"
        registry["solutions"].append(speculative)
        matches = search_solutions("GitHub pull request branch policy", registry, self.sources, objective_id="current_rung_incident")
        self.assertEqual(matches[0]["id"], "foculoom-reviewed-pr-workflow")

    def test_untrusted_source_is_rejected(self):
        solution = copy.deepcopy(self.registry["solutions"][0])
        solution["implementation_location"] = "/Users/hello/factory-secrets/hidden.sh"
        self.assertTrue(validate_solution_sources(solution, self.sources))

    def test_unauthorized_candidate_escalates_without_execution(self):
        matches = search_solutions("create GitHub pull request after direct branch push", self.registry, self.sources, objective_id="current_rung_incident")
        result = recovery_decision(
            blocker={"class": "governance_restriction"},
            candidates=matches,
            attempts=0,
        )
        self.assertEqual(result["state"], "HUMAN_AUTHORIZATION_REQUIRED")

    def test_failed_attempt_is_bounded(self):
        result = recovery_decision(
            blocker={"class": "governance_restriction"},
            candidates=[{"id": "candidate", "authority_state": "AVAILABLE", "human_authorization_required": False}],
            attempts=3,
            max_attempts=3,
        )
        self.assertEqual(result["state"], "BLOCKED_AFTER_SELF_UNBLOCKING")

    def test_blocker_classification_distinguishes_policy_and_service(self):
        self.assertEqual(classify_blocker(error="pre-push hook direct push prohibited", operation="git push"), "governance_restriction")
        self.assertEqual(classify_blocker(error="HTTP 530", operation="live URL"), "transient_infrastructure_problem")

    def test_registry_does_not_expose_credentials(self):
        serialized = json.dumps(self.registry).casefold()
        self.assertNotIn("ghp_", serialized)
        self.assertNotIn("ntfy", serialized)

    def test_checked_in_registry_validates(self):
        self.assertEqual(VALIDATOR.validate(self.registry, self.sources), [])
