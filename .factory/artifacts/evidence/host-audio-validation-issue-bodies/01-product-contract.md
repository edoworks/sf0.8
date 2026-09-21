# Parent

#73

# Outcome

Define the new, narrow iOS/iPadOS meow-capture app as the first consumer of the
host audio-validation capability. This does not revive Product A.

# Acceptance criteria

- Record one owner-visible acceptance sentence centered on automatic meow
  capture and audible playback.
- Define the minimum session, privacy boundary, non-goals, stop rules, and
  device/empirical evidence classes.
- Record a provisional internal identity without authorizing publication,
  TestFlight, App Store submission, or a new external repository.
- Synchronize `NOW.md` and the human-action queue.
- Preserve Product A as shelved/read-only.

# Verification

- `python3 scripts/validate-human-action-queue.py .factory/human-action-queue.json`
- `python3 -m unittest tests.test_human_actions`
- `git diff --check`
