# Production Readiness Audit

Status: current audit, 2026-09-16. Scope: `sf0.8` and nested `product-a`.
This is the single prioritized backlog after this audit.

Authority: `product-a/docs/PRD.md` -> `product-a/docs/device-validation-runbook.md`
-> this backlog and linked issues -> implementation -> tests/evidence -> human
release decision. Historical issue status never overrides this chain.

## Verdict

### sf0.8

**PARTIAL, not production-ready. HIGH confidence.** The repository provides a
small Git/YAML/Markdown policy layer, deterministic routing, disposable telemetry,
lifecycle/public-surface checks, recovery evidence, and a tested safety-kernel
prototype. It has no integrated executor, host-enforced sandbox, credential
broker, externally protected audit, or governed archive/TestFlight path. The
kernel explicitly authorizes and records; it does not safely execute effects.

### Product A

**NOT READY FOR INTERNAL TESTFLIGHT. HIGH confidence.** The app has a minimal
cat-first surface, explicit Talk/Listen actions, bounded capture, local
deterministic Pet Voice, cat-only classification, cautious copy, local deletable
history, and lifecycle cleanup. `./scripts/doctor.sh && ./scripts/verify.sh`
passed locally on 2026-09-16 with 23 unit and 11 UI tests; root safety/lifecycle
checks passed with 31 tests. These prove deterministic seams, not genuine
`PET <-> APP <-> HUMAN` communication. Device evidence proves entry and a
near-silence diagnostic only. Audio quality/isolation, household listening,
accessibility inspection, specialist review, and repeat-use value remain open.

## Current Truth

| Capability | Classification | Evidence and limitation |
|---|---|---|
| Product contract/claims | WORKING | PRD and safety policy reject literal translation, medical/welfare, cloud, and raw-audio claims; tests pass. |
| Two-way exchange | PARTIAL | Reducer/fake UI cover both directions; real pet capture and response are unproven. |
| Listen | PARTIAL | Finite window, candidate/post-roll, bounded collector, cat classifier, abstention; no household capture evidence. |
| Talk | PARTIAL | Human input drives local Pet Voice and pet wait; audibility, isolation, comfort, and usefulness are unproven. |
| Expressive pet | PARTIAL | Deterministic avatar/performance vocabulary exists; accessibility and comprehension are unsigned. |
| Privacy/runtime dependency | PARTIAL | Source shows no network/raw-audio path and empty manifest; archive inspection is open. |
| Persistence/relaunch | PARTIAL | Atomic JSON, corruption backup, deletion tests; upgrade/migration lacks current end-to-end evidence. |
| Product CI | PARTIAL | Serial self-hosted simulator workflow and local verify pass; no release/upload workflow. |
| Accessibility | PARTIAL | Labels, targets, Reduce Motion code, Dynamic Type-capable text styles, and simulator tests exist; VoiceOver, large-content, and iPad review is open. |
| Factory authorization | WORKING as prototype | 31 tests cover scope, expiry, budgets, delegation, audit tamper detection, and Docker command shape. |
| Factory effects/isolation | MISSING | Kernel does not execute; Docker remains a trusted dependency, not independent isolation. |
| Factory telemetry | PARTIAL | SQLite records runs/costs; shell SQL interpolation and lack of authenticated attribution limit trust. |
| Factory routing | WORKING | Two deterministic routes; no evidence justifies learned routing. |

## Component Disposition

- **KEEP:** Git-visible PRD/decisions/handoff, `AGENTS.md`, deterministic
  verification, lifecycle checks, simple routing, tiny ledger, recovery scripts,
  and safety policy as a prototype.
- **MERGE:** device runbook, review governance, handoff, and issue evidence into
  the release record defined below. Do not add a dashboard.
- **REPLACE-WITH-NATIVE:** use Xcode/Apple tooling and one trusted CI/TestFlight
  path for archive/upload. Trigger: the demonstrated missing release path.
- **ARCHIVE:** learned routing/budgets, workspace MCP, vector DB, knowledge
  graph, web dashboard, publication automation, and public self-hosted runner
  expansion. The design review explicitly defers them.
- **DELETE:** none from the current dirty checkout without dependency proof.
  Do not implement historical speculative abstractions.

