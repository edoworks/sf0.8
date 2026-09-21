# Host Audio Validator Hardening

Date: 2026-09-20
Issue: #75
Scope: fail-closed validation of structured host-replay evidence

## Correction

The report validator now rejects malformed fixture identifiers, observation
labels/confidences, sample rates, and frame counts. These fields are required
because they are emitted by the replay producer and are part of the durable
evidence contract. Invalid values return validation errors rather than raising
an exception or being accepted as evidence.

## Verification

- `python3 -m unittest tests.test_validate_audio_replay` — 7 tests passed.
- `swift test --package-path experiments/audio-validation-macos` — 9 tests passed.
- `git diff --check -- scripts/validate-audio-replay.py tests/test_validate_audio_replay.py` — passed.

No audio bytes were added to this evidence. The change does not establish
microphone, physical-device, real-cat, or product-readiness claims.

## 5-Whys

1. Why could malformed replay evidence pass or crash validation? The validator
   checked only the presence of shallow fixture keys and assumed the identifier
   was hashable.
2. Why were nested observations and audio metadata not checked? The initial
   contract focused on fixture hash/path integrity and decision/status values.
3. Why was that boundary incomplete? The structured report producer already
   emitted observation and audio metadata, but the validator did not mirror the
   full producer schema.
4. Why did tests not catch the mismatch? Tests covered valid reports, hash
   drift, path escape, device-claim rejection, and failed status, but not
   malformed nested fields or metadata.
5. Why could the gap recur? There was no test fixture requiring every emitted
   field to be type- and range-validated.

Root cause: the evidence validator and producer contract evolved out of sync.

Immediate correction: validate the emitted nested fields and metadata with
fail-closed type/range checks.

Recurrence guard: regression tests cover unhashable IDs, malformed
observations, invalid confidence, sample rate, and frame count.

## Remaining Boundary

Issue #75 remains open. Owner-approved comparison fixtures and integration with
the future product capture boundary are still required. Host replay remains
`HOST_REPLAY_ONLY`.
