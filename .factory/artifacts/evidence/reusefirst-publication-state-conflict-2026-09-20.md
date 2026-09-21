# ReuseFirst Publication-State Conflict

Date: 2026-09-20
Status: `SUPERSEDED_BY_CUSTOMER_ZERO_REVIEW`

## Observed Conflict

- `.factory/artifacts/public-sources.json` records `reusefirst` at
  `edoworks/artifacts`, version `1.2.0`, release tag `reusefirst/v1.2.0`, and
  source revision `30e588b4dc0d869da9b58a01d91c22d6f4931361`.
- `.factory/artifacts/reuse-registry.json` now retains `reusefirst` as a
  `PUBLIC_CANDIDATE` with `publication_approved: false` pending Customer Zero
  dogfood.
- `.factory/artifacts/records/reuse-gate.json` calls it a
  `validated-candidate`; the external release is not treated as customer-zero
  verified.
- `constitution` and `asc` are explicitly marked `RELEASED` with release URLs.

Read-only public verification on 2026-09-20 confirmed both the ReuseFirst
source tree and release page:

- https://github.com/edoworks/artifacts/tree/reusefirst/v1.2.0/artifacts/reusefirst
- https://github.com/edoworks/artifacts/releases/tag/reusefirst/v1.2.0

## 5-Whys

1. **Why is it unclear whether ReuseFirst was released?** The public-source
   registry records a canonical release, while the shareability and artifact
   records retain a candidate/unapproved state.
2. **Why can those states coexist?** The migration registry tracks artifact
   location and revision, while the shareability registry tracks approval and
   lifecycle; no invariant currently requires their publication states to
   agree.
3. **Why was no invariant added?** The migration increment focused on pointer,
   checksum, and release evidence, while the reuse gate preserved a
   human-approval boundary.
4. **Why does that create ambiguity?** “Published to the canonical artifact
   repository” and “approved for public promotion by the factory” were treated
   as separate claims without an explicit reconciliation record.
5. **Root cause:** a release was externally present while the local human
   approval record remained false; two source-of-truth dimensions lacked a
   machine-checked relationship. The subsequent Customer Zero review found a
   second defect: internal capability use had been counted as public artifact
   consumption.

## Safe Correction

- Immediate correction: keep local approval false and block release readiness
  until Customer Zero dogfood is evidenced; do not republish or mutate the
  external repository.
- Root correction: add a human-reviewed reconciliation record or validator
  rule that distinguishes canonical presence, release evidence, and current
  publication approval.
- Recurrence guard: reject claims that call an artifact both released and
  unreleased without an explicit state transition or reconciliation reference.

Implemented in this increment:

- `.factory/artifacts/publication-state-reconciliation.json` records the
  explicit `PENDING_CUSTOMER_ZERO_DOGFOOD` state.
- `PUBLIC_RELEASED` is now distinct from `PUBLIC_CANDIDATE`; approved releases
  require Customer Zero and approval evidence.
- Validators require matching reconciliation evidence across canonical source,
  lifecycle, disposition, and approval state.

## Verification

- `python3 scripts/validate-ecosystem.py` passed.
- `python3 scripts/validate-reuse-registry.py` passed.
- `python3 scripts/validate-artifacts.py` passed.
- `python3 -m unittest tests.test_ecosystem_gates tests.test_publication_state_reconciliation` passed.
- Full suite: 209 tests passed.
- No external mutation or publication was performed by this reconciliation.
