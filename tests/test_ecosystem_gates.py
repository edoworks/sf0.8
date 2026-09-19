import json
import subprocess
import unittest
from pathlib import Path

from scripts.ecosystem_gates import (
    contribution_gate,
    evaluate_candidate,
    required_search,
    reuse_gate,
    validate_feedback_record,
    validate_change_record,
    validate_changed_records,
    validate_discovery_evidence,
    validate_reuse_registry,
    completion_state,
)


class EcosystemGateTests(unittest.TestCase):
    def candidate(self, **overrides):
        value = {
            "id": "local-capability",
            "source": ".factory/local",
            "source_type": "FOCULOOM_SHARED",
            "artifact_type": "tool",
            "revision": "abc123",
            "license": "internal",
            "security": "reviewed",
            "disposition": "ADAPT",
            "reason": "reuse local capability",
        }
        value.update(overrides)
        return value

    def test_reuse_gate_is_proportional(self):
        self.assertEqual(required_search(1), 1)
        self.assertEqual(required_search(8), 1)
        self.assertEqual(required_search(9), 2)
        self.assertEqual(reuse_gate(9, 1, 0, "not found")["decision"], "BLOCKED")
        self.assertEqual(reuse_gate(9, 2, 1)["decision"], "REUSE")
        self.assertEqual(reuse_gate(9, 2, 0, "not compatible")["decision"], "BUILD_NEW")

    def test_reuse_gate_rejects_bad_candidate_counts(self):
        result = reuse_gate(1, 1, 2)
        self.assertEqual(result["decision"], "BLOCKED")

    def test_discovery_entrypoint_exposes_applicable_external_sources(self):
        result = subprocess.run(
            ["python3", "scripts/discover-reuse.py", "executive review", "--artifact-type", "skill"],
            cwd=Path(__file__).parents[1], capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual([item["source"] for item in payload["external_sources"]], ["GitHub agent skills", "Awesome Copilot", "skills.sh"])

    def test_contribution_classification_preserves_product_boundary(self):
        result = contribution_gate(
            product_specific=True, portable=True, dependency_free=True,
            tests=True, docs=True, provenance=True, license_checked=True,
        )
        self.assertEqual(result["classification"], "product-specific")
        self.assertEqual(result["publication"], "human-approval-required")

    def test_contribution_requires_all_publication_evidence(self):
        result = contribution_gate(
            product_specific=False, portable=True, dependency_free=True,
            tests=True, docs=True, provenance=False, license_checked=True,
        )
        self.assertEqual(result["classification"], "upstream-candidate")
        self.assertFalse(result["checks_pass"])

    def test_complete_portable_artifact_is_public_reusable_candidate(self):
        result = contribution_gate(
            product_specific=False, portable=True, dependency_free=True,
            tests=True, docs=True, provenance=True, license_checked=True,
        )
        self.assertEqual(result["classification"], "public-reusable")
        self.assertEqual(result["publication"], "human-approval-required")

    def test_upstream_improvement_is_explicit(self):
        result = contribution_gate(
            product_specific=False, portable=True, dependency_free=True,
            tests=True, docs=True, provenance=True, license_checked=True,
            upstream_useful=True,
        )
        self.assertEqual(result["classification"], "upstream-contribution")

    def test_candidate_with_compatible_license_can_be_adopted(self):
        result = evaluate_candidate({
            "relevance": "direct",
            "quality": "credible",
            "maintenance": "active",
            "license": "MIT",
            "security": "reviewed",
            "privacy": "local-only",
            "dependency_cost": "low",
            "portability": "portable",
            "overlap": "none",
            "adaptability": "cheap",
            "provenance": "tag-v1",
            "disposition": "ADAPT",
        })
        self.assertEqual(result["decision"], "ADAPT")

    def test_unknown_license_is_rejected(self):
        result = evaluate_candidate({
            "relevance": "direct",
            "quality": "credible",
            "maintenance": "active",
            "license": "unknown",
            "security": "reviewed",
            "privacy": "local-only",
            "dependency_cost": "low",
            "portability": "portable",
            "overlap": "none",
            "adaptability": "cheap",
            "provenance": "tag-v1",
            "disposition": "ADOPT",
        })
        self.assertEqual(result["decision"], "REJECT")

    def test_suspicious_artifact_is_quarantined(self):
        result = evaluate_candidate({
            "relevance": "direct",
            "quality": "credible",
            "maintenance": "active",
            "license": "MIT",
            "security": "suspicious",
            "privacy": "unknown",
            "dependency_cost": "unknown",
            "portability": "unknown",
            "overlap": "unknown",
            "adaptability": "unknown",
            "provenance": "tag-v1",
            "disposition": "ADOPT",
        })
        self.assertEqual(result["decision"], "REJECT")

    def test_feedback_is_review_input_not_execution_authority(self):
        result = validate_feedback_record({
            "artifact": "proportional-reuse-gate",
            "source": "https://example.invalid/report",
            "observed_at": "2026-09-18",
            "status": "unreviewed",
            "requested_action": "review",
        })
        self.assertEqual(result["decision"], "REVIEW_REQUIRED")

        blocked = validate_feedback_record({
            "artifact": "proportional-reuse-gate",
            "source": "https://example.invalid/report",
            "observed_at": "2026-09-18",
            "status": "accepted",
            "requested_action": "adapt",
            "applied": True,
        })
        self.assertEqual(blocked["decision"], "BLOCKED")

    def test_candidate_evaluation_requires_complete_safety_context(self):
        result = evaluate_candidate({"disposition": "ADOPT"})
        self.assertEqual(result["decision"], "REJECT")
        self.assertTrue(any("privacy" in reason for reason in result["reasons"]))

    def test_tiny_change_bypasses_heavyweight_gate(self):
        result = validate_change_record(["ProductA/Feature.swift", "docs/note.md"], None)
        self.assertEqual(result["decision"], "BYPASS")

    def test_substantial_change_requires_record(self):
        result = validate_change_record(["scripts/new-tool.py"], None)
        self.assertEqual(result["decision"], "BLOCKED")

    def test_substantial_change_accepts_valid_record(self):
        result = validate_change_record(
            [".agents/skills/example/SKILL.md"],
            {
                "change_units": 8,
                "reuse": {"searched": 1, "compatible": 0, "reason": "No compatible artifact", "discovery": {"capability": "new tool", "decision": "BUILD_NEW", "matches": [], "specialization_reason": "No compatible artifact"}, "candidates": [self.candidate(id="external", source="https://example.invalid/tool", source_type="SOURCE_REPOSITORY", disposition="REJECT")]},
                "contribution": {"classification": "internal-reusable"},
                "shareability": {"disposition": "REUSE_CANDIDATE", "evidence": "first proven implementation"},
            },
        )
        self.assertEqual(result["decision"], "PASS")

    def test_substantial_change_without_shareability_is_blocked(self):
        result = validate_change_record(
            ["scripts/new-tool.py"],
            {"change_units": 1, "reuse": {"searched": 1, "compatible": 0, "reason": "new"}, "contribution": {"classification": "product-specific"}},
        )
        self.assertEqual(result["decision"], "BLOCKED")

    def test_discovery_rejects_counts_without_candidates_and_duplicates(self):
        self.assertTrue(validate_discovery_evidence({"searched": 1, "compatible": 0, "discovery": {"decision": "BUILD_NEW"}}))
        candidate = self.candidate()
        errors = validate_discovery_evidence({"searched": 2, "compatible": 2, "discovery": {"decision": "EXTEND_EXISTING"}, "candidates": [candidate, candidate]})
        self.assertTrue(any("unique" in error for error in errors))
        self.assertTrue(any("external candidate" in error for error in errors))

    def test_adopted_external_candidate_requires_immutable_ref(self):
        reuse = {"searched": 1, "compatible": 1, "discovery": {"decision": "CONSUME_EXISTING"}, "candidates": [self.candidate(source="https://example.invalid/tool", source_type="SOURCE_REPOSITORY")]}
        self.assertTrue(any("immutable_ref" in error for error in validate_discovery_evidence(reuse)))

    def test_changed_paths_require_current_bound_ledgers(self):
        path = "scripts/new-tool.py"
        record = {
            "issue": 9,
            "capability": "new tool",
            "change_units": 1,
            "changed_paths": [path],
            "reuse": {"searched": 1, "compatible": 0, "reason": "not compatible", "discovery": {"capability": "new tool", "decision": "BUILD_NEW", "matches": [], "specialization_reason": "different contract"}, "candidates": [self.candidate(id="external", source="https://example.invalid/tool", source_type="SOURCE_REPOSITORY", disposition="REJECT")]},
            "contribution": {"classification": "internal-reusable"},
            "shareability": {"disposition": "REUSE_CANDIDATE", "evidence": "first consumer"},
        }
        bindings = {"by_capability": {"new tool": {"number": 9}}}
        self.assertEqual(validate_changed_records([path, ".factory/artifacts/ledger/issue-9.json"], [record], bindings)["decision"], "PASS")
        self.assertEqual(validate_changed_records([path], [], bindings)["decision"], "BLOCKED")

    def test_test_only_ledger_still_requires_valid_candidate_evidence(self):
        record = {
            "issue": 9,
            "capability": "test-only guard",
            "change_units": 1,
            "changed_paths": ["tests/test_guard.py"],
            "reuse": {
                "searched": 1,
                "compatible": 0,
                "reason": "platform documentation",
                "discovery": {"capability": "test-only guard", "decision": "EXTEND_EXISTING", "matches": [], "specialization_reason": "guard extension"},
                "candidates": [self.candidate(source_type="PLATFORM_BUILTIN", disposition="LEARN_ONLY")],
            },
            "contribution": {"classification": "internal-reusable"},
            "shareability": {"disposition": "REUSE_CANDIDATE", "evidence": "first consumer"},
        }
        result = validate_changed_records(
            ["tests/test_guard.py", ".factory/artifacts/ledger/issue-9.json"],
            [record],
            {"by_capability": {"test-only guard": {"number": 9}}},
        )
        self.assertEqual(result["decision"], "BLOCKED")
        self.assertTrue(any("invalid source_type" in error for error in result["errors"]))
        self.assertTrue(any("invalid disposition" in error for error in result["errors"]))

    def test_rule_of_two_and_public_safety_registry_rules(self):
        base = {
            "id": "x", "title": "x", "origin": "x", "created_by": "x", "problem": "x",
            "consumers": [], "plausible_consumers": [], "second_consumer_demonstrated": False,
            "extraction_justified": False, "equivalent_public_capability": False, "upstream_assessment": "x",
            "tests": "x", "provenance": "x", "license": "x", "secrets_private_data": False,
            "consumer_evidence": ["x"], "verification_evidence": ["x"],
            "differentiation_security": False, "lifecycle_state": "candidate", "rationale": "x",
        }
        bad = dict(base, disposition="INTERNAL_SHARED")
        self.assertTrue(validate_reuse_registry({"artifacts": [bad], "metrics": {}}))
        bad_public = dict(base, id="public", disposition="PUBLIC_CANDIDATE", secrets_private_data=True)
        self.assertTrue(validate_reuse_registry({"artifacts": [bad_public], "metrics": {}}))
        approved_public = dict(base, id="approved", disposition="PUBLIC_CANDIDATE", publication_approved=True)
        self.assertTrue(validate_reuse_registry({"artifacts": [approved_public], "metrics": {}}))

    def test_registry_catches_duplicate_and_obsolete_shared_artifacts(self):
        shared = dict({
            "id": "shared", "title": "shared", "origin": "x", "created_by": "x", "problem": "x",
            "consumers": ["a", "b"], "plausible_consumers": [], "second_consumer_demonstrated": True,
            "extraction_justified": True, "equivalent_public_capability": False, "upstream_assessment": "x",
            "tests": "x", "provenance": "x", "license": "x", "secrets_private_data": False,
            "consumer_evidence": ["x"], "verification_evidence": ["x"],
            "differentiation_security": False, "lifecycle_state": "active", "rationale": "x",
        }, disposition="INTERNAL_SHARED")
        duplicate = dict(shared, id="duplicate", disposition="REUSE_CANDIDATE", duplicate_of="missing")
        obsolete = dict(shared, id="obsolete", consumers=[], second_consumer_demonstrated=False)
        errors = validate_reuse_registry({"artifacts": [shared, duplicate, obsolete], "metrics": {}})
        self.assertTrue(any("duplicate_of" in error for error in errors))
        self.assertTrue(any("zero consumers" in error for error in errors))

    def test_upstream_candidate_requires_equivalent_public_capability(self):
        record = {
            "id": "upstream", "title": "upstream", "disposition": "UPSTREAM_CANDIDATE", "origin": "x", "created_by": "x", "problem": "x",
            "consumers": ["a"], "plausible_consumers": [], "second_consumer_demonstrated": False, "extraction_justified": True,
            "equivalent_public_capability": False, "upstream_assessment": "x", "tests": "x", "provenance": "x", "license": "x",
            "secrets_private_data": False, "differentiation_security": False, "lifecycle_state": "candidate", "rationale": "x",
            "consumer_evidence": ["x"], "verification_evidence": ["x"],
        }
        self.assertTrue(any("equivalent public" in error for error in validate_reuse_registry({"artifacts": [record], "metrics": {}})))

    def test_registry_and_dogfood_ledger_are_git_visible(self):
        root = Path(__file__).parents[1] / ".factory" / "artifacts"
        record = json.loads((root / "records" / "reuse-gate.json").read_text())
        ledger = json.loads((root / "ledger" / "product-a-candidates.json").read_text())
        registry = json.loads((root / "reuse-registry.json").read_text())
        self.assertFalse(record["publication"]["approved"])
        self.assertIn("maintenance", record)
        self.assertEqual(ledger["issue"], 31)
        self.assertEqual(validate_reuse_registry(registry), [])

    def test_versioned_package_stays_candidate_until_human_release(self):
        root = Path(__file__).parents[1]
        manifest = json.loads((root / ".factory/artifacts/packages/proportional-reuse-gate/MANIFEST.json").read_text())
        self.assertEqual(manifest["version"], "1.0.0")
        self.assertEqual(manifest["release_state"], "CANDIDATE_UNRELEASED")
        self.assertFalse(manifest["publication_approved"])

    def test_portfolio_incompleteness_is_not_done(self):
        result = completion_state({"blocker_state": "PORTFOLIO_RECONCILIATION_BLOCKED"})
        self.assertFalse(result["done"])
        self.assertEqual(result["state"], "PORTFOLIO_RECONCILIATION_BLOCKED")


if __name__ == "__main__":
    unittest.main()
