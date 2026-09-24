# Issue 48 Map Closeout

- Issues 48-53 report `CLOSED` through the combined closeout guard.
- Issue 53's final matrix merged in PR 144 at `e0f0bd5`; its policy check passed.
- Canonical continuation, integrity, remote snapshot, and `NOW.md` now represent
  the completed reconciliation map.
- Private predecessor completeness remains `UNKNOWN`; no inaccessible scope is
  inferred complete.

## Terminal-State Validator Analysis

1. The existing integrity rule required the active increment gate to be `OPEN`.
2. That is correct while continuation is in progress but cannot represent a
   verified terminal continuation whose active increment is already closed.
3. The rule was introduced to prevent premature gate closure and did not model
   the map's completed state.

Root cause: continuation-to-gate validation encoded only the active lifecycle
state. Immediate correction: require `CLOSED` when continuation is `COMPLETE`
and `OPEN` otherwise. Root-cause correction: focused tests exercise both
terminal and in-progress semantics, and the changed-path ledger binds the
validator change to map issue 48.

Independent review found that the first correction checked only the final
increment, did not reconcile integrity status with continuation status, and used
an issue ledger absent from the control-plane binding registry. The corrected
guard requires both active map and increment gates to match the lifecycle,
requires both status projections to agree, and binds issue 48 canonically.
Focused negative tests cover an open terminal increment, an open terminal map,
status drift, and a closed in-progress increment.

## Capability-Ledger Gate Failure

1. The first exact PR-range validation blocked the issue 48 ledger for lacking
   an external candidate.
2. The ledger documented only the existing internal integrity validator because
   the code change was a narrow terminal-state extension.
3. The ecosystem policy requires external discovery evidence for every new or
   extended machinery path, regardless of implementation size.

Root cause: the closeout ledger omitted the proportional external-discovery
record required by the changed-path policy. Immediate correction: add the
first-party GitHub issue-state contract as `LEARN_FROM` while retaining the
internal validator as the only compatible implementation. Recurrence guard:
run the exact PR event range before every push; the corrected range must pass.
