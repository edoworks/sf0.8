# Reusable Component Extraction Report

## Scope And Cutoff

Audience: Foculoom/Edoworks maintainers and the factory owner deciding extraction, registration, reuse, and release boundaries. Jurisdiction: authorized local workspace and locally discoverable factory/application repositories. Cutoff: 2026-09-20 inclusive. External publication, credentials, destructive changes, and legal/licensing acceptance were not authorized.

Decision: determine which previously submitted applications and existing factory implementations have reusable capabilities, their disposition, and the smallest repeatable prospective review gate.

Stopping rule: every locally evidenced submitted Apple application has an inventory row; the canonical registry, artifact source records, portfolio archaeology, discovery entrypoint, validators, and CI wiring have been inspected; each material candidate has a classification and disposition. Unknown remote state remains unknown.

Known facts: `.factory/portfolio.yaml` identifies two current Apple products and eleven historical Apple products; `.factory/artifacts/portfolio-archaeology/inventory.json` records the same eleven historical products and their release evidence; `.factory/artifacts/reuse-registry.json` records thirteen assessed substantial artifacts; `reusefirst` has pinned release and Customer Zero evidence.

Open questions: whether every remote repository is still submitted or archived; whether deferred source candidates have compatible licenses; whether any future independent consumer exists for Rendit, MeowCore, or CI-status evidence.

Hypotheses: the highest compounding value is factory governance, evidence, and discovery rather than product-domain code; the three historical candidates needing source review are not safe to extract yet.

Recommendations: use the existing registry and gates; search before implementation; classify every material increment; preserve product-only and historical knowledge separately; do not publish additional artifacts without human authorization and independent consumer evidence.

## Executive Answer

- **HIGH confidence:** No new public artifact should be extracted from the application code in this pass. The existing `reusefirst` artifact is already the justified public extraction and is independently tested, pinned, and dogfooded (`.factory/artifacts/records/reuse-gate.json`, primary registry record, retrieved 2026-09-20; `.factory/artifacts/evidence/reusefirst-customer-zero-dogfood.json`, primary verification record, retrieved 2026-09-20).
- **HIGH confidence:** Apple submission readiness is a valid internal shared capability. It recurs in Product A and Vorynce profiles and is exercised by the validator; it should be reused by future Apple products, not repackaged publicly (`.factory/artifacts/reuse-registry.json`, primary registry, retrieved 2026-09-20).
- **HIGH confidence:** Historical App Review rejection material is reusable knowledge/evaluation evidence, not a public package. It has provenance and a tested fixture but contains Foculoom-specific history (`.factory/artifacts/portfolio-archaeology/reuse-mining.json`, primary archaeology record, retrieved 2026-09-20).
- **MEDIUM confidence:** MeowCore persistence, deterministic state-machine testing, Rendit deterministic rendering, and CI terminal-state inspection are useful candidates, but source/license review, independent contracts, or second-consumer evidence is incomplete. Defer extraction.
- **HIGH confidence:** The prospective review gate already exists in substance: discovery CLI, proportional gate, completion disposition validation, registry validation, and CI checks (`docs/ecosystem-compounding.md`, secondary workflow documentation, retrieved 2026-09-20; `scripts/start-work.py`, `scripts/complete-work.py`, and `.github/workflows/checks.yml`, primary implementation, retrieved 2026-09-20).

## Application Inventory

