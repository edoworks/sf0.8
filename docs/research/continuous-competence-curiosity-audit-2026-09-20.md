# Continuous Competence Curiosity Audit

Date: 2026-09-20
Scope: whether the learning surface provides useful help when a learner is stuck

## Strongest Claim

The current experience should let a learner request graduated hints and a clear,
plain-language explanation without immediately replacing independent reasoning.
Popular education solutions suggest reusable patterns such as short practice,
feedback, correction, and mastery-oriented checks, but this repository does not
have direct user evidence that any one pattern improves learning here.

## Evidence, Inference, Unknowns

| Category | Finding |
|---|---|
| Observation | The intervention previously asked for a defect and repair, then ended; it had no hint or explanation action. |
| Observation | Existing research records concise lessons, correction, and short practice as user-valued signals from Khan Academy and Duolingo reviews, while explicitly noting that ratings do not prove learning. |
| Inference | A progressive hint ladder and optional explanation are reasonable reusable interaction patterns for the stated stuck moment. |
| Unknown | Whether these additions improve independent transfer, explanation quality, return behavior, or willingness to pay. |
| Counterevidence | Showing the full explanation too early could reduce retrieval effort or measure recognition instead of reasoning. |

## High-Value Questions

1. Do learners request the first hint only after making a genuine attempt?
2. Does each hint reduce confusion without making the answer mechanically copyable?
3. After help, can the learner explain the mechanism on a novel isomorphic task?
4. Is the explanation understandable without imitating any named person or source?
5. Would the learner voluntarily return to use this workflow again?

## Falsifiable Test

Alternate predeclared control and intervention sessions. Compare AI-free novel-task
performance, explanation quality, confidence calibration, and delayed retest
performance. The intervention is not supported if it increases assisted completion
but does not improve independent transfer or delayed explanation relative to
control.

## Decision

**Moderate confidence:** agree with the user-reported gap and add optional,
progressive hints plus an explicit plain-language explanation. Keep the change in
the local experiment; do not present it as tutoring effectiveness or mastery.

## Root-Cause Guard

The immediate defect was a missing recovery path in the intervention UI. The
contributing design assumption was that a controlled-defect task alone would
cover both reasoning measurement and learner support. The recurrence guard is a
contract test requiring the fixture and surface to expose at least three hints,
an explanation action, and local usage fields. This does not prove educational
effectiveness; it prevents silently shipping another no-help stuck state.

## Human Gate

A human must decide whether to recruit participants, change the experiment
protocol, or promote this beyond local research. No external publication,
participant recruitment, or autonomous education claim is authorized here.
