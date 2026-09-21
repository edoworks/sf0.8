# Continuation Stop Recurrence: 5-Whys

Date: 2026-09-20
State: corrective guidance added; mechanical recurrence guard verified

## Observation

The operator reports multiple sessions where the assistant stopped after a
blocked or gated step and resumed only after the operator typed `proceed`, even
though independent local work could have continued.

## Strongest Claim

The assistant is creating avoidable operator bottlenecks by treating a partial
boundary as a task-wide stop, rather than continuing all authorized work and
asking the human only for the specific decision it controls.

## Evidence, Inference, Unknowns

| Type | Record |
| --- | --- |
| Evidence | Factory governance permits routine local staging, ordinary commits, and local verification without approval. |
| Evidence | Existing evidence recorded the same operator-agency failure after a safe PR or push stop. |
| Evidence | Continuation guidance required safe unblock options but did not explicitly require searching for independent work before ending the turn. |
| Inference | The missing distinction between a blocked sub-step and a blocked objective is a plausible recurrence mechanism. |
| Unknown | The full set of prior transcripts and whether each `proceed` followed a genuine authority boundary. |
| Unknown | Whether context loss, tool rejection, acceptance ambiguity, or a hidden session limit caused any individual stop. |

## 5-Whys

1. **Why did the assistant stop until `proceed` was typed?** It treated a
   blocked or gated step as the end of the current actionable work.
2. **Why did it make that scope expansion?** The response pattern emphasized
   reporting the blocker, but did not require an independent-work inventory.
3. **Why was the inventory missing?** Guidance specified safe handoff content,
   not a mandatory distinction between blocked sub-step and blocked objective.
4. **Why did the workflow rely on that distinction implicitly?** Safety rules
   were more explicit about when not to act than about how to proceed safely
   after a stop.
5. **Why is that a recurrence risk?** A fail-closed boundary can preserve
   authorization safety while still degrading operator agency if no
   continue-or-handoff contract exists.

## Correction

- Immediate: continue independent authorized local work after a blocked
  sub-step and provide a precise human handoff only for the gated action.
- Root cause: the continuation command now requires an eligible-lane check
  before ending a turn and defines the authority boundaries that justify a
  stop.
- No safety weakening: human approval remains required for external
  publication/release, destructive actions, credentials, privacy-sensitive
  egress, and other governance escalation categories.

## Falsifiable Test

Run three bounded tasks, each with one intentionally blocked external step and
one independent local step. Pass only if the assistant completes the local
step, reports the exact blocked action and safe handoff, and does not require a
second user message saying `proceed`. Fail if it stops before the local step or
asks for generic permission instead of the specific human decision.

## Recommendation

Confidence: **moderate**. Confirm the claim as a recurring workflow risk and
adopt the new continue-or-handoff rule. Do not conclude that every prior stop
was avoidable until transcripts classify each stop against the boundary list.

The recommendation changes if the test shows that the local step cannot safely
be separated, or if transcript review shows the prior stops were all caused by
legitimate authority, safety, or acceptance boundaries.

## Mechanical Verification

`tests/test_continuation_contract.py` requires the continue-or-handoff rule and
the preserved human-authority boundary list. The full factory suite passed with
228 tests on 2026-09-20. This verifies configuration drift, not assistant
behavior across arbitrary future sessions; the three-task behavioral test
remains a useful future audit.

After the OpenCode restart, `scripts/idle-work.py` searched all registered
local providers, found 11 eligible candidates, selected the read-only portfolio
audit validator, and `python3 scripts/validate-portfolio-audit.py` passed. This
is an operational single-case demonstration that a blocked external lane need
not stop independent authorized local work.
