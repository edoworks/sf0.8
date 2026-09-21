# Issue #75 Progress

Implemented and verified the next portable-core slice:

- `AudioReplayCore` now declares macOS and iOS support.
- Shared logic owns confidence-based `TARGET`, `NON_TARGET`, and `ABSTAIN`
  decisions plus bounded pre-roll/post-roll event windows.
- Fixture expectations are distinct from classifier decisions; any mismatch is
  a failed fixture and fails Python evidence validation.
- A generated non-target speech fixture completed the full local path: decode,
  Sound Analysis, report generation, SHA-256 verification, and expectation
  validation. It abstained as expected.
- The result-semantics defect and recurrence guard are recorded in
  `.factory/artifacts/evidence/host-audio-replay-result-semantics-5whys.md`.

Verification:

- `swift test --package-path experiments/audio-validation-macos` — 9 tests
- `python3 -m unittest tests.test_validate_audio_replay tests.test_human_actions` — 7 tests
- `python3 scripts/validate-human-action-queue.py .factory/human-action-queue.json`
- End-to-end generated non-target replay and report validation — passed

Issue #75 remains open. Completion still requires owner-approved local real-meow
and comparison fixtures replayed through this production boundary. The human
action queue records the provenance/consent gate; no historical household audio
was reused or copied.