## Single Prioritized Backlog

Every item is independently verifiable. Suggested roles are not authorization.

### P0: Internal TestFlight blockers

#### P0-1 PRODUCT A: exact release candidate and preflight (#30)

- **Problem/evidence:** No archive, signing, beta metadata, crash/feedback path,
  or upload evidence exists; the runbook says these gates are open.
- **Desired behavior/scope:** One clean exact artifact produces a governed archive,
  privacy/metadata inspection, and reproducible internal upload record.
- **Non-goals:** External beta, App Store release, analytics, cloud services.
- **Acceptance:** Clean archive succeeds; every gate row has linked evidence;
  processing succeeds; owner approval is last.
- **Verification:** `doctor.sh`, `verify.sh`, archive output, processing result,
  review record, metadata/privacy inspection.
- **Dependencies:** P0-2 through P0-5. **Priority:** P0. **Owner:** release owner.

#### P0-2 PRODUCT A: real audio lifecycle and bounded listening (#29)

- **Problem/evidence:** Humans cannot predict pet vocalization. Exact-device
  entry passed, but RMS 0.0004/peak 0.0013 had no controlled stimulus; audio
  audibility, isolation, route behavior, and household detection remain open.
- **Desired behavior/scope:** Finite unmistakable listening, short relevant
  retention, environmental discard, honest abstention, safe permission,
  interruption, route, background, cancellation, timeout, and termination paths;
  Talk is audible and does not self-trigger.
- **Non-goals:** Ambient surveillance, raw-audio history, cloud AI, hidden
  automatic mode, unsupported species.
- **Acceptance:** Exact-device matrix records controlled speech/pet-like/noise
  outcomes, route/interruption behavior, comfort, retention, and failure recovery.
- **Verification:** Device runs, manual audio log, lifecycle tests, source/privacy
  inspection. **Dependencies:** clean exact artifact/device. **Priority:** P0.
  **Owner:** audio/reliability.

#### P0-3 PRODUCT A: accessibility and adaptive layout (#19, #20)

- **Problem/evidence:** Labels and simulator assertions are not VoiceOver,
  Dynamic Type, Reduce Motion, or iPad sign-off.
- **Desired behavior/scope:** Core loop is operable and understandable across
  VoiceOver, large text, reduced motion, portrait/landscape, and touch-only use.
- **Non-goals:** Settings-heavy accessibility machinery.
- **Acceptance:** No clipping, unreachable action, or ambiguous critical state;
  evidence covers listening, uncertainty, denial, deletion, and timeout.
- **Verification:** Inspector/VoiceOver session, annotated current-artifact
  screenshots, targeted UI smoke tests. **Dependencies:** exact artifact.
  **Priority:** P0. **Owner:** accessibility/art/editorial.

#### P0-4 PRODUCT A: current-artifact persona and specialist review (#14, #17)

- **Problem/evidence:** Child/Parent comprehension, character quality, safe copy,
  and parent/privacy boundary lack current signed review.
- **Desired behavior/scope:** Child understands both actions and uncertainty;
  parent understands permission/privacy/deletion; sensory performance carries
  state without conventional chrome.
- **Non-goals:** New screens/assets to manufacture a passing review.
- **Acceptance:** Child, Parent, Audio, Art, Editorial, Safety, and Board records
  all say `ship`, with evidence/open risks; owner is last.
- **Verification:** `scripts/check-review-gates.sh` on the current review record.
  **Dependencies:** P0-2, P0-3. **Priority:** P0. **Owner:** review board.

#### P0-5 PRODUCT A: migration, privacy, and failure inspection (#2)

- **Problem/evidence:** Store corruption/deletion are unit-tested, but no current
  upgrade/migration, relaunch, archive, or complete privacy inspection exists.
- **Desired behavior/scope:** Fresh install, relaunch, upgrade, missing/corrupt
  state, cancellation, and deletion fail safely with no raw audio retention.
- **Non-goals:** Accounts, sync, analytics, server recovery.
- **Acceptance:** Install/relaunch/upgrade/delete matrix passes; archive has no raw
  audio/network capability; privacy strings match.
- **Verification:** Seeded-state runs, archive manifest, source/policy checks,
  deletion inspection. **Dependencies:** P0-1. **Priority:** P0. **Owner:** privacy/reliability.

