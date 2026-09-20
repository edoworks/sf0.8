# Ecosystem Compounding Trial Evidence

Date: 2026-09-18

This is an end-to-end leverage trial, not a proposal for more factory
architecture. The existing portfolio registry, nested repository layout,
artifact registry, gates, and product verification paths were used as-is.

## Product Discovery Correction

The canonical product is `edoworks/product-a` in `.factory/portfolio.yaml`.
The intended local checkout is the nested `product-a/` repository, described by
its own `.factory/repo.yaml` and `AGENTS.md`. It was present and had the correct
GitHub origin. The earlier "unavailable" result came from searching
`/Users/hello/product-a` rather than resolving the registry entry relative to
the factory workspace. No hardcoded path or new discovery architecture was
needed.

## Trial 1: External Reuse On A Real Need

Need: Product A sensory-quality verification for AP-1/AP-9, including visible
launch behavior, accessibility, and screenshot evidence.

Discovery and decision:

- Apple SpriteKit: `ADOPT` the platform capability already used by the product;
  no third-party rendering framework was justified.
- Apple XCTest/XCUITest: `ADOPT` native UI automation and `XCTAttachment`
  screenshots already present in `ProductAUITests/PetNativeUITests.swift`.
- skills.sh, OpenCode skills, AGENTS.md, and agent-skill repositories: `LEARN_FROM`
  or `REJECT` for this product need; no untrusted instructions were installed.
- Swift Package Index: not evaluated because retrieval returned HTTP 403; no
  package was copied or installed.

Observed leverage:

| Measure | Result |
|---|---|
| Work avoided | No visual-QA package, screenshot harness, renderer, or custom accessibility framework was built |
| Duplication avoided | Existing XCTest/XCUITest attachments and SpriteKit APIs satisfied the need |
| Dependencies introduced | 0 |
| Maintenance burden | 0 new external dependencies; Apple platform maintenance remains existing product scope |
| Artifacts produced | 0 product artifacts; one candidate ledger with evidence and disposition |
| Verification | `product-a/scripts/verify.sh`: 8 unit tests, 3 UI tests passed |

This changed the engineering decision: build-new was rejected in favor of
existing platform capabilities.

## Trial 2: Standalone Extraction

Source: sf0.8's proportional reuse/contribution decision logic.

The generalized artifact is
`.factory/artifacts/packages/proportional-reuse-gate/`. It has independent
Python code, a test, README, Apache-2.0 license, provenance, registry record,
secrets/path validation, and a human-only publication flag.

Observed leverage:

| Measure | Result |
|---|---|
| Work avoided | A consumer can use the pure decision contract without importing sf0.8 or recreating the proportional rule |
| Duplication avoided | Product-specific policy, governance, and private context were excluded from the package |
| Dependencies introduced | 0 runtime dependencies |
| Maintenance burden | Explicit owner `sf0.8 factory maintainers`; next review 2026-10-18 |
| Artifacts produced | 1 standalone package, 1 test, README, LICENSE, PROVENANCE, registry record |
| Verification | Standalone package test passed; ecosystem validator passed |

This is publication-ready for human review, not published. No external source
code was copied.

## Trial 3: Cross-Product/Factory Reuse

Consumer: `/Users/hello/rung`, the existing public Rung product listed in the
portfolio. The consumer imported the standalone package from the factory
artifact path and evaluated a representative 9-unit decision as `BUILD_NEW`
with a recorded reason. Rung's existing 64-test suite also passed.

Observed leverage:

| Measure | Result |
|---|---|
| Boundary crossed | `sf0.8/.factory/artifacts/packages/proportional-reuse-gate/reuse_gate.py` -> Rung consumer process |
| Work avoided | Rung did not reimplement proportional search arithmetic or decision semantics |
| Duplication avoided | One shared pure contract was exercised by both factory and product contexts |
| Dependencies introduced | 0 installed dependencies; trial used a source path only |
| Maintenance burden | Low for the pure file, but distribution is not solved |
| Artifacts produced | 1 consumer result and 64 passing Rung tests |

The trial exposed a concrete but bounded defect: cross-repository consumption
currently requires a source path because the package has no selected distribution
channel. This is not silently treated as solved. Publishing a package or
choosing a shared repository requires human authorization and is out of scope.

## Ceremony Review

The gates changed decisions in all three trials: adopt native APIs, generalize
the pure contract, and reject unsafe/unavailable external candidates. The
duplicate skills.sh ledger entry was removed because it added no new evidence.
The remaining ledger records are proportional evidence, not installation
ceremony.

## What Remains Unproven

- Product A real-cat, child-comprehension, and physical-device value remain untested.
- No external artifact was adopted as executable third-party code.
- Cross-product reuse is proven at source-consumer level, not via a versioned distribution.
- No upstream contribution or public publication was authorized.
- Long-term maintenance and community feedback have not yet been observed.
