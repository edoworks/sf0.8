import os
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "runner-readiness.sh"


class RunnerReadinessTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name) / "runner"
        self.bin = Path(self.temporary.name) / "bin"
        self.root.mkdir()
        self.bin.mkdir()
        self.pgrep = self.bin / "pgrep"

    def tearDown(self):
        self.temporary.cleanup()

    def write_command(self, path: Path, body: str) -> None:
        path.write_text(f"#!/usr/bin/env bash\n{body}\n")
        path.chmod(0o755)

    def run_guard(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(SCRIPT), str(self.root)],
            env={**os.environ, "PGREP_BIN": str(self.pgrep)},
            capture_output=True,
            text=True,
        )

    def test_ready_service_and_listener_pass(self):
        self.write_command(
            self.root / "svc.sh",
            f'test "$PWD" = "{self.root}" || exit 9\necho \'Started: runner\'',
        )
        self.write_command(self.pgrep, "exit 0")
        result = self.run_guard()
        self.assertEqual(result.returncode, 0)
        self.assertIn("READY", result.stdout)

    def test_stopped_service_fails_before_listener_check(self):
        self.write_command(self.root / "svc.sh", "echo 'Stopped'")
        self.write_command(self.pgrep, "exit 0")
        result = self.run_guard()
        self.assertEqual(result.returncode, 3)
        self.assertIn("not started", result.stderr)

    def test_started_service_without_listener_fails(self):
        self.write_command(self.root / "svc.sh", "echo 'Started: runner'")
        self.write_command(self.pgrep, "exit 1")
        result = self.run_guard()
        self.assertEqual(result.returncode, 4)
        self.assertIn("no active listener", result.stderr)

    def test_missing_service_command_fails(self):
        self.write_command(self.pgrep, "exit 0")
        result = self.run_guard()
        self.assertEqual(result.returncode, 2)
        self.assertIn("service command is missing", result.stderr)

    def test_ci_status_checks_readiness_before_waiting_on_queued_sf08(self):
        ci_status = (ROOT / "scripts" / "ci-status.sh").read_text()
        readiness = ci_status.index('"$SCRIPT_DIR/runner-readiness.sh"')
        wait_loop = ci_status.index("while :; do")
        self.assertLess(readiness, wait_loop)
        self.assertIn('"$initial_status" = "queued"', ci_status)


if __name__ == "__main__":
    unittest.main()
