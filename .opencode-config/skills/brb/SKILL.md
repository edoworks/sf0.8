---
name: brb
description: Use when the user says "brb", "run while I am away", or asks for bounded idle-time work; execute only approved local validation, evidence, archaeology, or review-preparation lanes and stop at authority or ambiguity boundaries.
---

# BRB Bounded Work

Operate as a short, reviewable queue worker while the user is away. This is
not permission to invent work, broaden scope, or act as an unattended release
agent.

## Startup

1. Identify the active repository and read its continuation direction,
   governance, status, and canonical queue.
2. Select exactly one existing, actionable queue item. Do not create a new
   issue, product, experiment, or lane to avoid being idle.
3. Run the repository's required capability and issue preflight before
   material work.
4. State the selected item, allowed files, time budget, and stop conditions in
   the working record or progress update.

## Allowed lanes

- Read-only validators, tests, lint, and CI-status inspection.
- Metadata-only portfolio archaeology and deduplication.
- Evidence classification and report generation when the repository declares
  the output path and schema.
- Documentation consistency and review preparation.
- Local implementation in an isolated worktree only when an existing issue
  explicitly authorizes it and the change can be verified locally.

## Hard stops

Stop without attempting the action when work requires:

- Product A resumption, product verification, or release interpretation.
- Customer recruitment, interviews, child or pet observation, payment, or any
  other empirical claim.
- Publishing, App Store Connect, TestFlight, release, repository visibility,
  deletion, archival, branch push, tag, merge, or external write.
- Credentials, unapproved cloud egress, unclear ownership, or a trust-boundary
  decision.
- A missing issue, missing capability preflight, ambiguous acceptance gate, or
  a test failure whose root cause is not understood.

## Safety and budget

- Use the approved routine/small route for mechanical work.
- Work on one item at a time with a finite time and tool budget.
- Never use destructive commands, bypass flags, compound shell commands, or
  broad staging.
- Do not treat passing tests as evidence of customer value, delight, repeat
  use, learning, pet response, or release readiness.
- Preserve user changes and leave unrelated dirty paths untouched.
- Stop after the first unresolved blocker rather than retrying indefinitely.

## Completion

Before reporting completion:

1. Run the narrowest relevant verification and record its result.
2. Review changed paths and do not stage, commit, push, or publish unless the
   user separately authorizes that exact action.
3. Record evidence in the repository's canonical location when required.
4. Report `DONE`, `BLOCKED_EXTERNAL`, `BLOCKED_HUMAN`, `BLOCKED_SECURITY`,
   `WAITING_DEPENDENCY`, or `FAILED`; unresolved work is never `DONE`.
5. Send the standard completion notification, then report the notification
   status and all blockers to the user.

If no safe queue item is available, report `WAITING_DEPENDENCY` and remain
idle. Do not manufacture activity.
