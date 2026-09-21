import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validate_audio_replay", ROOT / "scripts/validate-audio-replay.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class AudioReplayContractTests(unittest.TestCase):
    def make_report(self, root: Path) -> dict:
        fixture = root / "meow.wav"
        fixture.write_bytes(b"RIFF test fixture")
        return {
            "schema_version": 1,
            "runner": {"name": "mac-replay", "version": "test"},
            "environment": {"platform": "macOS", "os": "test"},
            "device_claim": "HOST_REPLAY_ONLY",
            "fixtures": [{
                "id": "meow-001",
                "path": "meow.wav",
                "sha256": hashlib.sha256(fixture.read_bytes()).hexdigest(),
                "observations": [{"label": "cat", "confidence": 0.8}],
                "decision": "TARGET",
                "status": "PASS",
                "sample_rate": 44100,
                "frame_count": 128,
            }],
        }

    def test_valid_report_checks_fixture_hash(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.assertEqual([], MODULE.validate_report(self.make_report(root), root))

    def test_host_report_cannot_claim_device_proof(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            report = self.make_report(root)
            report["device_claim"] = "IPHONE_VERIFIED"
            self.assertIn("report: device_claim must be HOST_REPLAY_ONLY", MODULE.validate_report(report, root))

    def test_changed_fixture_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            report = self.make_report(root)
            (root / "meow.wav").write_bytes(b"changed")
            self.assertIn("fixtures[0]: sha256 does not match fixture bytes", MODULE.validate_report(report, root))

    def test_fixture_path_cannot_escape_root(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            report = self.make_report(root)
            report["fixtures"][0]["path"] = "../outside.wav"
            self.assertIn("fixtures[0]: path escapes the report root", MODULE.validate_report(report, root))

    def test_failed_fixture_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            report = self.make_report(root)
            report["fixtures"][0]["status"] = "FAIL"
            self.assertIn("fixtures[0]: fixture expectation failed", MODULE.validate_report(report, root))

    def test_malformed_fixture_id_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            report = self.make_report(root)
            report["fixtures"][0]["id"] = ["not", "a", "string"]
            errors = MODULE.validate_report(report, root)
            self.assertIn("fixtures[0]: id must be a non-empty string", errors)

    def test_malformed_observation_and_audio_metadata_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            report = self.make_report(root)
            report["fixtures"][0]["observations"] = [{"label": "", "confidence": 2}]
            report["fixtures"][0]["sample_rate"] = 0
            report["fixtures"][0]["frame_count"] = -1
            errors = MODULE.validate_report(report, root)
            self.assertIn("fixtures[0].observations[0]: label must be a non-empty string", errors)
            self.assertIn("fixtures[0].observations[0]: confidence must be a number from 0 to 1", errors)
            self.assertIn("fixtures[0]: sample_rate must be a positive number", errors)
            self.assertIn("fixtures[0]: frame_count must be a non-negative integer", errors)


if __name__ == "__main__":
    unittest.main()
