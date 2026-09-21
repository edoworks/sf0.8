# Finance Data Engineering Question Bank

Date: 2026-09-20
Audience: software engineers building financial transaction pipelines
Decision: expand the local learning surface beyond generic algorithms and Scala

## Coverage Added

- Spark Structured Streaming: event time, watermarks, deduplication, checkpoints, replay, and late-data policy.
- Azure Synapse Analytics: distribution skew, statistics, data movement, and replicated dimensions.
- Azure Event Hubs: partition-scoped ordering, checkpoint placement, replay, and idempotent effects.
- Azure Data Lake Storage Gen2: small files, columnar layout, committed publication, and idempotent reruns.
- Financial reconciliation: immutable evidence, missing and duplicate events, amount mismatches, and auditable corrections.

The same five scenario families are now available in both the mobile web bank
and the native iOS bank; the native surface also preserves the Apple
Intelligence assist and local reference library.

## Evidence Boundary

These are concept-refresh questions and visible contract cases, not production
certification or vendor-specific operational guarantees. The runner compares
predefined expected and observed outcomes; it does not compile arbitrary Scala or
SQL and does not execute untrusted code.

## Design Guard

Every platform question includes at least four boundary cases, progressive hints,
an explanation, and a named reference. Future additions should preserve those
fields and include a failure or recovery case, not only a happy-path query.

## Open Questions

- Which Spark, Synapse, Event Hubs, and ADLS cases are most frequently requested by the intended learner?
- Should a future authenticated toolchain run real Scala/Spark tests, and what isolation and cost boundary would be required?
- Which Azure-version or service-mode differences need to be made explicit before using these as operational guidance?
