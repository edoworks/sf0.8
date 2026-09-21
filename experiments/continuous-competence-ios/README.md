# Competence Check iPhone/iPad Spike

Status: `EXPERIMENT_ARTIFACT`, local-only, issue #50.

This is a bounded SwiftUI spike for the same Customer Zero experiment as
`../continuous-competence-mobile`. It targets iPhone and iPad from one adaptive
view and stores session results locally. It is not a product, tutor,
credential, child-directed experience, or App Store submission.

## Generate and build

From this directory:

```bash
xcodegen generate
xcodebuild -project CompetenceCheck.xcodeproj \
  -scheme CompetenceCheck \
  -sdk iphonesimulator \
  -destination 'generic/platform=iOS Simulator' \
  CODE_SIGNING_ALLOWED=NO build
```

Before a physical-device attempt, use the CoreDevice authority check rather
than `xcrun xctrace list devices`:

```bash
python3 scripts/check-apple-device.py --device Ethan
```

The current spike intentionally has no development team or signing identity.
Physical installation therefore requires a human-authorized Apple development
team and signing configuration; simulator builds remain unsigned and local.

The project has no network dependencies, account flow, analytics, or payment
capability. The intervention includes an explicit Apple Intelligence assist
through Apple's on-device `FoundationModels` framework when the OS and device
make it available; it falls back to the local explanation and references when
Apple Intelligence is disabled, unavailable, or not ready. No model response is
sent to a repository-owned server.

The learning surface currently includes three software-engineering question
types, progressive hints, concept refreshers with references, common questions,
and two text-based visual walkthroughs. These are interaction hypotheses, not
evidence of tutoring effectiveness or mastery.

## Evidence boundary

Use the same control/intervention protocol as the mobile web experiment. Compare
native and web surfaces only on completion, interruption/resumption, independent
score, transfer, unprompted return, and surface-caused errors. Do not infer
native product demand from a successful simulator build.

The paired five-session protocol is recorded at
`docs/research/continuous-competence-surface-comparison-2026-09-20.md`.

TestFlight, App Store submission, publication, and external participant access
remain human-authorized operations.
