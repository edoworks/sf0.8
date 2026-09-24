# State-Aware CI Observation

## Impact

Integration repeatedly appeared stuck because long blocking GitHub CLI watch
calls emitted undifferentiated `pending` output. The first occurrence was a real
offline self-hosted runner; later occurrences were active hosted Xcode jobs.

## Five Whys

1. Progress was opaque because completion used long `gh ... --watch` calls.
2. The watch output did not distinguish a zero-step queued job from an active
   long-running Xcode step.
3. Completion procedure optimized for a terminal result rather than reporting
   state transitions and diagnosing missing progress.
4. The runner-readiness correction covered availability but not the observation
   loop, so the same watch primitive was reused immediately afterward.
5. No global or PRD contract defined queue, active-step, no-progress, and overall
   deadlines separately.

## Corrections And Guard

- Immediate correction: stop using long blocking GitHub watch commands and read
  status, active step, and timestamps explicitly.
- Root correction: `scripts/ci-status.sh` now reports state transitions and has
  independent queue, no-progress, and overall thresholds. Queue age comes from
  zero-step queued jobs in the current run attempt, and progress includes every
  job and step rather than only the first active step.
- Global correction: OpenCode factory guidance requires snapshot-based CI
  observation and forbids treating repetitive `pending` output as progress.
- Recurrence guard: behavioral tests cover progress transitions, queue timeout,
  stalled active work, terminal success, and terminal failure.

The checks themselves remain authoritative. Observation limits do not authorize
merge, cancellation, rerun, or bypass, and no cause is inferred merely from a
job remaining on one active step until its declared threshold is exceeded.

## Verification Harness Failure

The first behavioral-test run timed out instead of advancing through its fake
GitHub states.

1. The monitor stayed queued because every fake `gh` invocation returned the
   first fixture state.
2. Every invocation returned that state because the fake read its call index
   but did not persist the incremented value.
3. The missing write survived initial review because single-state timeout and
   terminal-result tests did not require the fixture to advance.
4. The successful-transition test exposed the defect by requiring four ordered
   states and enforcing a ten-second subprocess deadline.

The immediate and root correction is to persist the increment after each fake
`gh` call. The successful-transition test is the mechanical recurrence guard:
without that write it times out rather than producing queued, build, test, and
completed transitions. The focused four-case suite and the full 382-test suite
both pass with the correction.

A later live smoke test exposed a second verification defect: the installed
GitHub CLI rejects `gh api --slurp` when `--jq` is also present. The invalid
combination was selected while adding pagination because the option help lists
both flags but does not establish that they compose, and the fake CLI accepted
unknown flag combinations. The correction keeps `--paginate`, emits one
queued-job summary per page through `--jq`, and computes the oldest timestamp in
shell. The test harness now rejects recurrence by asserting that pagination is
present and `--slurp` is absent; a completed-run smoke test exercises the real
CLI path.
