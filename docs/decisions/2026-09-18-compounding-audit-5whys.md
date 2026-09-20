# Institutional Compounding Audit 5-Whys

Evidence reviewed: `.factory/artifacts/reuse-registry.json`,
`.factory/artifacts/portfolio-archaeology/`, `scripts/ecosystem_gates.py`,
`scripts/validate-apple-distribution.py`, and the current factory test suite.

## A. Product work to reusable artifacts

1. Meaningful work was not uniformly classified because the gate covered only selected substantial paths.
2. The work-start protocol was not universal because discovery was enforced by entrypoints rather than the work contract.
3. The registry could be updated without proving a cold consumer because consumer evidence was descriptive.
4. This persisted because artifact validation checked records and paths, not immutable release/consumption transitions.
5. Root cause: reuse policy was not a single executable boundary.

Correction: retain the registry, require cold-agent discovery, validate consumer evidence, and keep unproven artifacts candidate-only.

## B. Versioning and release

1. The proportional reuse package had a version but was not released.
2. Publication was human-gated, but release state was not explicit.
3. A manifest could therefore look versioned without proving whether it was released.
4. Root cause: version and publication state were separate undocumented assumptions.

Correction: package manifests now require semantic version, source revision, explicit release state, and `publication_approved: false`; working-tree provenance cannot claim `RELEASED`.

## C. Cold-agent discovery

1. A fresh agent could rebuild a capability if it bypassed the entrypoint.
2. The registry search was not an acceptance condition for all substantial work.
3. Root cause: discovery was a helper, not a mandatory state transition.

Correction: `scripts/start-work.py` and adversarial tests require search and block deliberate duplicate builds without specialization evidence.

## D. Historical failures

1. Vorynce rejection lessons were preserved, but conversion depended on a product-specific fixture.
2. There was no general failure-to-regression contract.
3. Root cause: historical learning was stored as evidence, not enforced as a required control.

Correction: the Vorynce fixture is permanently consumed by Apple preflight tests, including orientation, purchase-disclosure, review-information, and placeholder-name checks.

## E. Safe archival and deletion

1. Candidate repositories had source paths but unknown unique knowledge and recovery state.
2. A path-preservation record was insufficient to prove recoverability.
3. Root cause: lifecycle state and preservation evidence were not coupled.

Correction: lifecycle transitions and deletion evidence are validated by `.factory/lifecycle-contract.json`; a real docketloom candidate was exercised and remains blocked before archive/deletion.

## F. Blocked versus done

1. Local implementation could finish while external reconciliation or release evidence remained unresolved.
2. Completion modeled only a narrow control-plane blocker.
3. Root cause: acceptance state was not an explicit finite set of failure/blocker states.

Correction: completion now distinguishes `DONE`, `BLOCKED_EXTERNAL`, `BLOCKED_HUMAN`, `BLOCKED_SECURITY`, `WAITING_DEPENDENCY`, and `FAILED`; adversarial tests assert every blocker has `done: false`.

## G. Ready work around blockers

1. Static lane evidence showed ready work but did not select it.
2. No deterministic scheduler boundary consumed lane state.
3. Root cause: bounded parallelism was reported, not executed.

Correction: `scripts/select-lanes.py` selects independent ready lanes, respects resource conflicts, and proves `idle_despite_ready_work=0` for the current blocked Apple portfolio.
