# Parent

#73

# Blocked by

Functional iOS/iPadOS vertical slice.

# Outcome

Automate exact-revision installation and bounded audio validation on physical
iPhone and iPad while preserving human trust boundaries.

# Acceptance criteria

- The harness proves the exact clean revision, build, install, and launch.
- Device evidence covers permission recovery, microphone pickup, playback,
  route changes, interruption recovery, repeated sessions, and deletion.
- iPhone and iPad results are recorded separately.
- Unlock, trust, consent, and acoustic judgment remain explicit human actions.
- Host replay is never cited as physical-device evidence.

# Verification

- Exact-revision device script passes on one iPhone and one iPad
- Device evidence manifest validates
- Failure and recovery paths are exercised
