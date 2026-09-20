# Experience-Quality Dogfood

Issue: [Factory: Apple-first product experience quality](https://github.com/edoworks/sf0.8/issues/32)

## Portfolio resolution

The active private product resolves through `.factory/portfolio.yaml` as
`edoworks/product-a` rather than a guessed directory. Its registered source
repository is not present in this sf0.8 checkout and no local ProductA project
was found. Product A was not rewritten and no product-specific visual claim is
made. This is an execution blocker for the requested Product A dogfood, not a
passing result.

## Product A disposition

- SpriteKit: `EVALUATE` when the registered product checkout is available; it is
  already the native game boundary and should not be replaced by a custom
  renderer.
- SwiftUI integration: `EVALUATE` only for surrounding settings/onboarding or
  platform navigation; preserve SpriteKit where direct manipulation is core.
- Animation, sound, haptics, touch, device behavior, accessibility, XCTest/
  XCUITest, performance, and visual QA: `EVALUATE` against a rendered build.
- Current evidence: simulator/device/product evidence unavailable here.

## Second product: Vorynce

Vorynce is materially different from Product A: an audio-first SwiftUI +
SwiftData productivity app targeting iOS 17, with Foundation Models as an iOS
26 progressive enhancement. Existing evidence includes 1320x2868 rendered
captures at `.../qa/screenshots/asc-v2.1/` and source-level accessibility,
fallback, audio, and UI tests.

### Design critic findings

- `KEEP`: the onboarding screenshot makes the transcript-to-task payoff legible
  and gives the completion action a large, high-contrast target.
- `KEEP`: the focus screenshot gives the timer visual priority and keeps the
  primary Stop action close to the bottom navigation.
- `REFINE`: the large unoccupied surfaces and generic Welcome/Focus Timer labels
  do not yet communicate much product personality; test a warmer, product-owned
  visual moment without adding decorative chrome.
- `REFINE`: verify the purple accent and green completion action under Increase
  Contrast, VoiceOver, and color-vision conditions; color must not carry state
  alone.
- `REMOVE_OR_REJECT`: do not add Liquid Glass, widgets, haptics, or Foundation
  Models to this surface without a user problem and a measured benefit.

### Apple capability disposition

- Foundation Models: `USE_NOW` only in Vorynce's existing iOS 26 guarded feature;
  `EVALUATE` for any new feature. The source shows compile-time, OS, and device
  availability guards plus a deterministic fallback.
- SwiftUI: `USE_NOW`; it supplies native navigation, accessibility, and layout.
- App Intents: `EVALUATE`; useful for recording or starting focus only if user
  research shows system entry points matter.
- Xcode/Instruments: `USE_NOW` for performance and energy evidence.

### Evidence boundary

The captures are rendered simulator/App Store evidence by file inspection; they
are not physical-device or empirical user evidence. Vorynce source contains
accessibility and fallback tests, but this factory increment did not rerun the
product suite or alter the product repository.

### 5-Whys for the observed test defect

1. The targeted XCUITest failed because `No tasks yet` was not found after the
   non-action transcript flow, while the journal transcript was found.
2. The test therefore reached the Tasks tab but the expected empty-state
   accessibility element was absent or the task query was not empty.
3. The available log does not distinguish a SwiftData persistence/query issue
   from an accessibility-tree or timing issue.
4. No source-only inspection can establish which runtime cause is responsible;
   the existing test has no hierarchy dump enabled for this case.
5. Evidence ends at the runtime observation. The product owner must inspect the
   captured hierarchy and persistence state before choosing a correction.

Immediate correction: preserve the failing test result and xcresult path as a
blocker rather than claiming Vorynce is green. Root-cause correction: add a
targeted hierarchy/persistence diagnostic and rerun the test in the product
repository. Recurrence guard: keep this negative-path XCUITest in the required
experience evidence set and require a green targeted run before acceptance.

## Reusable result

The factory contract generalizes across a SpriteKit game and a SwiftUI app, but
the visual findings remain product-specific. The validator and templates are
`internal-reusable`; the versioned reuse-gate package remains a candidate for
public reuse pending human approval.
