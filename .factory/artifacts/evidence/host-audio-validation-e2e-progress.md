# Issue 73 Progress

Implemented the authorized factory-side slice for host audio validation.

- Added `scripts/validate-audio-replay.py`.
- Added contract tests covering valid reports, fixture hash drift, path escape,
  and rejection of device-proof claims.
- Added `docs/host-audio-validation.md` describing the staged evidence boundary
  and privacy constraints.
- Product A was not modified or revived; it remains shelved/read-only.

Verification passed:

- `python3 -m unittest discover -s tests -p 'test_*.py'` — 247 tests passed.
- `python3 scripts/validate-ecosystem.py` — passed.
- `python3 scripts/validate-automation.py` — passed.
- `git diff --check` — passed for tracked changes.

Remaining scope for issue #73:

- A macOS Swift replay producer now exists at
  `experiments/audio-validation-macos`; it reads a manifest, decodes approved
  fixtures, runs Sound Analysis, and emits `HOST_REPLAY_ONLY` reports.
- An authorized product repository still needs to integrate its portable
  production classifier boundary with this producer.
- A physical iPhone/iPad validation gate remains required for device claims.
- Any live Mac microphone probe requires explicit owner-started bounded consent.

Additional verification:

- `swift test --package-path experiments/audio-validation-macos` — 4 tests passed.
- `swift run --package-path experiments/audio-validation-macos audio-replay --help` — passed.
