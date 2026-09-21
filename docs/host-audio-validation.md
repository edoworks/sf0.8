# Host Audio Validation

Issue: [Add host-side audio validation E2E](https://github.com/edoworks/sf0.8/issues/73)

The factory-side contract accepts structured output from a future macOS audio
replay runner. It verifies fixture existence and content hashes, records the
runner/environment, and requires the explicit claim `HOST_REPLAY_ONLY`.

The first replay producer lives under
`experiments/audio-validation-macos`. It is a macOS Swift Package with a
library, executable, and pure status-evaluation tests. The executable reads a
manifest and uses Apple Sound Analysis against each approved audio file.

The manifest is intentionally small and contains no audio bytes:

```json
{
  "schema_version": 1,
  "fixtures": [
    {
      "id": "cat-001",
      "path": "fixtures/cat-001.wav",
      "expected_labels": ["cat"],
      "minimum_confidence": 0.5,
      "expected_decision": "TARGET"
    }
  ]
}
```

Run it with `swift run --package-path experiments/audio-validation-macos
audio-replay --manifest MANIFEST.json --root FIXTURE_ROOT --output REPORT.json`.
The report is then checked by `scripts/validate-audio-replay.py`.

`AudioReplayCore` supports macOS and iOS and owns the shared confidence and
abstention policy plus bounded pre-roll/post-roll event-window calculation.
Platform adapters remain responsible for decoding, microphone permissions,
audio sessions, and persistence.

Each fixture declares an expected `TARGET`, `NON_TARGET`, or `ABSTAIN`
decision. Reports preserve that classifier decision separately from fixture
`PASS` or `FAIL`; the Python validator fails closed when any expectation fails.

This is intentionally not a microphone implementation and does not revive the
shelved Product A repository. The next authorized product increment can provide
a Swift macOS replay executable and emit this report shape.

## Evidence boundary

Host replay can establish deterministic decoding and shared classifier behavior
for approved fixtures. It cannot establish iOS permissions, `AVAudioSession`
routes, device microphone response, Bluetooth behavior, speaker feedback,
physical-device timing, or real-cat response. Those remain device or empirical
evidence classes.

## Privacy boundary

Fixture paths must remain inside the report root and hashes are checked against
the actual bytes. Household recordings must not be committed, uploaded, logged,
or copied into CI artifacts. Any future live-Mac probe requires a visible,
bounded, owner-started session and must fail closed on microphone denial.

## Verification

```bash
python3 -m unittest tests.test_validate_audio_replay
python3 scripts/validate-audio-replay.py REPORT.json
swift test --package-path experiments/audio-validation-macos
```
