# Parent

#73

# Blocked by

The new meow-capture product contract.

# Outcome

Provide one portable production audio boundary consumed by both the Mac replay
producer and the future iOS/iPadOS app.

# Acceptance criteria

- Separate normalized audio, event detection, confidence/abstention policy,
  and event extraction from SwiftUI and `AVAudioSession`.
- Replay approved real-audio fixtures through the production boundary.
- Cover target, silence, non-target, malformed input, and threshold behavior.
- Emit and validate `HOST_REPLAY_ONLY` evidence with fixture hashes and
  environment metadata.
- Keep household audio outside Git, CI, logs, and durable factory evidence.

# Verification

- `swift test --package-path experiments/audio-validation-macos`
- `python3 scripts/validate-audio-replay.py REPORT.json --root FIXTURE_ROOT`
- Repository canonical checks