| App | Repository/path | Platforms | Status and submission/release state | Primary capabilities and technologies | Existing shared dependencies/artifacts | Potential extraction areas | Evidence |
|---|---|---|---|---|---|---|---|
| Product A / Mews & Woofs | `edoworks/product-a`; local `product-a/` | iOS/iPadOS | Shelved/read-only in portfolio; never released in Apple inventory | SwiftUI, SpriteKit, adaptive play/audio | Apple preflight, rejection fixture, ReuseFirst | adaptive state machine; deterministic tests | `portfolio.yaml`, `product-a/README.md`, `product-a-candidates.json` |
| Vorynce | `foculoom/vorynce`; `/Users/hello/foculoom/products/vorynce-rebuild` | iOS | Active with release blockers; previously released/rejected | SwiftUI, SwiftData, audio, speech, FoundationModels, StoreKit | Apple preflight, rejection fixture, ReuseFirst | AI/evaluation and audio patterns; keep product-specific pending contract | `portfolio.yaml`, archaeology inventory, source/tests |
| Cat Whispers | historical sf0.7 app; `/Users/hello/sf0.7/apps/catwhispers` | iOS/iPadOS | Dormant; TestFlight valid | SwiftUI, AVFoundation, SoundAnalysis, FoundationModels, MeowCore | historical rejection knowledge | MeowCore persistence; license/source review required | portfolio historical inventory; MeowCore tests/license |
| Veilsort | `foculoom/veilsort`; `/Users/hello/foculoom/products/veilsort` | iOS | Dormant; removed from store | SwiftUI, share extension, local analysis, StoreKit, grounding/PII controls | Apple preflight eligibility; rejection knowledge | share ingestion and grounding patterns, but privacy-coupled | inventory; source files under `Sources/Shared` |
| Skiplet | `foculoom/skiplet`; `/Users/hello/foculoom/products/skiplet` | iOS | Dormant; removed from store | Godot, GDScript, iOS export | historical rejection knowledge | Godot export/plugin patterns; no contract evidence | portfolio inventory; source path |
| Edglex | `foculoom/findmyloophole-ios`; `/Users/hello/foculoom/products/edglex-rebuild` | iOS | Dormant; prepare for submission | SwiftUI, SwiftData, pure Swift BM25, FoundationModels | Apple preflight eligibility; rejection knowledge | search implementation is domain-coupled | inventory; `Sources/Search/BM25Search.swift` |
| Docketloom | `foculoom/docketloom`; `/Users/hello/foculoom/products/docketloom-rebuild` | iOS | Dormant; developer rejected | SwiftUI, SwiftData, calendar, local domain workflow | Apple preflight eligibility; rejection knowledge | UI/evaluation patterns; no independent contract | inventory; source/tests/evals |
| Jumpyloo | `foculoom/jumpyloo`; `/Users/hello/foculoom/products/jumpyloo-rebuild` | iOS | Dormant; prepare for submission | Godot, GDScript, persistence, game loop | Apple preflight eligibility; rejection knowledge | Godot persistence/game loop; no second consumer contract | inventory; source/tests |
| Legal Exception | `foculoom/legalexception`; local scaffold | iOS | Retired; developer rejected | SwiftUI/SwiftData/BM25 scaffold | historical rejection knowledge | none beyond consolidated Edglex history | inventory/reuse-mining |
| Law Gaps | `foculoom/lawgaps-ios`; local scaffold | iOS | Retired; developer rejected | legal-content scaffold | historical rejection knowledge | none beyond consolidated Edglex history | inventory/reuse-mining |
| Find My Loophole | historical only | iOS | Retired; developer rejected | predecessor to Edglex | historical rejection knowledge | none; no local source | inventory/reuse-mining |
| Bloomline | `foculoom/bloomline`; `/Users/hello/foculoom/games/bloomline` | iOS | Dormant; developer rejected | Godot game, dual orientation, asset provenance | historical rejection knowledge | asset/rendering workflow; overlaps Rendit, not yet extracted | inventory; source path |

The two current Apple entries and eleven historical entries are the authoritative submitted-app set for this report. Other local candidates in archaeology are explicitly not treated as submitted applications without equivalent release evidence.

## Findings By Claim

### Claim 1: The factory already has a canonical artifact architecture

**Evidence:** `.factory/artifacts/reuse-registry.json` is the declared source of truth and records disposition, consumers, evidence, provenance, safety, lifecycle, and maintenance fields (primary registry, retrieved 2026-09-20). `docs/ecosystem-compounding.md` defines discovery order, validation, Customer Zero, and human-only publication (secondary policy documentation, retrieved 2026-09-20). `.factory/artifacts/public-sources.json` pins Edoworks artifact revisions and migration targets (primary source map, retrieved 2026-09-20).

**Counterevidence:** the repository did not contain a separate machine-readable graph before this report, and remote artifact state was not independently queried. The registry has no external demand proof for several internal candidates.

