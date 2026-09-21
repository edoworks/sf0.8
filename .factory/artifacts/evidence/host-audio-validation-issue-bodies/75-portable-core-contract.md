# Outcome

Provide one portable production audio boundary consumed by the Mac replay
producer and the future iOS/iPadOS meow-capture app, then prove its target,
non-target, and abstention behavior with owner-approved local fixtures.

# Scope

- Keep confidence policy, target/non-target/abstention decisions, and bounded
  pre-roll/post-roll event windows in `AudioReplayCore` for macOS and iOS.
- Decode approved files and run Apple Sound Analysis through the Mac replay
  executable.
- Emit fixture hashes, environment, observations, decisions, and pass/fail in a
  `HOST_REPLAY_ONLY` report.
- Validate report integrity and reject every failed fixture mechanically.
- Record only non-audio evidence.

# Out of scope

- Live Mac microphone access, iOS microphone sessions, product UI, device
  installation, TestFlight, App Store submission, public identity, cloud
  processing, interpretation, and generalized shared-factory promotion.
- Reuse of Product A or historical household recordings without explicit
  provenance and consent.

# Acceptance criteria

- The package declares macOS and iOS support without coupling shared policy to
  SwiftUI or `AVAudioSession`.
- Tests cover target, non-target, silence/abstention, invalid thresholds,
  duplicate or malformed contracts, bounded event windows, hash drift, path
  escape, and failed fixture expectations.
- A generated non-target smoke fixture completes decode, Sound Analysis,
  structured report generation, SHA-256 validation, and expectation checking.
- An owner-approved local real-meow fixture produces the declared target result.
- Approved silence and non-target comparisons produce their declared results.
- No raw household audio enters Git, CI, logs, issue comments, or durable
  factory evidence.

# Verification

- `swift test --package-path experiments/audio-validation-macos`
- `python3 -m unittest tests.test_validate_audio_replay`
- `python3 scripts/validate-audio-replay.py REPORT.json --root FIXTURE_ROOT`
- `python3 scripts/validate-human-action-queue.py .factory/human-action-queue.json`
- `python3 -m unittest discover -s tests -p 'test_*.py'`
- `python3 scripts/validate-ecosystem.py`
- `python3 scripts/validate-automation.py`
- `git diff --check`

# Dependencies

- Issue #74 product contract: complete.
- Owner approval of local-only target and comparison fixtures through
  `meow-capture-fixture-approval` in `.factory/human-action-queue.json`.
- Issue #76 and issue #77 remain blocked until this production boundary and its
  approved-fixture evidence are complete.

# Authority and privacy

- Local implementation and generated non-household smoke fixtures are
  authorized under issue #75.
- Household fixture selection, ownership, consent, and local replay require the
  explicit human action above.
- This issue does not authorize ambient listening, external repository
  creation, publication, release, device microphone claims, or persistence of
  private audio in factory artifacts.
- Host replay is never physical iPhone/iPad or real-cat product evidence.

# Source provenance

- `docs/decisions/2026-09-20-meow-capture-product-contract.md`
- `docs/host-audio-validation.md`
- `.factory/artifacts/evidence/host-audio-replay-result-semantics-5whys.md`
- `.factory/artifacts/evidence/host-audio-validation-e2e-map.md`
- GitHub issue #73 and issue #75

# Classification

`enhancement`: add a portable production audio boundary and replay evidence.

# Priority

`P1`: this is the active dependency for the selected customer-zero capability
and blocks live listening and the Apple vertical slice.

# Triage review

- Duplicate review: reviewed issue #73 (parent map), #74 (product contract),
  #76 (live Mac probe), #77 (Apple vertical slice), #78 (device validation),
  #79 (real-cat acceptance), and #80 (issue-handoff guard). No duplicate; each
  has a distinct outcome.
- Reprioritization review: remains `P1`; no higher-priority active audio issue
  supersedes this dependency. Product A remains shelved and is not a competing
  implementation lane.
