# Executive Council Lifecycle Conflict 5-Whys

Date: 2026-09-19

## Defect

The canonical Customer Zero record describes Product A as an active product
direction while the portfolio and release-board evidence classify it as
shelved/read-only. A review that silently chooses one claim could recommend
unauthorized work.

## Analysis

1. Why could the council receive contradictory lifecycle claims? Because
   customer-direction evidence and portfolio/release evidence are stored in
   separate artifacts with different purposes.
2. Why are those artifacts not reconciled at generation time? Because no
   existing review consumer compared lifecycle claims across sources.
3. Why was that comparison absent? The factory had release and portfolio
   validators but no cross-domain decision review.
4. Why does that matter? Executive synthesis could convert stale or scoped
   evidence into a false current-state recommendation.
5. Evidence ends here. The root cause is a missing cross-domain conflict check;
   no further cause is claimed without examining artifact ownership/history.

## Correction

- Immediate: the council records the conflict as
  `BLOCKED_UNRESOLVED_SOURCE_CONFLICT` and does not infer current authority.
- Root-cause correction: the council validator requires every detected conflict
  to remain explicitly unresolved or resolved before synthesis.
- Recurrence guard: `tests/test_executive_council.py` fails if lifecycle conflict
  is absent or represented as a settled fact without resolution.
