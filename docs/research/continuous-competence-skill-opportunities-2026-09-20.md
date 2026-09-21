# Skill Opportunities From the Continuous Competence Session

Date: 2026-09-20
Status: `LOCAL_LEARNING_RECORD`
Bound issue: #50

This record captures repeatable workflow opportunities discovered while
building the mobile web and native SwiftUI experiment. It does not authorize
creating, installing, publishing, or externalizing a skill.

## Candidates

| Candidate | Observed recurrence risk | Smallest automation | Disposition |
|---|---|---|---|
| SwiftUI experiment scaffold | Generated Xcode target initially omitted an `Info.plist`; the app compiled until bundle validation. | A project generator/check that requires `GENERATE_INFOPLIST_FILE`, bundle identifier, iOS deployment target, unsigned simulator build, and a test target. | Reuse `xcodegen` locally; consider a factory skill only after a second native experiment consumer. |
| Native visual verification | SwiftUI inherited dark-mode foreground colors on a custom light canvas; unit tests and compilation did not detect it. | Build/install/launch both iPhone and iPad simulators, capture screenshots with the existing `macos-screenshot` skill, and require review under the active appearance. | Existing skill is the reusable capability; add a project-specific recurrence test, not a duplicate screenshot tool. |
| Experiment contract parity | Web and native versions duplicate the same controlled fixture and result fields. | Validate that every surface declares the same mode names, fixture defect, independent-confidence fields, and local-only boundary. | `REUSE_CANDIDATE`; requires a second real experiment consumer before extraction. |
| Artifact publication preflight | Local artifacts can be mistaken for public release candidates before Customer Zero, Rule-of-Two, provenance, and authorization gates pass. | Existing reuse/publication validators plus an explicit `LOCAL_ONLY_PENDING_HUMAN_AUTHORIZATION` state. | Reuse existing factory gates; do not create a new release service. |

## Evidence-backed Existing Skill

The existing `macos-screenshot` skill was used for both the mobile web and
native iPhone/iPad surfaces. It caught the native contrast defect that build and
unit tests missed. Its source is outside this repository at
`/Users/hello/.agents/skills/macos-screenshot`; it remains a candidate for
shareability review, not an artifact copied into this project.

## Promotion Rule

Promote a workflow into a reusable skill only when:

1. the workflow has a second real consumer;
2. the interface can be separated from this experiment's private context;
3. the recurrence guard is deterministic;
4. provenance, license, maintenance ownership, and privacy boundaries are
   recorded;
5. publication is explicitly authorized.

## Human Gate

No skill installation, public artifact release, external repository mutation,
TestFlight submission, or App Store submission occurred.
