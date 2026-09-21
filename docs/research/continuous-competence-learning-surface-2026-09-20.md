# Continuous Competence Learning Surface

Date: 2026-09-20
Scope: question breadth, engineering education support, visual walkthroughs, and Apple Intelligence integration

## User Need

The prior spike measured one controlled defect. It did not yet function as a
useful engineering learning tool: there was no question bank, concept refresher,
reference trail, common-question surface, or worked visual path.

## Change

- Added three engineering questions covering loop bounds, binary-search invariants, and transaction boundaries.
- Added progressive hints, plain-language explanations, and reference links to each question.
- Added common questions covering complexity, transactions, testing, and debugging.
- Added visual walkthroughs for shrinking a search interval and making a failure-safe write boundary explicit.
- Added a local Apple Intelligence assist using `FoundationModels` when available, with an explicit local fallback.
- Added local result fields for task identity, hint usage, explanation reveal, and Apple Intelligence use.

## Evidence

- `xcodebuild ... test` on a concrete iOS 26.5 simulator: 3 tests passed.
- Signed physical-device build succeeded with the existing local development profile.
- Updated app installed and launched on Ethan, bundle ID `com.foculoom.competence-check-experiment`.
- The build compiled the guarded `FoundationModels` path with the iOS 26.5 SDK.

## 5-Whys Recurrence Analysis

1. Why was the requested learning experience absent? The spike had one hard-coded task and ended after defect inspection.
2. Why was the task hard-coded? The initial scope optimized for a narrow experiment instrument rather than a reusable learning surface.
3. Why did that hide the gap? The acceptance criteria checked local storage and one controlled defect, not question breadth or reference-backed recovery.
4. Why was Apple Intelligence missing? The original artifact explicitly excluded model APIs before the user requirement was captured.
5. Why could that exclusion persist? There was no product-surface contract requiring education content, references, visual examples, and an assist availability decision.

Immediate correction: add the question bank, learning library, walkthroughs, hints,
and Apple Intelligence action.

Root-cause correction: keep the learning-surface contract and tests alongside the
experiment fixture so future changes cannot silently reduce the experience to a
single prompt.

Mechanical guard: tests require at least three reference-backed tasks with three
hints and non-empty explanations. Human review is still required before claiming
learning effectiveness, recruiting participants, or publishing the experience.

## Open Questions

- Does assistance improve AI-free performance on a novel isomorphic task?
- Does reference review improve delayed recall rather than only immediate completion?
- On supported devices, does Apple Intelligence improve explanation quality enough to justify its interaction cost?
- Which additional engineering domains should be added after observing real learner requests?
