# Executive Decision Brief Effectiveness 5-Whys

Date: 2026-09-19

## Defect

The Executive Council MVP passed structural validation without proving that it
improved a founder decision. Its lenses converged by construction, the report
could become stale while CI stayed green, and no supported command recorded the
founder decision or actual outcome.

## Analysis

1. Why could a structurally green review fail to improve a decision? Because
   the generator produced a general recommendation rather than one decision
   with alternatives, thresholds, and a stop rule.
2. Why did the generator produce that shape? Because the MVP acceptance gate
   measured files, schemas, and tests rather than a decision-to-outcome loop.
3. Why was the outcome loop missing? Because tracking fields were declarative
   placeholders and the CLI had no decision or outcome mutation path.
4. Why could stale evidence remain green? Because CI validated a fixed dated
   artifact without source fingerprints or current-date enforcement.
5. Evidence ends here. The root cause is an acceptance boundary that treated
   report generation as a proxy for decision usefulness; no deeper cause is
   claimed without observing three real founder decisions.

## Correction

- Immediate: preserve the historical v1 artifact and generate a schema-v2
  decision brief with one concrete decision, options, constraints, and an
  explicit no-material-disagreement state.
- Root-cause correction: validate current-date identity, source fingerprints,
  distinct lens contributions, complete execution criteria, and outcome fields;
  add `record-decision` and `record-outcome` commands.
- Recurrence guard: focused tests reject stale briefs, duplicate contributions,
  payload/render drift, outcome recording before a decision, and composite
  health scores. The continuation record requires three real decisions before
  the council framing is treated as effective.

## Remaining Evidence Gap

No founder decision outcome has been recorded yet. The correction improves the
measurement mechanism; it does not establish usefulness or customer value.
