import os
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "ci-status.sh"
SEPARATOR = "\x1f"


class CiStatusObservationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.bin = self.root / "bin"
        self.bin.mkdir()
        self.sequence = self.root / "sequence"
        self.index = self.root / "index"
        self.queue_sequence = self.root / "queue-sequence"
        self.queue_index = self.root / "queue-index"
        self.calls = self.root / "gh-calls"
        self.times = self.root / "times"
        self.time_index = self.root / "time-index"
        self.output = self.root / "output"
        self.write_command(
            "gh",
            '''printf '%s\n' "$*" >> "$FAKE_GH_CALLS"
if [ "${1:-}" = "api" ]; then
  index=$(cat "$FAKE_QUEUE_INDEX" 2>/dev/null || echo 0)
  line=$(sed -n "$((index + 1))p" "$FAKE_QUEUE_SEQUENCE")
  if [ -z "$line" ]; then line=$(tail -n 1 "$FAKE_QUEUE_SEQUENCE"); fi
  echo $((index + 1)) > "$FAKE_QUEUE_INDEX"
  echo "$line"
  exit 0
fi
json_value=""
previous=""
for argument in "$@"; do
  if [ "$previous" = "--json" ]; then json_value="$argument"; break; fi
  previous="$argument"
done
if [ "$json_value" = "jobs" ]; then
  echo "failed-step"
  exit 0
fi
index=$(cat "$FAKE_INDEX" 2>/dev/null || echo 0)
line=$(sed -n "$((index + 1))p" "$FAKE_SEQUENCE")
if [ -z "$line" ]; then line=$(tail -n 1 "$FAKE_SEQUENCE"); fi
echo $((index + 1)) > "$FAKE_INDEX"
echo "$line"'''.strip(),
        )
        self.write_command("sleep", "exit 0")
        self.write_command(
            "date",
            '''if [ "${1:-}" = "-u" ]; then
  echo "2026-09-24T00:00:00Z"
  exit 0
fi
index=$(cat "$FAKE_TIME_INDEX" 2>/dev/null || echo 0)
value=$(sed -n "$((index + 1))p" "$FAKE_TIMES")
if [ -z "$value" ]; then value=$(tail -n 1 "$FAKE_TIMES"); fi
echo $((index + 1)) > "$FAKE_TIME_INDEX"
echo "$value"'''.strip(),
        )

    def tearDown(self):
        self.temporary.cleanup()

    def write_command(self, name: str, body: str) -> None:
        path = self.bin / name
        path.write_text(f"#!/usr/bin/env bash\n{body}\n")
        path.chmod(0o755)

    def run_gate(
        self,
        states: list[str],
        times: list[int] | None = None,
        queues: list[str] | None = None,
        **overrides: str,
    ) -> subprocess.CompletedProcess[str]:
        self.sequence.write_text("\n".join(states) + "\n")
        self.queue_sequence.write_text("\n".join(queues or [f"{SEPARATOR}0"]) + "\n")
        self.times.write_text("\n".join(str(value) for value in (times or [100])) + "\n")
        environment = {
            **os.environ,
            "PATH": f"{self.bin}:{os.environ['PATH']}",
            "FAKE_SEQUENCE": str(self.sequence),
            "FAKE_INDEX": str(self.index),
            "FAKE_QUEUE_SEQUENCE": str(self.queue_sequence),
            "FAKE_QUEUE_INDEX": str(self.queue_index),
            "FAKE_GH_CALLS": str(self.calls),
            "FAKE_TIMES": str(self.times),
            "FAKE_TIME_INDEX": str(self.time_index),
            "GH_BIN": str(self.bin / "gh"),
            "DATE_BIN": str(self.bin / "date"),
            "SLEEP_BIN": str(self.bin / "sleep"),
            "POLL_SECONDS": "0",
            "TIMEOUT_MIN": "1",
            "QUEUE_TIMEOUT_SECONDS": "60",
            "NO_PROGRESS_SECONDS": "600",
            **overrides,
        }
        try:
            return subprocess.run(
                [str(SCRIPT), "example/repo", "123", str(self.output)],
                env=environment,
                capture_output=True,
                text=True,
                timeout=10,
            )
        except subprocess.TimeoutExpired as error:
            index = self.index.read_text() if self.index.exists() else "missing"
            self.fail(
                f"gate timed out; index={index!r} stdout={error.stdout!r} stderr={error.stderr!r}"
            )

    def test_reports_progress_transitions_and_success(self):
        result = self.run_gate([
            SEPARATOR.join(["queued", "", "", "", "1"]),
            SEPARATOR.join(["in_progress", "", "Build | Package", "Build | Package=in_progress", "1"]),
            SEPARATOR.join(["in_progress", "", "Tests", "Build | Package=completed,Tests=in_progress", "1"]),
            SEPARATOR.join(["in_progress", "", "Tests", "Build | Package=completed,Tests=in_progress", "1"]),
            SEPARATOR.join(["completed", "success", "", "Build | Package=completed,Tests=completed", "1"]),
        ], times=[100, 100, 109, 110, 111], NO_PROGRESS_SECONDS="10")
        self.assertEqual(result.returncode, 0)
        self.assertIn("state=in_progress step=Build", result.stdout)
        self.assertIn("state=in_progress step=Tests", result.stdout)
        self.assertIn("conclusion=success", result.stdout)

    def test_completed_failure_is_nonzero(self):
        result = self.run_gate([SEPARATOR.join(["completed", "failure", "", "", "1"])])
        self.assertEqual(result.returncode, 1)
        self.assertIn("failed_steps=failed-step", result.stdout)

    def test_queued_run_fails_at_queue_threshold(self):
        result = self.run_gate(
            [SEPARATOR.join(["in_progress", "", "", "Policy=queued", "2"])],
            times=[150, 159, 160],
            queues=[SEPARATOR.join(["Policy", "100"])],
            QUEUE_TIMEOUT_SECONDS="60",
        )
        self.assertEqual(result.returncode, 4)
        self.assertIn("queued without execution", result.stderr)
        self.assertIn("queue_age_seconds=60", result.stdout)
        self.assertIn("/attempts/2/jobs?per_page=100", self.calls.read_text())
        self.assertIn("--paginate", self.calls.read_text())
        self.assertNotIn("--slurp", self.calls.read_text())

    def test_unchanged_active_step_fails_at_progress_threshold(self):
        result = self.run_gate(
            [SEPARATOR.join(["in_progress", "", "Build", "Build=in_progress", "1"])],
            times=[100, 100, 109, 110],
            NO_PROGRESS_SECONDS="10",
        )
        self.assertEqual(result.returncode, 5)
        self.assertIn("no observable transition", result.stderr)


if __name__ == "__main__":
    unittest.main()
