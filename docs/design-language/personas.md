# UX Personas

Status: proposed
Issue: #27

This document defines UX personas for the factory's operator surfaces and the
products the factory helps ship. It is separate from
[`docs/public-surface-review/personas.md`](../public-surface-review/personas.md),
which contains review lenses for public artifacts.

## Evidence discipline

These personas are working hypotheses unless a statement is marked as observed
or validated. They should guide the first reference slices, then be revised from
interviews, usability sessions, device observations, support evidence, or
repeated product behavior.

Use these labels:

- **Observed:** directly seen in a session, device test, support report, or
  other traceable evidence.
- **Validated:** tested with the intended person and supported by repeatable
  evidence.
- **Assumption:** plausible but not yet tested.
- **Constraint:** imposed by safety, privacy, platform, or product policy.

Do not turn an assumption into a requirement without validation or an explicit
owner decision.

## Factory Personas

### Solo Factory Operator

**Role:** accountable owner of product delivery, approvals, and recovery.

**Jobs:**

- Understand what is happening without reading every implementation detail.
- Decide whether evidence is sufficient to proceed.
- Recover from blocked or failed work safely.
- Preserve product intent and avoid unnecessary factory work.

**Needs:** current state, next safe action, provenance, timestamps, concise
summaries, and a clear path to detail.

**Fears:** silent failure, stale status, irreversible actions, unsupported
claims, and spending attention on factory machinery instead of product value.

**Design consequences:**

- Put state, evidence, and next action above secondary metadata.
- Separate verified, proposed, blocked, failed, and unknown states.
- Make recovery and reversal visible.
- Keep the default view scannable; make investigation detail one step away.

**Evidence status:** Assumption informed by the factory North Star and current
single-operator workflow.

### Product Builder

**Role:** person implementing or reviewing a product increment across the PRD,
code, verification, simulator, device, and handoff.

**Jobs:**

- Translate a validated requirement into a small usable change.
- Preserve context while moving between implementation and evidence.
- Know what remains unverified.
- Reuse proven patterns without inheriting speculative infrastructure.

**Needs:** traceability from requirement to acceptance criterion to evidence,
low navigation overhead, clear scope, and explicit blockers.

**Fears:** stale requirements, duplicated design decisions, accidental scope
growth, and a green check that proves the wrong behavior.

**Design consequences:**

- Link work state to the current PRD and acceptance criteria.
- Keep decisions and verification evidence close to the work they explain.
- Expose deferred work instead of implying completion.
- Prefer platform capabilities and existing patterns before new abstractions.

**Evidence status:** Assumption based on the current PRD-and-verification
workflow.

### Safety and Quality Reviewer

**Role:** accountable reviewer of privacy, accessibility, correctness, and
release readiness.

**Jobs:**

- Find material risk before acceptance or publication.
- Distinguish evidence from assertion.
- Confirm that failure and fallback behavior is safe.
- Understand unresolved assumptions and their consequences.

**Needs:** provenance, edge states, negative evidence, accessible review paths,
and explicit unresolved questions.

**Fears:** false confidence, hidden data movement, inaccessible primary flows,
and ambiguous ownership of a decision.

**Design consequences:**

- Never use a single green status as a substitute for evidence.
- Make privacy, accessibility, and failure checks first-class review sections.
- Preserve the path from finding to correction to recurrence guard.
- Support keyboard, pointer, and readable touch interaction for review work.

**Evidence status:** Constraint-aligned assumption; validate against actual
review sessions.

## Product Personas

These are the current Mews & Woofs working personas. They are product users,
not operator roles.

### Kid Playful Explorer

**Context:** uses a shared iPad with a parent or an iPhone with supervision.

**Job:** make a sound, understand the playful result, and try again quickly.

**Needs:** large targets, short language, read-aloud-friendly cards, positive
uncertainty, immediate feedback, and no frightening output.

**Fears:** confusing controls, waiting without feedback, or an output that feels
scary or overly certain.

**Design consequences:**

- One primary action per screen.
- Keep essential copy short and concrete.
- Make low-confidence output redirect toward play.
- Support VoiceOver and co-use without requiring independent reading.
- Make recording, stopping, and replay state obvious.

**Evidence status:** Assumption from the active product PRD; device and
co-play validation required.

### Parent Companion and Controller

**Context:** co-uses the app, explains results, manages profiles, and checks
privacy or capability limits.

**Job:** help the child explore while maintaining trust and control.

**Needs:** clear disclosures, understandable fallback behavior, profile and
history controls, privacy explanation, and a quick route to adult context.

**Fears:** misleading interpretation, unexpected data retention, and unclear
boundaries around what the app can infer.

**Design consequences:**

- Keep honesty language visible on interpretation surfaces.
- Make privacy and capability explanations easy to reach without interrupting
  play.
- Distinguish playful output from factual detection.
- Preserve child-friendly primary surfaces while providing adult context.

**Evidence status:** Assumption plus product safety constraint; validate in
parent-child co-use sessions.

### Owner and Privacy Steward

**Context:** maintains the personal app and decides what stays on the device.

**Job:** use the product without accounts, cloud dependency, or hidden data
movement.

**Needs:** predictable local behavior, clear permission handling, reliable
fallbacks, deletion controls, and honest network/data status.

**Fears:** accidental retention, network access, data leakage, or a required
feature that silently depends on unavailable intelligence.

**Design consequences:**

- Explain permission denial and unavailable capability states.
- Make local-only and no-network behavior testable and visible where relevant.
- Preserve useful behavior without Apple Intelligence.
- Treat deletion and profile isolation as understandable user actions.

**Evidence status:** Constraint from the active product PRD and privacy posture.

## System actors, not personas

Agents, CI, simulators, and verification scripts are system actors. They need
contracts, inputs, outputs, and failure handling, but they are not substitutes
for human UX personas. Agent-facing guidance belongs in repository instructions
and acceptance criteria; the resulting product must still serve human users.

## Reference journeys

### Operator journey: queue to disposition

1. Find the current increment in the queue.
2. Understand its state and next safe action.
3. Inspect acceptance criteria and evidence.
4. Resolve, approve, defer, or escalate.
5. Leave a durable decision and recovery path.

### Product journey: co-play record to card

1. Child or parent identifies the primary record action.
2. App communicates recording state and how to stop.
3. Processing state explains that work is in progress.
4. Interpretation card presents playful output and honesty boundary.
5. User can replay, try again, or return to a profile without losing context.

Both journeys must include their failure, empty, unavailable, accessibility, and
uncertainty states before the reference slice is accepted.

## Persona-to-design mapping

| Need | Design response | Verification evidence |
|---|---|---|
| Operator needs trustworthy state | Explicit state vocabulary and linked evidence | Review checklist and evidence view |
| Builder needs preserved context | PRD-to-criterion-to-evidence links | Handoff and acceptance review |
| Reviewer needs negative evidence | Failure, privacy, accessibility, and recurrence sections | Review record and deterministic checks |
| Kid needs quick, safe play | One primary action, large targets, positive abstention | iPhone/iPad co-play review |
| Parent needs understandable boundaries | Locked disclosure and adult context | Product UI review and policy tests |
| Owner needs local trust | Permission, fallback, deletion, and network clarity | Product verification and device evidence |