**Implication:** do not invent a package format. Add evidence and graph records within `.factory/artifacts/`; treat the new graph as a view over the registry, not a second artifact authority.

### Claim 2: `reusefirst` is the only application/factory capability justified for public extraction now

**Evidence:** the record states Apache-2.0, no private data/secrets, independent tests, immutable `1.2.1` provenance, and verified Customer Zero across factory, Product A, Vorynce, and modeled consumer (`reuse-gate.json` and Customer Zero record, primary records, retrieved 2026-09-20). The public source map pins the exact commit/tag (primary source map, retrieved 2026-09-20).

**Counterevidence:** external problem and economic evidence remain unknown in the primitive inventory; public usefulness is proven by internal dogfood, not market adoption (`capability-primitive-inventory.json`, primary inventory, retrieved 2026-09-20).

**Implication:** maintain the released artifact; do not infer commercial demand or start a second public package. Future changes require versioned validation and human publication authority.

### Claim 3: Apple preflight is a shared internal service/contract, not product code to duplicate

**Evidence:** the registry names two product profiles, shared validator/tests, and repeated historical rejection causes (`reuse-registry.json`, primary registry; `portfolio-archaeology/reuse-mining.json`, primary archaeology, retrieved 2026-09-20). The Apple profiles contain the same evidence concerns: identity, metadata, orientation, paywall disclosure, review notes, and archive proof.

**Counterevidence:** historical apps are not all proven to consume the current validator, and Apple policy changes over time.

**Implication:** future Apple apps should consume the internal contract; historical links are eligibility/provenance only until direct integration is recorded. Keep Apple-specific policy adapters internal.

### Claim 4: Persistence, search, AI, audio, rendering, and game patterns should not be extracted wholesale

**Evidence:** MeowCore has one demonstrated consumer and incomplete source/license review; Edglex BM25 was a domain consolidation with one consumer; Product A's adaptive state machine is coupled to interaction/audio behavior; Rendit has multiple internal consumers and a deterministic probe but unresolved licensing/externalization; Vorynce/Veilsort AI and share-extension code has product privacy and domain coupling (`reuse-registry.json`, primary registry; source inventories, primary code, retrieved 2026-09-20).

**Counterevidence:** multiple products contain parallel audio, AI, persistence, onboarding, StoreKit, and test/evaluation patterns, so future rule-of-two reviews may justify narrower contracts.

**Implication:** preserve candidates and extract only after a domain-neutral API, independent tests, clean provenance, and second-consumer evidence exist. Prefer platform-native APIs and existing public libraries where equivalent.

### Claim 5: The prospective gate is present but review completion is evidence-driven rather than an app-store-style hard checklist

**Evidence:** `scripts/discover-reuse.py` searches the canonical registry; `scripts/start-work.py` blocks or routes work before implementation; `scripts/complete-work.py` delegates to completion/disposition validation; CI runs ecosystem and registry validators (`scripts/*.py`, `.github/workflows/checks.yml`, primary implementation, retrieved 2026-09-20). `validate_change_record` rejects missing or fabricated shareability dispositions (`tests/test_control_plane.py`, primary test, retrieved 2026-09-20).

**Counterevidence:** the requested checklist is not represented as one named `factory-complete` schema, and historical application archaeology still has 135 unextracted candidates (`reuse-mining.json`, primary record, retrieved 2026-09-20).

**Implication:** the smallest safe improvement is documentation and graph registration, not a parallel gate. Future work should require a disposition/evidence record through the existing completion path; a single checklist schema would be justified only if CI evidence shows omissions.

## Extraction Matrix

