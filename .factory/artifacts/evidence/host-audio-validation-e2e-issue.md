# Host-Side Audio Validation E2E

## Scope

Design and implement the smallest authorized factory capability that can
validate an audio product on the Mac before installation on an iPhone or iPad.
Start with deterministic, offline fixture replay. Do not revive Product A or
add unattended ambient microphone capture in this increment.

## Acceptance criteria

- A portable audio-validation boundary is documented or implemented without
  coupling the core contract to SwiftUI or iOS-only audio-session behavior.
- A Mac-side replay command can consume approved fixtures and emit structured
  results containing fixture hash, environment, classifier/pipeline version,
  observations, and pass/fail.
- Tests cover valid input, silence/non-target input, malformed input, and
  abstention or confidence-threshold behavior.
- The evidence explicitly states what Mac replay does and does not prove about
  physical iPhone/iPad microphone behavior.
- No raw household audio is committed, uploaded, logged, or placed in CI
  artifacts.
- A follow-up design records the authorization and privacy requirements for any
  future visible, bounded live-Mac listening session.

## Verification

- Run the repository's canonical checks for every changed factory file.
- Run the Mac replay and its tests against approved fixtures.
- Validate the resulting evidence artifact against the repository artifact
  contract.

## Root-cause context

Previous audio-product validation relied on simulator/fake-microphone paths
that bypassed the real classifier and did not establish physical microphone
behavior. The immediate correction is host-side real-fixture replay; the
recurrence guard is a staged validation matrix that never labels host replay as
device proof.
