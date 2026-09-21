# Conservative Projection Gap

## Impact

Before the governor was activated, its planned-request estimate used one
quarter of the tier context ceiling for a fresh session. A first prompt larger
than that estimate could have crossed a rolling budget cap. No governed request
was shown to cross a cap through this path.

## Evidence-Based Whys

1. A large first prompt could cost more than projected because projection used
   `context_limit / 4` when no prior message metadata existed.
2. The estimate used a typical-context heuristic because `chat.params` does not
   expose authoritative tokenization for the pending prompt.
3. The heuristic was treated as conservative even though it was only typical.
   Review identified that mismatch before completion.
4. Evidence does not establish why the original review and tests failed to
   distinguish typical from worst-case input; deeper causes are unknown.

## Corrections And Guard

- Immediate and root-cause correction: price every pending cloud request at the
  full tier context ceiling, or the measured current context if larger.
- Mechanical recurrence guard: the dispatch test now requires projected input
  to equal the full configured tier context ceiling.
- Verification: `npm test` must pass, and the historical replay must keep every
  reported rolling maximum at or below its configured cap.

## Concurrent Dispatch Gap

### Evidence-Based Whys

1. Concurrent requests could each pass because they read the same completed
   usage total before either request wrote a message row.
2. Only completed message metadata was counted; pending work had no ledger
   representation.
3. Pending work was omitted because the first implementation modeled historical
   rolling usage but not admission concurrency.
4. The replay was sequential, so it could not expose simultaneous admission.
5. Evidence does not establish a deeper process cause; further claims would be
   assumptions.

### Corrections And Guard

- Immediate and root-cause correction: serialize admission with a filesystem
  lock and atomically reserve each request's worst-case projected charge.
- A matching message row clears its reservation. A 60-minute TTL recovers an
  abandoned reservation without silently granting immediate capacity.
- Mechanical recurrence guard: a unit test proves pending reservations consume
  rolling capacity before another dispatch is admitted.

## Reservation Lock Integration Failure

### Evidence-Based Whys

1. The first live reservation probe failed before dispatch because lock creation
   targeted a nonexistent nested directory.
2. The caller passed a lock-file path to `acquireRoutingLock`, but that helper
   accepts a directory and appends its own `.update.lock` name.
3. Unit tests covered reservation arithmetic but not the helper's filesystem
   contract. Evidence does not establish a deeper cause.

### Corrections And Guard

- Immediate and root-cause correction: pass the existing model-routing
  directory to the shared lock helper, intentionally serializing reservations
  with catalog updates.
- Mechanical recurrence guard: repeat a live cloud dispatch through a newly
  loaded plugin and require a successful exact response before completion.

The first successful probe then showed its reservation remained active. The
message row is created before `chat.params`, so its `time_created` predates the
reservation; completion is represented by `time_updated` plus `finish` or an
error. Reconciliation now requires that terminal state and an update timestamp
after admission. This was verified by re-reading live status after the corrected
reconciliation and observing `reserved: 0`. Evidence does not support a deeper
causal claim.

The first full test rerun failed because the test's inline policy fixture did
not include the newly required TTL. Production policy already contained it.
The fixture drifted because policy shape is duplicated in the test; the direct
correction adds the TTL to that fixture, and the existing lifecycle assertions
are the mechanical guard. Evidence does not establish further causal depth.
