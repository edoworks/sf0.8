# Portfolio Discovery Failure 5-Whys

## Failure

The prior audit passed while its reconciliation artifact omitted Veilsort as a
product. Veilsort was independently evidenced by the sf0.7 App Store survey,
bundle identifier `com.foculoom.veilsort`, local source, and deployment evidence.

## Causal chain

1. Veilsort was absent from the prior reconciliation because that artifact
   reconciled a hand-selected repository/surface list rather than products.
2. The repository/surface list was considered sufficient because discovery
   enumerated known portfolio records and bounded local directories, but did not
   independently form a public/distributed product set.
3. The validator passed because it asserted expected IDs and internal artifact
   counts, not set differences, durable identity relationships, or recall.
4. Product and repository identity were conflated: a product could exist in
   App Store evidence without appearing as one of the reconciled repository IDs.
5. No adversarial fixture omitted a verified shipping product from the registry,
   so completion had no mechanical way to detect silent portfolio loss.

## Root causes and guards

- Root cause: registry correctness was treated as portfolio completeness.
  Guard: independent discovery excludes the registry and reconciliation requires
  verified shipping recall of 100%.
- Root cause: product identity was not a first-class entity.
  Guard: durable bundle IDs, distribution records, repositories, folders, and
  provenance are reconciled independently.
- Root cause: scheduler completion covered only known work.
  Guard: scheduler emits known-work idleness separately from discovery
  confidence and unreconciled candidate count.
- Root cause: omission had no adversarial acceptance test.
  Guard: the verified shipping fixture remains outside discovery input and an
  omitted product blocks `PORTFOLIO_RECONCILIATION_BLOCKED`.