| Origin/application | Candidate | Classification | Disposition | Edoworks artifact or next action | Evidence status |
|---|---|---|---|---|---|
| sf0.8 + Product A | proportional reuse/shareability gate | SHARED FACTORY CAPABILITY / EDOWORKS ARTIFACT CANDIDATE | EXTRACTED, VALIDATED, PUBLIC_RELEASED | `reusefirst` v1.2.1 | independent tests, pinned source, Customer Zero |
| Product A + Vorynce + Apple history | submission readiness | SHARED SERVICE / SHARED EVALUATION | REUSED EXISTING, INTERNAL_SHARED | `apple-distribution-preflight` | two current profiles and validator evidence |
| sf0.7 Vorynce | rejection regression | SHARED EVALUATION / KNOWLEDGE_ARTIFACT | EXTRACTED, PRESERVED | `vorynce-rejection-regression` | fixture and provenance; not public code |
| Cat Whispers | MeowCore persistence | SHARED LIBRARY candidate | DEFERRED | `cat-whispers-meowcore-persistence`; source/license review | one consumer; unknown license until review |
| Product A | adaptive play state machine | APP-SPECIFIC / SHARED EVALUATION candidate | KEEP PRODUCT_ONLY | no artifact | privacy/domain/audio coupling; no second consumer |
| Product A | deterministic transition tests | SHARED EVALUATION candidate | DEFERRED | define domain-neutral contract only after second consumer | promising tests, not extracted |
| Edglex and predecessors | BM25 legal search | APP-SPECIFIC | REJECTED / KEEP HISTORICAL | `edglex-bm25-search` knowledge only | consolidated domain code; established alternatives |
| Vorynce + Veilsort | AI structured output, grounding, fallback | SHARED SERVICE candidate | DEFERRED | product-local until independent contract and privacy review | parallel implementations, no safe common core established |
| Vorynce + Grandma Storytime + others | audio capture/soundscape | SHARED SERVICE candidate | DEFERRED | inspect only when second consumer and data boundary are clear | parallel code, product/audio coupling |
| Rendit + game consumers | deterministic rendering/provenance | SHARED FACTORY CAPABILITY candidate | DEFERRED / INTERNAL PROTOTYPE | capability inventory entry; no Edoworks submission | deterministic probe; licensing and external demand unknown |
| sf0.8 + Product A | CI terminal-state evidence | SHARED FACTORY CAPABILITY candidate | DEFERRED / INTERNAL | retain recurrence evidence | provider coupling and external problem unknown |
| all historical apps | onboarding, design tokens, paywalls, screenshots | SHARED DESIGN PRIMITIVE / WORKFLOW candidates | REJECTED AS GENERIC EXTRACTIONS | retain patterns in source; use platform-native/product system | cosmetic or product-specific variation; no coherent contract |

Per-application totals, based only on materially evidenced candidates in the matrix and existing registry: Product A 3 candidates (1 extracted/reused, 2 deferred/keep); Vorynce 4 (2 reused, 2 deferred); Cat Whispers 1 (deferred); Veilsort 3 (1 reused, 2 deferred); Edglex 2 (1 reused, 1 rejected); Docketloom 1 (reused eligibility, no new extraction); Jumpyloo 1 (reused eligibility, no new extraction); Skiplet 1 (knowledge reuse, no new extraction); Legal Exception 1 (rejected/consolidated); Law Gaps 1 (rejected/consolidated); Find My Loophole 1 (rejected/consolidated); Bloomline 2 (knowledge reuse, rendering deferred). These are review candidates, not claims that every historical source was exhaustively inspected.

## Duplication Removed Or Avoided

- Consolidated Find My Loophole, Law Gaps, and Legal Exception into Edglex rather than creating multiple search artifacts.
- Centralized Apple preflight in the factory instead of duplicating product-specific readiness checks.
- Preserved Vorynce rejection causes as one regression fixture/knowledge artifact rather than copying incident text into each app.
- Avoided a second local copy of public `reusefirst`; `.factory/artifacts/public-sources.json` and validator enforce pinned canonical sourcing.
- No safe merge was justified for persistence, AI, audio, or rendering because their contracts and boundaries differ.

## Reuse Graph

Machine-readable graph: `.factory/artifacts/reuse-graph.json` (primary factory artifact, created 2026-09-20). It records application-to-artifact and artifact-to-application relationships plus uncertainty. It deliberately distinguishes historical eligibility from verified current consumption.

## Validation

Completed inspection: canonical registry, public source map, artifact records, portfolio registry, archaeology inventory/reuse mining/preservation records, product source/test manifests for the principal candidates, discovery CLI, start/completion gates, registry/ecosystem validators, and CI wiring. The report and graph contain no credentials, user data, private datasets, or external instructions.

