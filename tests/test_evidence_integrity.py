import importlib.util
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("evidence_integrity", ROOT / "scripts/evidence_integrity.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)
ENTRY_SPEC = importlib.util.spec_from_file_location(
    "validate_evidence_integrity", ROOT / "scripts/validate-evidence-integrity.py"
)
ENTRY = importlib.util.module_from_spec(ENTRY_SPEC)
assert ENTRY_SPEC.loader is not None
ENTRY_SPEC.loader.exec_module(ENTRY)


def timeout_receipt(**overrides):
    receipt = {
        "outcome": "COMMAND_TIMEOUT_PROGRESSING",
        "current_test": "test_a",
        "result_bundle_path": "artifacts/result.xcresult",
        "started_at": "2026-09-22T10:00:00Z",
        "last_progress_at": "2026-09-22T10:01:00Z",
        "ended_at": "2026-09-22T10:02:00Z",
        "inactivity_threshold_seconds": 30,
        "completed_count": 2,
        "progress_events": [{"at": "2026-09-22T10:01:00Z", "test": "test_a"}],
        "exit_status": None,
    }
    receipt.update(overrides)
    return receipt


class EvidenceIntegrityTests(unittest.TestCase):
    def test_progressing_timeout_is_not_a_failure_or_hang(self):
        self.assertEqual([], MODULE.validate_timeout_receipt(timeout_receipt()))

    def test_no_progress_timeout_requires_threshold_evidence(self):
        receipt = timeout_receipt(
            outcome="COMMAND_TIMEOUT_NO_PROGRESS",
            last_progress_at="2026-09-22T10:00:00Z",
            completed_count=0,
            progress_events=[],
        )
        self.assertEqual([], MODULE.validate_timeout_receipt(receipt))
        receipt["ended_at"] = "2026-09-22T10:00:10Z"
        self.assertTrue(any("inactivity threshold" in error for error in MODULE.validate_timeout_receipt(receipt)))

    def test_confirmed_hang_requires_two_stable_process_samples(self):
        receipt = timeout_receipt(
            outcome="TEST_HANG_CONFIRMED",
            last_progress_at="2026-09-22T10:00:00Z",
            completed_count=0,
            progress_events=[],
            process_samples=[
                {"at": "2026-09-22T10:00:00Z", "active_test": "test_a", "output_progress": False, "result_bundle_progress": False},
                {"at": "2026-09-22T10:00:30Z", "active_test": "test_a", "output_progress": False, "result_bundle_progress": False},
            ],
        )
        self.assertEqual([], MODULE.validate_timeout_receipt(receipt))

    def test_untracked_evidence_is_rejected(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            evidence = root / "receipt.json"
            evidence.write_text("{}")
            errors = MODULE.validate_evidence_references(
                [{"path": "receipt.json", "revision": "HEAD"}], root, []
            )
            self.assertTrue(any("not tracked" in error for error in errors))

    def test_evidence_revision_must_be_exact_or_current(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            evidence = root / "receipt.json"
            evidence.write_text("{}")
            errors = MODULE.validate_evidence_references(
                [{"path": "receipt.json", "revision": "working-tree"}], root, ["receipt.json"]
            )
            self.assertTrue(any("full commit id" in error for error in errors))

    def test_evidence_must_exist_at_cited_revision(self):
        errors = ENTRY.evidence_at_revision(
            ROOT, [{"path": "missing-evidence.json", "revision": "HEAD"}]
        )
        self.assertTrue(any("absent at revision" in error for error in errors))

    def test_continuation_drift_is_rejected(self):
        state = {
            "status": "IN_PROGRESS",
            "active_map_issue": 42,
            "active_increment_issue": 47,
            "source_of_truth": ".factory/continuation-state.json",
        }
        errors = MODULE.validate_continuation_state(state, "Canonical status: `IN_PROGRESS`\nCanonical active map issue: `#42`\n")
        self.assertTrue(any("active increment issue" in error for error in errors))

    def test_wrong_ledger_weekday_is_rejected(self):
        ledger = {
            "ledger_version": "1.0.0",
            "started": "2026-09-22",
            "target": {"weekday_changes": 10, "unattended_success_rate": 0.95, "failure_taxonomy": True},
            "daily_receipts": [{
                "date": "2026-09-22",
                "weekday": "Monday",
                "change_description": "change",
                "unattended_success": True,
                "manual_repair_required": False,
                "failure_classification": None,
                "operator_identity": "operator-a",
                "denominator": 1,
                "cumulative_success_rate": 1.0,
            }],
        }
        self.assertTrue(any("weekday" in error for error in MODULE.validate_qualification_ledger(ledger)))

    def test_stale_remote_snapshot_is_rejected(self):
        snapshot = {
            "schema_version": 1,
            "captured_at": "2026-09-20T00:00:00Z",
            "max_age_hours": 24,
            "issues": [{"repo": "edoworks/factory", "number": 49, "state": "OPEN"}],
        }
        gates = {
            "49": {
                "repo": "edoworks/factory", "number": 49, "remote_state": "OPEN",
                "evidence_state": "INCOMPLETE", "effective_state": "OPEN",
            }
        }
        errors = MODULE.validate_remote_snapshot(
            snapshot, gates, now=datetime(2026, 9, 23, tzinfo=timezone.utc)
        )
        self.assertIn("remote snapshot is stale", errors)

    def test_invalid_closed_gate_is_blocked(self):
        snapshot = {
            "schema_version": 1,
            "captured_at": "2026-09-23T00:00:00Z",
            "max_age_hours": 24,
            "issues": [{"repo": "edoworks/factory", "number": 16, "state": "CLOSED"}],
        }
        gates = {
            "16": {
                "repo": "edoworks/factory", "number": 16, "remote_state": "CLOSED",
                "evidence_state": "INVALID", "effective_state": "CLOSED",
            }
        }
        errors = MODULE.validate_remote_snapshot(
            snapshot, gates, now=datetime(2026, 9, 23, 1, tzinfo=timezone.utc)
        )
        self.assertTrue(any("must be BLOCKED" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
