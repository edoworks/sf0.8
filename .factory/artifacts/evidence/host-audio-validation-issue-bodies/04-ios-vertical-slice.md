# Parent

#73

# Blocked by

New app contract and portable production audio core.

# Outcome

Build the smallest polished iOS/iPadOS vertical slice that automatically
captures a likely meow and supports audible local playback and deletion.

# Acceptance criteria

- The app consumes the same portable core used by Mac replay.
- iOS-specific code owns microphone permission, `AVAudioSession`, routing,
  interruptions, and lifecycle behavior.
- The primary flow requires no fake classifier result or developer control.
- Captured clips stay local and can be replayed and deleted.
- Simulator tests cover deterministic state transitions, permission recovery,
  silence, non-target input, interruptions, and repeated sessions.
- The first-launch and captured-event surfaces are visually deliberate on
  iPhone and iPad.

# Verification

- Canonical build/unit/UI test command recorded by the product
- Rendered iPhone and iPad evidence
- Policy check proving fake input cannot justify production capture
