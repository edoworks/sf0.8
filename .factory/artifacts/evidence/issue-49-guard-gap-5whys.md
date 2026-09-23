# Issue 49 Evidence-Integrity Guard Gap: 5-Whys

Date: 2026-09-23
Parent map: edoworks/factory#48

## Defect

The first issue #47 implementation passed while ignoring its declared canonical
continuation file, validating no durable timeout receipts, checking evidence
only in the current index, and accepting manually entered gate states.

## Evidence-Based 5-Whys

1. Why did semantic drift pass? The command validated a duplicate continuation
   object and current paths rather than canonical records at cited revisions.
2. Why could remote gate drift pass? Gate values were syntax-checked but never
   compared with a freshness-bounded remote snapshot.
3. Why did timeout coverage overstate protection? Only unit fixtures called the
   timeout classifier; the canonical command discovered no durable receipts.
4. Why were these gaps missed? The final review checked function behavior but
   not whether the production entrypoint invoked each promised guard.
5. Evidence ends at incomplete integration coverage; no deeper cause is proven.

## Corrections

- Load one canonical continuation record and validate its checked-in projection.
- Resolve every evidence path with `git cat-file` at its cited commit.
- Validate freshness-bounded remote issue snapshots and separate remote,
  evidence, and effective gate state.
- Discover and validate every durable timeout receipt; retain unsupported
  historical classifications as `UNKNOWN`.

## Recurrence Guard

Focused tests reject stale snapshots, invalid closed gates, wrong weekdays,
untracked evidence, malformed revisions, continuation drift, and unsupported
timeout classifications. CI executes the same repository entrypoint.