### P1: External TestFlight

#### P1-1 CROSS-CUTTING: real-pet repeat-use and two-way validation (#6, product-a #2)

- **Problem/evidence:** Repository analysis cannot answer whether people perceive
  a real exchange, understand the actions, or return; no current real-pet session
  exists.
- **Desired behavior/scope:** Supervised users naturally attempt another turn and
  describe a playful pet/app/human relationship without translation belief.
- **Non-goals:** Statistical market claims or literal classifier accuracy.
- **Acceptance:** Observations, failures, and decision are recorded; observed
  defects become bounded issues.
- **Verification:** Exact-build human/pet sessions and decision record.
  **Dependencies:** internal TestFlight. **Priority:** P1. **Owner:** product owner.

#### P1-2 FACTORY: one release evidence path

- **TRIGGER:** P0-1 demonstrates the current factory lacks governed archive/upload
  evidence. **Problem/evidence:** Release facts are scattered across scripts,
  handoff, and issue comments.
- **Desired behavior/scope:** One forge-visible record binds exact HEAD, checks,
  artifact, reviewers, and owner decision, using Xcode/Apple-native capability.
- **Non-goals:** Dashboard, autonomous upload agent, new protocol.
- **Acceptance:** A second operator can reproduce the record from Git without
  release credentials in ordinary verification.
- **Verification:** Clean-checkout rehearsal and evidence review.
  **Dependencies:** P0-1. **Priority:** P1. **Owner:** factory/release.

### P2: App Store candidate and hygiene

#### P2-1 PRODUCT A: publication identity/legal/privacy (#21)

- **Problem/evidence:** Bundle ID remains `com.foculoom.ProductA`; portfolio lists
  identity, IP, history, and privacy blockers.
- **Desired behavior/scope:** Owner-approved identity, rights, metadata, and
  privacy posture are consistent before public release.
- **Non-goals:** Making the repo public in this audit.
- **Acceptance:** Approved identity/rights/privacy evidence and clean public scan.
  **Verification:** Archive metadata and publication preflight. **Dependencies:**
  P1-1/owner. **Priority:** P2. **Owner:** owner/legal/privacy.

#### P2-2 FACTORY: preserve safety-kernel prototype boundary (#12, #15)

- **Problem/evidence:** Tests pass, but `TRUST_BOUNDARIES.md` explicitly says
  host enforcement, credential brokering, and immutable audit are absent.
- **Desired behavior/scope:** No external production action uses this prototype
  without independently enforced controls and complete evaluation.
- **Non-goals:** Building the autonomous runtime now.
- **Acceptance:** All issue/release records retain the disclaimer; no unqualified
  authorization claim. **Verification:** Source/doc review and safety tests.
  **Dependencies:** none. **Priority:** P2. **Owner:** trust reviewer.

#### P2-3 FACTORY: lifecycle/portfolio consistency (#4, #7, #10)

- **Problem/evidence:** Open hygiene work can compete with shipping; lifecycle
  validation already proves sf0.8 is the sole active factory.
- **Desired behavior/scope:** One portfolio state, no revived legacy work, and no
  permission optimization before product evidence.
- **Non-goals:** Dashboard, learned routing, portfolio construction.
- **Acceptance:** Existing validator passes and roadmap/issues show one order.
  **Verification:** `python3 scripts/validate-lifecycle.py`, issue audit, diff.
  **Dependencies:** product outcomes. **Priority:** P2. **Owner:** maintainer.

### P3: Deferred