Required local verification after recording this report: `python3 scripts/validate-reuse-registry.py`, `python3 scripts/validate-ecosystem.py`, and the focused control-plane tests. Product builds were not rerun because this pass does not modify application source and several products are read-only or externally governed.

## Factory Improvements

- Added `.factory/artifacts/reuse-graph.json` as a generated relationship view, while retaining the reuse registry as source of truth.
- Made the retrospective inventory and prospective gate decision explicit in this evidence record.
- Confirmed the existing discovery sequence: shared artifact, product capability, approved external source, then build new.
- No parallel registry, package format, installer, publication path, or automatic dependency update was created.

## Conflicts And Unknowns

- `portfolio.yaml` describes Product A as shelved/read-only while its Apple product subsection says lifecycle active; preserve both claims and treat the higher-level repository lifecycle as the authority for work permission.
- Portfolio reconciliation marks some public repositories not locally observed; absence is not deletion and remote verification was not performed.
- `reusefirst` internal usefulness is strong, but external problem, retention, economic, and payment evidence remains unknown.
- The 135 historical archaeology candidates remain unextracted; their existence is not evidence that extraction is justified.
- Existing artifact records cite issue and remote release evidence, but this report does not independently mutate or publish GitHub state.

## Decision Implications And What Would Change The Conclusion

Proceed with reuse of existing internal/public artifacts and the new graph record. Do not extract application code or publish new artifacts now. Reopen MeowCore if source/license review and a second independent local-first Swift consumer appear. Reopen adaptive-state testing if another product needs the same transition contract. Reopen Rendit if an authorized independent workflow observation confirms a repeatable job and licensing-safe boundary. Promote any internal candidate only after independent contract tests, consumer validation, provenance, and registry evidence pass. Add a hard checklist schema only if future completion records demonstrate omissions that the current validators fail to detect.

## Human-Action Queue

- Confirm any remote GitHub/App Store Connect lifecycle facts not available locally.
- Authorize any external observation, artifact publication, licensing acceptance, or upstream contribution.
- Decide whether to retain the broader Edoworks artifact collection closed; no publication is implied by this report.

## Sources

### Primary

- `.factory/portfolio.yaml` — portfolio and Apple lifecycle registry; retrieved 2026-09-20.
- `.factory/artifacts/portfolio-archaeology/inventory.json` — historical application and source evidence; retrieved 2026-09-20.
- `.factory/artifacts/reuse-registry.json` — canonical reusable-artifact registry; retrieved 2026-09-20.
- `.factory/artifacts/capability-primitive-inventory.json` — primitive maturity and uncertainty records; retrieved 2026-09-20.
- `.factory/artifacts/records/reuse-gate.json` and `.factory/artifacts/evidence/reusefirst-customer-zero-dogfood.json` — artifact contract and verification; retrieved 2026-09-20.
- `.factory/artifacts/public-sources.json` — pinned public artifact sources; retrieved 2026-09-20.
- `.factory/artifacts/portfolio-archaeology/reuse-mining.json`, `knowledge-records.json`, and `preservation-manifests.json` — retrospective extraction evidence; retrieved 2026-09-20.
- `scripts/discover-reuse.py`, `scripts/start-work.py`, `scripts/complete-work.py`, `scripts/validate-ecosystem.py`, `scripts/validate-reuse-registry.py`, `tests/test_control_plane.py`, `.github/workflows/checks.yml` — discovery, completion, validation, and recurrence guards; retrieved 2026-09-20.
- Application source/test manifests under `/Users/hello/foculoom/products`, `/Users/hello/foculoom/games`, and `/Users/hello/sf0.7/apps/catwhispers`; retrieved 2026-09-20.

### Secondary

- `docs/ecosystem-compounding.md` — lifecycle and trust-boundary policy; retrieved 2026-09-20.
- `docs/decisions/2026-09-18-ecosystem-compounding.md` — prior root-cause and gate decision; retrieved 2026-09-20.
- `product-a/README.md` — Product A scope/toolchain; retrieved 2026-09-20.

### Lead-only

- Search hits and filenames not opened as source documents.
- Unqueried remote GitHub/App Store Connect state.
- Local directory candidates not represented in the authoritative application/release records.
