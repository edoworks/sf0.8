# Apple Platform, Intelligence, Safety, And Privacy

Issue: [Apple intelligence, child safety, and privacy](https://github.com/edoworks/sf0.8/issues/137)

Cutoff and retrieval date: `2026-09-23`

## Maturity Vocabulary

- **CURRENTLY AVAILABLE**: documented in a publicly released SDK/OS at cutoff.
- **BETA / PRE-RELEASE**: documented only for a beta SDK/OS or beta service.
- **ANNOUNCED**: Apple has described it, but production availability is not established.
- **SPECULATIVE**: no current Apple contract was found.

Apple's release page records Xcode 27 and iOS/iPadOS 27.0 as released on
`2026-09-14`; iOS 27 APIs below are therefore current, not merely WWDC
announcements [A18-A19]. Availability remains device, language, region, storage,
and settings dependent [A11].

## Capability Matrix

| Capability | Status at cutoff | Documented availability | Relevant fact | Product disposition |
|---|---|---|---|---|
| `FoundationModels` | CURRENTLY AVAILABLE | iOS/iPadOS/macOS/visionOS 26+ | Unified sessions, guided generation, tools, and Apple on-device model [A1-A4] | `EVALUATE_AFTER_LEVEL_2` |
| `SystemLanguageModel` | CURRENTLY AVAILABLE | iOS/iPadOS/macOS/visionOS 26+ | On-device; availability must be checked; OS updates can change model version [A4] | Optional Level 3 provider |
| `LanguageModelSession` | CURRENTLY AVAILABLE | iOS/iPadOS/macOS/visionOS 26+; watchOS 27+ | Stateful context, transcript, structured responses, prewarm, usage [A1-A2] | Adapter boundary only |
| `LanguageModel` protocol | CURRENTLY AVAILABLE | iOS/iPadOS/macOS/visionOS/watchOS 27+ | Public provider abstraction with capabilities and executor [A5] | Use if Level 3 is justified |
| `@Generable`, `@Guide` | CURRENTLY AVAILABLE | 26+ | Constrain output structure and values [A1-A3] | Proposal DTOs only; not gameplay proof |
| `GenerationSchema` | CURRENTLY AVAILABLE | 26+ | Deterministically constrains output format [A1] | Schema transport; validate semantics again |
| `DynamicGenerationSchema` | CURRENTLY AVAILABLE | 26+ | Runtime schema construction [A1] | Avoid initially; static versioned schema is safer |
| `Tool` | CURRENTLY AVAILABLE | 26+ | Model can call app code; tools may have side effects [A1-A3] | Read-only catalog lookup only, if ever |
| `GenerationOptions` | CURRENTLY AVAILABLE | 26+ | Sampling, temperature, response limit, tool mode [A1] | Version and evaluate; never defines rules |
| Dynamic instructions/profile APIs | CURRENTLY AVAILABLE | 27+ | Runtime switching among model, instructions, tools, temperature, and reasoning [A1] | Not needed for first AI experiment |
| Text and image attachments | CURRENTLY AVAILABLE | Current Foundation Models documentation | Multimodal text/image prompting and classification [A1] | `NOT_RELEVANT` to run planning |
| `PrivateCloudComputeLanguageModel` | CURRENTLY AVAILABLE, ENTITLEMENT-GATED | iOS/iPadOS/macOS/visionOS/watchOS 27+ | 32K context, reasoning, network, daily quotas, eligible-device requirement [A6] | `REJECT_FOR_V1`; no gameplay need |
| Core AI | CURRENTLY AVAILABLE | Apple platforms 27+ | Runs exported `.aimodel` models across Apple silicon [A7-A8] | `DEFER`; bundle/battery/performance cost unearned |
| Core ML | CURRENTLY AVAILABLE | Broad existing support | On-device prediction and model personalization [A9] | Possible later small classifier, but deterministic statistics are simpler |
| MLX Swift | CURRENT OPEN-SOURCE PROJECT | Package-specific | Swift API for MLX [A10] | Not a Foundation Models provider contract; reject unless a measured model need appears |
| Alternate server providers | CURRENTLY POSSIBLE | `LanguageModel` on 27+ | Custom model/provider can bridge through an executor [A5] | Architecture seam only; no provider integration |
| A model that safely controls physics | SPECULATIVE / UNSUPPORTED | None | No Apple API guarantees playability, fairness, child appropriateness, or deterministic physics | Forbidden by constitution |

## Confirmed Foundation Models Constraints

### Availability And Hardware

`SystemLanguageModel.default.availability` distinguishes unavailable devices and
models not ready for use. The app must not direct a child to enable Apple
Intelligence to obtain core gameplay [A2-A4]. Apple's current support page lists
eligible iPhones beginning with iPhone 15 Pro/Pro Max and iPhone 16 families,
supported iPads including M1-or-later models and iPad mini A17 Pro, and M1-or-
later Macs. Requirements vary and Apple can change them [A11].

**Requirement:** unsupported, disabled, downloading, storage-constrained,
language-ineligible, and region-ineligible states all resolve to the same
excellent deterministic game, not a degraded prompt or upsell.

### Offline, Context, And Latency

- The on-device model works offline; the documented context is 4096 tokens per
  session [A6, A21].
- PCC documents 32K context, stronger reasoning, daily quotas, and a required
  network connection. Apple advises on-device evaluation first [A6].
- Apple documents prewarming and Instruments measurements, but no universal
  latency bound. Latency, thermal load, memory, and battery use are `UNKNOWN`
  until measured on floor devices.
- AI must therefore run outside active gameplay, preferably between sessions,
  with a hard deadline. Missing the deadline selects a cached deterministic plan.

### Structured Output Is Not Semantic Safety

`@Generable`, guides, `GenerationSchema`, and `DynamicGenerationSchema` can make
the response fit a type [A1-A3]. They do not establish that:

- obstacle combinations are possible;
- reaction windows are fair;
- rewards fit economy limits;
- generated text is age appropriate;
- a plan is novel rather than superficially different; or
- output respects the game constitution.

The engine must perform independent allow-list, bounds, graph, difficulty,
economy, safety, and simulation checks.

### Tools

Apple's `Tool` protocol can gather data or perform side effects [A1]. The game
must expose only read-only tools such as `listEligibleChunks` or
`summarizePlayerModel`. It must never expose spawn, currency, purchase, save,
achievement, network, notification, or rule-mutation tools. Model tool output is
still untrusted.

### Apple's Dynamic Game Sample

Apple's WWDC25 sample generates character dialogue and structured customer
encounters, uses tool calling, checks output against blocked terms, resets the
session on rejection, and supplies a fixed fallback [A3]. This establishes that
Apple demonstrates game generation. It does **not** establish player enjoyment,
child suitability, deterministic playability, or permission to generate runtime
rules. Foculoom should learn from the fallback and typed boundary, not copy the
dialogue feature.

### Safety

Apple documents model guardrails for input and output while explicitly warning
that contextual harms can bypass built-in layers and require app-specific safety
[A20]. Refusals and guardrail errors are normal failure modes. For a child game:

- no child enters free-form prompts;
- no AI dialogue is in the first commercial scope;
- generated identifiers must resolve to age-reviewed authored components;
- fixed authored copy handles all rejection and unavailable states;
- generated text, if ever introduced, requires a separate child-safety case and
  cannot be correctness-critical.

### Model Changes

Apple states that routine OS updates change `SystemLanguageModel` and documents
distinct model versions across 26.0-26.3, 26.4, and 27.0 [A4]. Apple recommends
recording prior outputs, comparing model versions, and versioning prompts [A22].
Consequently the production contract versions:

`provider + OS/model cohort + prompt + instructions + schema + tools + options + fixture set`.

A new model never rolls directly into production behavior. It must pass offline
fixtures, simulation, safety checks, human review, and a controlled app release.
For Apple's system model, an old result set can be archived but the old model
usually cannot be frozen or restored after an OS update. An unqualified OS/model
cohort disables Level 3 and falls back to Level 2 until it passes; the
architecture must not promise rollback to an unavailable system model.

## Recommended Intelligence Ladder

| Level | Experience | Device/network dependency | Release gate |
|---|---|---|---|
| 0 | Authored courses, challenges, and callbacks | None | Core movement passes |
| 1 | Seeded grammar composition with authored rhythm templates | None | Solvability and meaningful-variety simulation pass |
| 2 | Deterministic adaptive director selects validated plans from local behavior | None | Different styles receive measurably better plans without rule drift |
| 3 | On-device `SystemLanguageModel` proposes a non-value-bearing `ExperienceIntent` between runs; Level 2 constructs the plan | Apple Intelligence-capable device; offline after model ready | Beats Level 2 blind evaluation and meets latency/battery/failure gates |
| 4 | PCC proposal for unusually complex planning | Eligible hardware, network, entitlement, quota | No current user problem justifies it; rejected for v1 |
| 5 | Core AI or alternate `LanguageModel` provider | Provider-specific | Future seam only; no implementation |

The same deterministic `RunPlanValidator` and engine execute Levels 1-5. Level 0
remains a complete authored game.

## Privacy And Child Safety

### Apple Requirements Relevant To The Design

- Kids Category participation is optional, but selection commits future updates
  to its rules. The selected age band can be 5 and under, 6-8, or 9-11 [A12-A13].
- External links, purchases, and similar actions require a parental gate in a
  designated adult area. A parental gate is generally not legal parental consent
  for personal-data collection [A12-A13].
- Kids apps should not include third-party analytics or advertising except
  narrow documented cases. Behavioral advertising based on Kids Category data
  is prohibited [A12].
- A privacy policy and accurate App Store privacy answers are required; third-
  party SDK behavior is part of the developer's disclosure responsibility
  [A12-A14].
- The Declared Age Range API can provide an age range rather than birthdate when
  a person or guardian chooses to share it [A15]. The proposed game does not need
  that data to deliver its core experience.
- PermissionKit addresses child-parent communication permissions over iMessage
  and significant changes [A16]. A local single-player game has no communication
  feature requiring it.

### Regulatory Boundary

COPPA is a current US rule relevant to online services directed to children
under 13 [A23]. Other jurisdictions can impose additional obligations. This
package makes no legal compliance conclusion. Before release, qualified review
must examine actual data flows, age positioning, storefronts, purchases,
support, and any cloud feature.

### Data-Minimizing Design

```text
bounded local gameplay events
        -> in-memory run aggregates
        -> gameplay-only task-selection evidence
        -> validated plan selection
        -> discard raw event detail at run end
```

- No account, advertising identifier, location, contacts, photos, microphone,
  free text, chat, or third-party analytics.
- No event stream leaves the device.
- No cross-app or cross-device profile.
- Export is absent by default; research playtests use consented observer sheets,
  not production telemetry.
- Parent controls can inspect and reset adaptation; the child can disable it.
- Selection evidence uses complete file protection, is excluded from device
  backup, never enters crash/diagnostic logs, and is deleted by adaptation reset
  or the adult-area delete choice. Backup/sync is deferred because it changes
  the data-flow and disclosure case.
- The marketed age range, App Store age rating, and optional Kids Category band
  remain `UNKNOWN/TBD`; the 6-12 research range does not decide them.

## What The Player Model Must Never Infer

- Health, disability, diagnosis, neurotype, intelligence, school performance,
  emotion, mood disorder, personality, identity, race, ethnicity, religion,
  sexuality, household income, family relationships, location, or real-world
  routines.
- Susceptibility to spending, notification response, stopping resistance,
  frustration tolerance for monetization, or likelihood of compulsive use.
- Age from reaction time or skill. If age-specific presentation is necessary,
  use an explicit parent-controlled setting or Apple's privacy-preserving age
  range, not inference.

## Fallback Architecture

```text
Run request
  -> validated cached plan available? use it
  -> Level 3 eligible and deadline permits? request proposal
  -> proposal validates and simulates? cache/use it
  -> otherwise DeterministicDirector
  -> otherwise authored safe plan
  -> deterministic engine executes
```

No availability alert blocks play. No network retry loop appears to the child.
No generated plan is consumed during an active run.

## Apple Architecture Decision

1. Build Levels 0-2 without importing Foundation Models.
2. Keep the director contract engine-neutral and provider-neutral.
3. If Level 2 passes, test `SystemLanguageModel` in a separate iOS 26+ adapter.
4. Use a static `@Generable` proposal type only as transport into the same
   canonical decoder and validators used by deterministic plans.
5. Do not use PCC, Core AI, MLX, multimodal input, dynamic profiles, or custom
   providers until a measured Level 3 deficiency names a user problem they solve.

## Unknowns Requiring Measurement

- End-to-end generation latency and variance on each supported device cohort.
- Energy, memory, thermal, and install/storage effects.
- Output validity and refusal rates by OS/model version and locale.
- Whether a model proposes plans players prefer to Level 2.
- Whether parents accept any model-driven adaptation even when local.

These unknowns are later experiment inputs, not reasons to raise the deployment
target or narrow the playable audience now.
