# Continuous Human Competence Artifact Decomposition

Status: `EXPERIMENT_ARTIFACT_LOCAL_ONLY_PENDING_HUMAN_AUTHORIZATION`
Bound issue: #50
Decision context: mobile-first Customer Zero experiment

## Scope

The intended reusable surface is not an app or a model integration. It is a
small set of independently testable experiment artifacts. The factory's
canonical public-artifact source is `edoworks/artifacts`, but publication is
blocked until Customer Zero evidence, independent interfaces, provenance,
tests, maintenance ownership, and explicit owner approval exist.

## Proposed Artifact Units

| Artifact | Purpose | Initial disposition | Evidence needed before sharing |
|---|---|---|---|
| Claim/evidence dossier | Preserve source provenance, claim ratings, counterevidence, and decision rule | `KNOWLEDGE_ARTIFACT` | Research review and freshness check; not a package |
| Mobile self-pass protocol | Run a 10-minute independent-recall and AI-verification session on a phone | `PRODUCT_ONLY` initially | One Customer Zero feasibility result, then an independent second consumer |
| Defect fixture format | Represent controlled plausible AI defects, expected repair, explanation rubric, and analogous transfer item | `REUSE_CANDIDATE` | At least two real experiment consumers and deterministic validation |
| Session result schema | Record independent score, assisted score, confidence, detection, latency, retention, adherence, and surface friction | `REUSE_CANDIDATE` | Two independent users/workflows with privacy review; do not merge into child schema prematurely |
| Delivery adapter contract | Describe mobile web/chat/native surfaces without coupling learning logic to one vendor | `REUSE_CANDIDATE` | Demonstrated surface difference in completion, resumption, or retention |
| Mobile delivery implementation | Actual app, plugin, skill, or PWA | `EXPERIMENT_ARTIFACT_LOCAL_ONLY` | Surface comparison and Customer Zero evidence; no release or product inference |
| Visual verification skill | Capture and inspect rendered macOS/iOS output instead of trusting compilation | `INTERNAL_REUSABLE_CANDIDATE` | Used on multiple Foculoom experiment surfaces, with recurrence evidence and owner-approved shareability review |

Implemented local vertical slice: `experiments/continuous-competence-mobile/`.
It contains one controlled fixture, `CONTROL` and `INTERVENTION` modes,
confidence capture, local-only result storage, JSON export, a responsive mobile
layout, and an installable/offline-capable web-app shell for phone/iPad use. It
is an experiment artifact, not evidence that a native mobile app is the correct
product surface.

Implemented native spike: `experiments/continuous-competence-ios/`. It is a
shared SwiftUI iPhone/iPad target with local persistence and the same control/
intervention contract. It passed unsigned simulator build and unit tests, with
visual captures on iPhone 17 Pro and iPad Pro 11-inch. It remains local-only.

## Separation Rules

- Content fixtures must not contain private source code, employer information,
  child identity, or model credentials.
- The learning protocol must work without a model integration; pre-authored
  outputs are preferred for controlled experiments.
- Independent performance must remain distinguishable from AI-assisted output.
- A mobile surface is an adapter, not the learning engine.
- A public artifact cannot contain the private factory dossier, participant
  records, or unpublished product strategy.
- No artifact is called a platform merely because it has an API.

## Publication Gate

Publication to `edoworks/artifacts` is not authorized by this decomposition.
Before any release, the artifact must have:

1. a narrow independent interface;
2. private-data and secret exclusion;
3. provenance and license review;
4. deterministic tests and validation;
5. a named maintenance owner;
6. Customer Zero behavior evidence;
7. a second real consumer under the Rule of Two;
8. explicit owner approval for publication and release.

The current state is therefore local research and experiment preparation, not a
shareable release.

The visual verification candidate currently points to the existing
`macos-screenshot` skill at `/Users/hello/.agents/skills/macos-screenshot`.
This session used it for both the mobile web surface and the native iPhone
surface, and it caught a native contrast defect. The skill should be reviewed
for a future `edoworks/artifacts` release only through the normal provenance,
license, maintenance-owner, second-consumer, and publication-authorization
gates; it is not copied or published here.

## Delivery Research Scope

Audience: busy adult software engineers who use AI and need independent
competence maintenance; secondary audience is the adult parent-side workflow.

Jurisdiction: no legal or regulated deployment; initial research is local and
adult-only.

Decision: determine whether a mobile-first independent-recall plus AI-
verification loop produces measurable benefit and repeat behavior, and whether
the reusable asset is an experiment protocol or a product surface.

Cutoff: 2026-09-20.

Surfaces compared: responsive mobile web/static flow, existing mobile chat,
skill/prompt package, native iOS, and vendor plugin/integration.

Stopping rule: stop building and retain only local research if the self-pass
cannot be completed on mobile, if the intervention has no independent or
delayed-retention advantage, if users do not return, or if no artifact has a
second consumer.

## Current Recommendation

Use the existing mobile chat or a static mobile flow for the Customer Zero
self-pass. Do not build a native app or publish a package yet. The first
shareable candidate, if evidence warrants one, is likely the defect fixture and
result schema rather than a user-facing app.
