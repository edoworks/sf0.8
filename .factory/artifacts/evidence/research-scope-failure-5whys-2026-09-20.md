# Research Scope Failure 5-Whys

Date: 2026-09-20
Incident: delegated deep-dive stopped twice because the prompt omitted the
research topic and decision.

## Analysis

1. **Why did the research stop?** The task received no subject or decision to
   investigate.
2. **Why was the subject missing?** The delegation relied on the surrounding
   conversation instead of restating the active decision in the task prompt.
3. **Why was that unsafe?** Evidence research needs a bounded claim, audience,
   jurisdiction, cutoff, and stopping rule to select relevant sources and
   counterclaims.
4. **Why was the omission repeated?** The first failed task result was
   summarized, but the next delegation did not convert the prior context into
   an explicit research charter before retrying.
5. **Root cause supported by evidence:** the task handoff had no mechanical
   required-field check for topic and decision before dispatch.

## Correction

- Immediate correction: the retry explicitly named the audience, jurisdiction,
  decision, cutoff, source plan, and stopping rule for the Product A/sf0.7/sf0.5
  consolidation decision.
- Root-cause correction: future deep-dive delegations must include the complete
  research charter in the task prompt rather than relying on conversational
  context.
- Recurrence guard: reject or rewrite any research handoff missing the explicit
  `topic`, `decision`, `audience`, `jurisdiction`, `cutoff`, `source plan`, or
  `stopping rule` fields before dispatch.

## Evidence Of Effectiveness

The corrected retry returned a scoped result covering the three repositories,
preservation versus pilot decisions, counterevidence, unknowns, and source
boundaries. No repository mutation or external write was performed.
