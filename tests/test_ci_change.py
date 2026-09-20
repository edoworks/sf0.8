import importlib.util
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest


ROOT = Path(__file__).resolve().parents[1]


def load_module():
    sys.path.insert(0, str(ROOT / "scripts"))
    spec = importlib.util.spec_from_file_location("validate_ci_change", ROOT / "scripts/validate-ci-change.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CIChangeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module()

    def setUp(self):
        self.temp = TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / ".factory/artifacts/ledger").mkdir(parents=True)
        bindings = {"by_capability": {"event range": {"number": 55}}}
        (self.root / ".factory/control-plane-bindings.json").write_text(json.dumps(bindings))

    def tearDown(self):
        self.temp.cleanup()

    def record(self, paths):
        return {
            "issue": 55,
            "capability": "event range",
            "change_units": 2,
            "changed_paths": paths,
            "reuse": {
                "searched": 1,
                "compatible": 0,
                "reason": "Extend the existing changed-path gate.",
                "discovery": {
                    "capability": "event range",
                    "decision": "EXTEND_EXISTING",
                    "matches": ["changed-path gate"],
                    "specialization_reason": "Select the complete event range.",
                },
                "candidates": [{
                    "id": "git-diff",
                    "source": "https://git-scm.com/docs/git-diff",
                    "source_type": "FIRST_PARTY",
                    "artifact_type": "documentation",
                    "revision": "retrieved-2026-09-19",
                    "license": "documentation terms",
                    "security": "documentation only",
                    "disposition": "LEARN_FROM",
                    "reason": "Use two-dot and three-dot range semantics.",
                }],
            },
            "contribution": {"classification": "internal-reusable"},
            "shareability": {"disposition": "REUSE_CANDIDATE", "evidence": "First consumer is sf0.8 CI."},
        }

    def runner(self, expected_range, paths):
        def run(command, **kwargs):
            self.assertEqual(command, ["git", "diff", "--name-only", "-z", expected_range])
            return subprocess.CompletedProcess(command, 0, b"\0".join(path.encode() for path in paths) + b"\0", b"")
        return run

    def test_pull_request_covers_paths_from_merge_base_not_only_last_commit(self):
        base, head = "a" * 40, "b" * 40
        paths = ["scripts/earlier-commit.py", ".factory/artifacts/ledger/issue-55.json"]
        (self.root / paths[1]).write_text(json.dumps(self.record([paths[0]])))
        result = self.module.validate_event_change(
            event_name="pull_request", before="", base=base, head=head,
            root=self.root, runner=self.runner(f"{base}...{head}", paths),
        )
        self.assertEqual(result["decision"], "PASS")
        self.assertEqual(result["gated_paths"], ["scripts/earlier-commit.py"])

    def test_push_uses_complete_before_after_range(self):
        before, head = "c" * 40, "d" * 40
        result = self.module.validate_event_change(
            event_name="push", before=before, base="", head=head,
            root=self.root, runner=self.runner(f"{before}..{head}", []),
        )
        self.assertEqual(result["decision"], "BYPASS")
        self.assertEqual(result["revision_range"], f"{before}..{head}")

    def test_incomplete_or_unsupported_event_ranges_fail_closed(self):
        with self.assertRaises(ValueError):
            self.module.event_range(event_name="push", before="0" * 40, base="", head="a" * 40)
        with self.assertRaises(ValueError):
            self.module.event_range(event_name="workflow_dispatch", before="a" * 40, base="", head="b" * 40)
        with self.assertRaises(ValueError):
            self.module.event_range(event_name="pull_request", before="", base="short", head="b" * 40)

    def test_git_diff_failure_fails_closed(self):
        def failed(command, **kwargs):
            return subprocess.CompletedProcess(command, 128, b"", b"missing object")
        with self.assertRaisesRegex(RuntimeError, "missing object"):
            self.module.changed_paths(f"{'a' * 40}..{'b' * 40}", root=self.root, runner=failed)

    def test_unbound_historical_ledgers_do_not_override_current_bindings(self):
        base, head = "a" * 40, "b" * 40
        paths = ["scripts/current.py", ".factory/artifacts/ledger/issue-31.json", ".factory/artifacts/ledger/issue-55.json"]
        (self.root / ".factory/artifacts/ledger/issue-31.json").write_text(json.dumps({"issue": 31}))
        (self.root / ".factory/artifacts/ledger/issue-55.json").write_text(json.dumps(self.record(["scripts/current.py"])))
        result = self.module.validate_event_change(
            event_name="pull_request", before="", base=base, head=head,
            root=self.root, runner=self.runner(f"{base}...{head}", paths),
        )
        self.assertEqual(result["decision"], "PASS")


if __name__ == "__main__":
    unittest.main()
