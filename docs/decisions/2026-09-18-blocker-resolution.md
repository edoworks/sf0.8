# Blocker Resolution And Empirical Validation

Issue: [Factory: Apple-first product experience quality](https://github.com/edoworks/sf0.8/issues/32)

## Product A resolution

The portfolio now records `source_of_truth:
https://github.com/edoworks/product-a.git` and `default_branch: main`.
`scripts/resolve-portfolio.py edoworks/product-a` resolves the repository
without a machine-specific checkout path. A clean checkout from that remote
contains `ProductA.xcodeproj`; `./scripts/doctor.sh && ./scripts/verify.sh`
passed with 26 unit tests and 10 UI tests, one physical-device test skipped by
design.

GitHub still reports the private repository as archived. No unarchive or
lifecycle mutation was performed. The product can be built and simulator-tested
read-only; physical validation and product continuation remain owner-authorized
actions.

## Vorynce diagnosis

The saved xcresult reported one failure on iPhone 17 Pro / iOS 26.5:
`RecordingFeedbackUITests/test_nonActionTranscript_savesJournalOnlyWithoutTask`.
The failure occurred after the Journal transcript was visible and the Tasks tab
was reachable. There were no media attachments in that original result.

Source and test evidence identified a product defect with a stale unit contract,
not a synchronization or accessibility-tree defect:

- `RecordingCapturePlan` created a fallback `TaskItem` whenever a transcript had
  no grounded action candidate.
- The UI test contract required a non-action transcript to remain journal-only.
- Unit tests and comments still asserted the older fallback-task behavior.

Correction: the domain plan now creates tasks only for grounded action
candidates; plain transcripts remain journal entries. Unit tests and comments
were updated to the current product contract. The targeted UI test passed after
the correction. Accessibility, Dynamic Type, and Reduce Motion audit suites
also passed: 6 tests, 0 failures.

The full Vorynce scheme still exceeded the time budget in an earlier run; the
relevant targeted and accessibility suites are green. This is not a claim that
the entire scheme is green.

## Before and after evidence

### Vorynce

- Before: `/tmp/vorynce-quality-before/C5B92ED6-B9EE-4FC4-ADB9-276E284CED94.png`
  shows the non-action sentence incorrectly rendered as a task.
- After: `/tmp/vorynce-quality-after/7E2E6CC7-2BF7-4698-B00B-E4694470FFD3.png`
  shows the same flow with an empty Tasks state.
- Removed: the misleading fallback task and its stale expectation.
- Added: no new UI chrome; the existing native empty state now reflects actual
  semantics.

### Product A

- Historical before: `/tmp/producta-visual-review/idle-20260916-141753-441.png`
  shows the older Talk first / Listen first control surface.
- Current simulator evidence: `/tmp/producta-quality-after/current-textless.png`
  shows the inherited reduced, creature-led, textless surface.
- The current surface passed textless, Reduce Motion, landscape, listening-state,
  and creature interaction UI tests.
- This session did not change Product A UI code, so the current Product A
  improvement cannot honestly be attributed to Issue #32. It is retained as
  evidence of a prior product reduction, not closure evidence for the factory
  increment.

## Capability dispositions

- SwiftUI: `REQUIRED` for Vorynce and Product A’s surrounding native surface;
  existing native navigation and accessibility were retained.
- Accessibility APIs: `REQUIRED`; evidence is the passing audit suites and
  product-specific accessibility labels, not checkbox completion.
- SpriteKit: `NOT_APPLICABLE` to the current Product A architecture, which is a
  SwiftUI/audio exchange rather than a SpriteKit scene. No engine was added.
- App Intents, Liquid Glass, Foundation Models additions, widgets, haptics, and
  custom visual infrastructure: `NOT_RELEVANT` or `EVALUATE` only; no new
  adoption was justified by these trials.

## Remaining gates

- Product A repository unarchive/project lifecycle action remains human-only.
- Product A physical microphone, speaker comfort, real pet response, and
  pre-literate empirical observation remain unverified.
- Product A current after evidence is simulator-only.
- Vorynce physical-device evidence and full-suite completion remain open.
- Issue #32 must remain open: only Vorynce has an observable before/after caused
  by this phase; Product A has not yet received a causal quality improvement.

## Physical-device handoff

Product A: run the exact verified commit from the clean canonical checkout on a
reachable iPhone/iPad using `docs/device-validation-runbook.md`; record touch
ergonomics, sound audibility/comfort, haptics, orientation, and real pet or
pre-literate observation separately. Do not infer these from the simulator.

Vorynce: install the corrected build on a reachable device and repeat the
non-action transcript flow, VoiceOver, Dynamic Type, Reduce Motion, audio, and
energy checks. The simulator results do not close this gate.

## Validation refresh: 2026-09-18

- Factory validation passed: 63 Python tests, ecosystem validation, lifecycle
  validation, contribution gate, and change gate.
- Product A clean canonical checkout passed `doctor.sh`, `verify.sh`, 26 unit
  tests, and 10 UI tests with one intentional skip.
- Product A physical build for commit
  `ef94f2492d3e73d98fb883320bad2902c64f3e15` built and installed on iPhone 16
  Pro Max `Ethan`; DDI services and Developer Mode were available. The first
  attempt was blocked by the device lock screen, then the unlocked rerun passed
  both `testPhysicalLaunchSurface` and `testPhysicalConversationEntry`. The
  run produced no screenshot attachments, so no visual screenshot evidence was
  claimed. Preflight evidence is in
  `docs/ci/device-checks/39C04F90-1CAA-5533-8FFD-BFB33A373880-ef94f2492d3e73d98fb883320bad2902c64f3e15-preflight.txt`.
- Product A physical result manifests are in
  `docs/ci/device-checks/39C04F90-1CAA-5533-8FFD-BFB33A373880-ef94f2492d3e73d98fb883320bad2902c64f3e15-1789748523/`
  and
  `docs/ci/device-checks/39C04F90-1CAA-5533-8FFD-BFB33A373880-ef94f2492d3e73d98fb883320bad2902c64f3e15-1789748547/`.
- Vorynce `RecordingCapturePlanTests` passed: 9 tests.
- Vorynce targeted recording, accessibility, Dynamic Type, and Reduce Motion UI
  suites passed: 7 tests.

The next action requiring a person is the manual audio and persona review on the
installed exact build. No code or lifecycle mutation is justified until that
evidence exists.