Product Review Lab (#26), generated/personalized voice, extra species, vision,
Foundation Models, accounts, cloud, analytics, Siri, Shortcuts, Watch, sharing,
gamification, semantic search, and runtime generative services. Also deferred:
learned routing/budgets, workspace MCP, vector/knowledge systems, web dashboard,
autonomous publication, and public self-hosted runner expansion. Each needs a
new demonstrated trigger.

## Issue Reconciliation

- **KEEP/UPDATE:** Product A #30, #29, #19, #20, #17, #2, #21 and sf0.8 #6,
  #12, #15, #4, #7, #10. Their scopes map above; historical comments are not
  requirements.
- **MERGED/CLOSED:** Product A #27 and #16 were closed as duplicate audio/
  reliability tracking and are represented by P0-2/#29. Product A #26 was
  closed as speculative Review Lab work and remains P3. Product A #19 and #20
  remain separate open review issues but are represented together by P0-3; #17
  remains open and is represented by P0-4. Factory #13 was closed after its
  Docker adapter scope and verification were completed; parent #12 remains open
  for production trust-boundary gaps.
- **IMPLEMENTED, NOT ACCEPTED:** Product A #19 has a Dynamic Type-capable
  implementation and simulator evidence, but remains open for physical
  VoiceOver, large-content, Reduce Motion, and adaptive-layout inspection.
- **SUPERSEDE:** Product A #14 as an active planning map with this backlog;
  retain its history until remaining children are closed or folded into P0.
- **CLOSE/ARCHIVE:** No issue is closed by this audit because closure requires
  implementation and verification evidence. Earlier obsolete concepts are
  already closed in Product A; do not reopen them. Factory open maps are hygiene,
  not shipping authority.
- **NO NEW FEATURE ISSUE:** No issue is created for automatic listening or
  generative assets until P0-2 produces a specific failure and bounded remedy.

## Critical Path

1. Freeze a clean exact Product A revision.
2. In parallel, run P0-2 device audio/lifecycle and P0-3 accessibility/layout.
3. Run P0-4 persona/specialist/Board review, then P0-5 migration/privacy.
4. Complete P0-1 archive and internal TestFlight upload: **Internal TestFlight**.
5. Run P1-1 real-pet repeat-use; fix only observed P0/P1 defects.
6. Complete P1-2 evidence-path consolidation, then P2-1 identity/legal/privacy
   and owner approval: **App Store candidate**.

No factory architecture work belongs on the internal path unless P0-1 exposes a
specific missing control that existing Xcode/CI/forge capabilities cannot solve.

## Validation Experiments

| Experiment | HYPOTHESIS | METHOD | SIGNAL | FAILURE CONDITION | DECISION |
|---|---|---|---|---|---|
| Talk vs Listen | Users understand two directions without tutorial. | Observe first-use sessions. | Unprompted correct action. | Repeated confusion/mode hunting. | Keep, revise, or simplify entry. |
| Bounded passive listening | Finite listening improves capture without unacceptable false triggers. | Compare controlled pet-like, speech, and noise sessions. | Relevant capture, abstention, latency, comfort. | Ambient-feeling state or no improvement. | Tune or defer. |
| Expressive surface | Deterministic sensory states communicate before prose. | Child/Parent review of key states. | Correct state and next action. | Explanatory text required or false certainty. | Retain, revise, or cut. |
| Curated sounds | Small reviewed vocabulary is fun and comfortable. | Audio review and household listening. | Comfort, recognizability, repeat desire, no self-trigger. | Harsh/cartoonish/no value. | Keep, curate, or remove. |
| Two-way exchange | Users perceive pet/app/human exchange, not recorder/result. | Observe complete Talk and Listen turns with real pet. | Another turn and relationship description. | Recorder/soundboard perception. | Preserve, revise, or cut. |
| Repeat use | Minimal loop earns another exchange. | Internal/external TestFlight observation/diary. | Voluntary return and repeat turns. | No return, confusion, or pet avoidance. | Fix, defer, or stop. |

## Factory Change Gate

Any future factory proposal must name a **TRIGGER** from a Product A release
failure, production requirement, cost/safety/privacy problem, or repeated measured
friction at least three times. It must show a simpler/native alternative, benefit,
and verification. Without that, it is P3 and deferred.

## Confidence

- **HIGH:** claim boundary, local/no-network source posture, deterministic tests,
  safety-kernel limits, and absence of a release upload path.
- **MEDIUM:** bounded collector/lifecycle design is directionally suitable, but
  physical route/interruption/persistence behavior is incomplete.
- **LOW:** pet response usefulness, sound delight, comprehension, two-way
  perception, repeat use, and passive-listening value. Only real users/pets can
  answer these.

Existing 5-Whys records remain canonical for prior verification, disk-space,
storage-race, device, and simulator failures. This audit does not invent a new
incident or claim documentation fixed those defects.
