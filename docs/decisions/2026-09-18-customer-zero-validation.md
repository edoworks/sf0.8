# Customer-Zero Validation

Date: 2026-09-18

## Result

Customer-Zero traceability passed in sf0.8: five critical outcomes map to
release criteria, all five have automated or simulator evidence paths, two also
require device evidence, three also require empirical evidence, and none are
unverified or unjustified manual.

Product A's full verification encountered one permission-recovery UI failure;
the same test passed in an isolated rerun. The full run therefore remains a
flaky-run observation, not a clean full-suite claim.

Vorynce's first targeted run exposed a real mismatch: unavailable recognition
used bundled sample text to create a task, while the current product contract
and test correctly require fallback content not to manufacture an action.

## 5-Whys: Vorynce Fallback Task

1. The unavailable-recognition journey could not find its `Continue` state.
2. The onboarding always converted the bundled fallback transcript into a task.
3. The fallback transcript is illustrative content, not evidence spoken by the
   person.
4. The onboarding path had not adopted the newer grounded-action rule already
   applied to normal capture.
5. Evidence ends at this product-boundary mismatch; no deeper cause is needed.

Immediate correction: only expose an extracted task when transcription actually
succeeded; retain the fallback transcript as a readable example.

Root-cause correction: fallback content is now explicitly non-action evidence.
Recurrence guard: the unavailable-recognition UI test asserts `Continue` and an
empty task list, while the successful deterministic sample test still asserts a
real extracted task.

## Evidence

- sf0.8 `python3 scripts/validate-automation.py`: passed with
  `UNJUSTIFIED_MANUAL=0`.
- sf0.8 test suite: 66 tests passed.
- Product A isolated permission-recovery test: passed; full verification's
  retained xcresult records the earlier failure.
- Vorynce targeted onboarding tests: 2 passed, including actionable sample and
  unavailable fallback.

Physical pet engagement, physical audio quality, accessibility traversal, and
desirability remain empirical/device claims and are not asserted by these runs.
