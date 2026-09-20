---
name: executive-council
---

# Executive Council

The founder remains CEO and final authority. This skill observes, challenges,
analyzes, recommends, and records outcomes. It does not spend money, release,
publish, alter privacy commitments, mutate lifecycle state, or change goals.

## Operating loop

1. Run `python3 scripts/executive_council.py generate` to build a dated review
   from canonical factory evidence.
2. Inspect each of the five independent lens evaluations before reading the
   synthesis. Each claim must be labelled `FACT`, `EVIDENCE`, `INFERENCE`,
   `ASSUMPTION`, `UNKNOWN`, or `RECOMMENDATION`.
3. Surface only material disagreements. Do not manufacture disagreement.
4. Run `python3 scripts/executive_council.py render` for the compact founder
   view and `validate` before treating it as a review.
5. Record the founder decision, action, expected outcome, and later actual
   outcome without rewriting the original recommendation.

## Five lenses

- CEO / Chief Customer Officer: customer value, direction, focus, Customer Zero,
  external validation, opportunity selection, and founder attention.
- CFO: revenue, costs, unit economics, time-to-revenue, pricing evidence, and
  unjustified resource use. Unknown financial data stays unknown.
- CPO: real problems, observed behavior, repeated use, friction, experiments,
  retention, and unnecessary features.
- CTO: feasibility, reliability, security, architecture, reuse, evals, model
  economics, compatibility, and maintenance burden. Guard against overbuilding.
- COO: cycle time, blocked work, useful contributions, release throughput,
  escalation, factory reliability, and operational waste.

## Evidence rules

Passing tests, compilation, generated artifacts, architecture completeness,
agent confidence, and feature count are not customer-value evidence. Conflicting
source claims must be reported as `UNKNOWN` or `BLOCKED` until reconciled.

## Customer Zero

The founder is Customer Zero for this council. Track whether the review was
opened, changed a decision, caught something missed, prevented work, saved time,
reduced cognitive load, or created redundant cognitive load. Repeated voluntary
use is stronger evidence than a successful demo. External release is out of
scope until internal value is demonstrated.
