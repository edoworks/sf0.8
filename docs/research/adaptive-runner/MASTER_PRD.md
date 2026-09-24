# Candidate Master Product Requirements Document

Status: `CANDIDATE_NOT_AUTHORIZED_FOR_IMPLEMENTATION`

Research cutoff: `2026-09-23`

Constitution: [GAME_CONSTITUTION.md](GAME_CONSTITUTION.md)

## Product Premise

A premium-quality, offline-first, one-input 2D runner where expressive movement,
authored world rules, route choice, and systemic callbacks create short stories
worth retelling. A deterministic director can eventually choose future run plans
from observed task selections. Optional model intelligence is admitted only
if it beats that director under controlled evaluation.

Working promise: **“A small world of tricks that remembers how you like to play,
without changing the rules.”** This is a hypothesis, not marketing copy.

## Goals

- Deliver movement a child voluntarily replays without rewards or progression.
- Support novice success and expert expression under the same stable rules.
- Create memorable physical and systemic events, not merely generated dialogue.
- Produce meaningful variation from versioned authored components.
- Keep gameplay complete offline and independent of generative AI.
- Earn parent trust through privacy, fair monetization, and clear stopping points.
- Make each system independently testable by an AI-driven software factory.

## Non-Goals

- A generic three-lane runner, live service, social network, UGC platform, or
  simulation of Minecraft/Roblox scale.
- Combat, bosses, building, crafting, pet care, dialogue, or narrative campaigns
  before the core gates justify them.
- Accounts, chat, ads, third-party analytics, notifications for retention,
  public leaderboards, or cloud saves in the first commercial scope.
- Real-time model control, arbitrary generated mechanics, or model-authored game
  rules.
- Optimizing total playtime, daily active use, purchases, or streak adherence.

## Personas

These are research personas. The marketed age range, App Store age rating, and
whether to enter the optional Kids Category are `UNKNOWN/TBD` until product,
platform, and qualified legal review. Recruiting ages 6-12 for edge testing does
not decide storefront positioning.

### Curious Improver, approximately 7-10

Understands direct action quickly, wants to beat a visible mistake, enjoys
physical humor and secrets, and may not read instructions patiently.

### Expressive Explorer, approximately 9-12

Chooses riskier routes, wants a favorite character/style, notices patterns, and
sets personal goals beyond score.

### Access-Seeking Player, any target age

Benefits from slower pace, larger timing windows, reduced motion, simplified
input, or an extra hit. Assistance is visible, dignified, and never monetized.

### Parent Purchaser

Needs a complete, age-appropriate, offline game with clear price, no ads, no
tracking, no chat, understandable settings, and easy interruption.

## Core Loop

```text
choose character/challenge
  -> play a 30-120 second intentional run
  -> move, choose routes, take risks, discover interactions
  -> clear, fail, or reach a satisfying checkpoint
  -> see cause, personal comparison, discoveries, and earned progress
  -> replay, choose another goal, or stop cleanly
```

The exact movement verb is `TBD_BY_E0`. The bake-off compares materially
different one-input candidates at equal polish; it does not assume jumping wins.

## Gameplay Requirements

### Movement And Controls

| ID | Requirement | Acceptance criteria |
|---|---|---|
| MOV-01 | One primary touch input supports immediate action and expressive technique. | The preregistered E0 comprehension and replay counts pass; no candidate advances solely on preference ratings. |
| MOV-02 | Fixed-timestep gameplay separates simulation from rendering. | Recorded input replay preserves score, state transitions, contacts, and plan consumption within defined tolerance. |
| MOV-03 | Input buffer, grace windows, acceleration, gravity/steering, and release behavior are data-driven. | Values are fixture-tested, shown in debug overlay, and changed only with replay and playtest evidence. |
| MOV-04 | Collision geometry is independent of art and favors readable near misses. | Swept collision and boundary tests pass; observed deaths are correctly identified by at least 80% of applicable participants. |
| MOV-05 | Restart is immediate. | Input-to-new-run median <=300 ms and p95 <=500 ms on floor hardware. |
| MOV-06 | Camera preserves forward readability and comfort. | Minimum telegraph time remains visible at every legal speed; Reduced Motion removes shake/zoom impulses. |

### Obstacles, Routes, And Enemies

| ID | Requirement | Acceptance criteria |
|---|---|---|
| OBS-01 | Every hazard has a unique silhouette and teach-before-combine introduction. | Visual review passes grayscale/color-deficiency checks; first exposure cannot require prior knowledge. |
| OBS-02 | A versioned movement envelope defines reachable positions over time. | Every composed transition passes reachability analysis with safety margin for its declared ability mode. |
| OBS-03 | Runs contain meaningful route choices, not cosmetic forks. | Each route declares different risk, technique, discovery, or reward; simulation verifies both are viable. |
| OBS-04 | Moving hazards use deterministic trajectories and telegraphs. | Same seed/plan/input produces the same logical contacts; minimum reaction-time budget passes. |
| ENY-01 | Early “enemies” are world actors governed by normal movement rules, not combat targets. | Player can understand avoidance/interaction from motion and telegraph; no health sponge or separate combat tutorial. |
| ENY-02 | A recurring rival may alter route pressure but not physics. | Rival state is authored, bounded, reproducible, and removable without invalidating the run. |

### Scoring And Near Misses

| ID | Requirement | Acceptance criteria |
|---|---|---|
| SCR-01 | Base score is progress plus at most three inspectable skill bonuses. | Score can be reconstructed exactly from event log; UI explains each bonus without a hidden formula. |
| SCR-02 | Near misses reward deliberate risk without changing collision. | Threshold is geometrically defined; false-positive/negative fixtures pass; no rescue logic occurs. |
| SCR-03 | Standard, assisted, and modified runs are distinguishable. | Records include ruleset/mode; UI never ranks materially different modes as equivalent. |
| SCR-04 | Personal comparison emphasizes learning. | End screen shows one prior split/actionable delta and can be dismissed to replay in one input. |

### Collectibles, Rewards, And Power-Ups

| ID | Requirement | Acceptance criteria |
|---|---|---|
| COL-01 | Collectibles invite route choice and communicate value before commitment. | Placement passes reachability and decision-window checks; missed collectibles do not obstruct survival. |
| REW-01 | Rewards are fixed or transparently earned; no paid/random duplicates. | Reward table is deterministic, finite, auditable, and economy simulation stays within progression bounds. |
| PWR-01 | Each power-up changes a movement or world interaction rule temporarily. | Blind playtest can distinguish its decision impact; removing score VFX does not erase its gameplay value. |
| PWR-02 | Every power-up has authored entry, active, warning, and exit states. | State-machine tests cover interruption, collision, save exclusion, and safe fallback. |

### Rhythm And Difficulty

| ID | Requirement | Acceptance criteria |
|---|---|---|
| DIF-01 | Difficulty is a vector: pace, timing precision, decision density, route risk, pattern complexity, and recovery pressure. | Reports graph each axis; no phase raises more than two axes simultaneously without evidence. |
| DIF-02 | Each run follows a declared rhythm profile. | Plan validator enforces teaching, intensity slope, breathers, novelty budget, and finale constraints. |
| DIF-03 | Reaction demand respects mode-specific minimums. | p1 simulated reaction-time requirement never falls below the approved floor; human failures are reviewed against telemetry-free observation. |
| DIF-04 | Hidden dynamic difficulty is prohibited. | Seed plus mode fully determines rules; test proves player history cannot alter physics or obstacle timing. |

## Retention Systems

### Progression

| ID | Requirement | Acceptance criteria |
|---|---|---|
| PRO-01 | Persistent progress records accomplishment, not attendance. | No streak loss, energy, expiry, or daily debt exists in schema or UI. |
| PRO-02 | Unlocks widen expression or authored choice before increasing power. | Every unlock has a player-facing difference and a bounded balance classification. |
| PRO-03 | Failure preserves earned discoveries and fixed rewards. | Crash/restart/save tests prove no duplicate grant or loss at transaction boundaries. |

### Missions And Challenges

| ID | Requirement | Acceptance criteria |
|---|---|---|
| MIS-01 | Missions teach or remix existing play. | Each mission maps to one validated mechanic and can be completed without grind, ads, purchases, or intentional failure. |
| MIS-02 | Daily/shared seeds are optional and deterministic. | Same content/rules version and seed yields the same plan; missing a day loses nothing. |
| MIS-03 | A player can choose among a small goal set. | At most three active goals; all have clear completion and a stop state. |

### Characters And Cosmetics

| ID | Requirement | Acceptance criteria |
|---|---|---|
| CHR-01 | Characters have distinctive silhouette, animation, sound, and personality through action. | Recognition test succeeds without name/color alone; age and accessibility review passes. |
| CHR-02 | Standard characters do not buy competitive advantage. | Score-comparable modes share movement envelope; ability variants are separate modifiers or equivalent choices. |
| COS-01 | Cosmetics are earned or permanently purchased in clear bundles. | No random draw, duplicate, scarcity timer, or child-facing storefront prompt. |

### Environments And World Rules

| ID | Requirement | Acceptance criteria |
|---|---|---|
| WLD-01 | Worlds differ mechanically, not only by palette. | Each world changes at least one authored interaction and one route grammar while preserving core control. |
| WLD-02 | Environment telegraphs rule changes before testing them. | Safe introduction segment precedes lethal combination; comprehension observed in playtest. |
| WLD-03 | New world rules remain simulator-legible. | Bot capabilities and movement envelope explicitly model the rule; unmodeled rules cannot ship. |

### Secrets And Achievements

| ID | Requirement | Acceptance criteria |
|---|---|---|
| SEC-01 | Secrets are hinted, rule-consistent, and discoverable without data mining. | At least one target participant discovers or forms a plausible hypothesis without instruction; no secret requires purchase or attendance. |
| ACH-01 | Achievements recognize mastery, exploration, and playful experimentation. | No achievement requires unhealthy duration, daily streak, spending, repetitive grind, or inaccessible precision without an alternate. |

### Bosses

Bosses are `DEFERRED`. A later milestone encounter may reuse normal movement and
world rules. It must pass the same grammar and simulation pipeline and cannot
introduce a separate combat game. No boss work begins before Variety Gate.

## Story-Worthy Moments

A story-worthy moment is a rare, understandable gameplay event a player may
spontaneously describe or show to another person. It is not generated dialogue.

Candidate families:

- a rival returns with a visible consequence from a previous run;
- a collected object changes a familiar authored segment;
- two known power/world rules combine into physical comedy;
- a secret route rejoins the main route at a dramatic moment;
- a near miss triggers an authored escalating chase;
- a previously harmless actor becomes an ally under an earned condition;
- a rare but seeded finale reflects the player's chosen route.

| ID | Requirement | Acceptance criteria |
|---|---|---|
| SWM-01 | Moments are authored templates with deterministic triggers and caps. | Every template has setup, trigger, payoff, cooldown, safety class, and fallback; simulation verifies frequency bounds. |
| SWM-02 | Rare does not mean random reward. | Moment odds are not monetized, do not expire, and cannot block collection completion. |
| SWM-03 | Measure locally without surveillance. | Device stores only aggregate template counts and recency; playtests record spontaneous reactions with consent. |
| SWM-04 | A moment is successful when remembered. | In delayed recall, participants describe the event or causal action; raw occurrence count alone is insufficient. |

## UX And Lifecycle

| ID | Requirement | Acceptance criteria |
|---|---|---|
| UX-01 | First launch enters safe interactive play, not account, shop, settings, or exposition. | First meaningful action median <10 seconds in observed test. |
| UX-02 | Onboarding teaches by safe arrangement and ghost/example only when needed. | At least 80% demonstrate basic rule without moderator explanation; tutorial can be replayed. |
| UX-03 | Pause is available in one action and stops logical time. | Physics, timers, audio transitions, and input state tests pass across pause/resume. |
| UX-04 | Background/interruption pauses and checkpoints safely. | Lifecycle tests cover phone/system interruption, termination, audio route change, and no duplicate rewards. |
| UX-05 | End screen supports replay, goal selection, and stop with equal dignity. | Replay is one input; no countdown, guilt copy, obscured quit, or store interruption. |

## Accessibility

| ID | Requirement | Acceptance criteria |
|---|---|---|
| A11Y-01 | Necessary cues use at least two channels. | Accessibility audit confirms color, sound, haptic, motion, and text are never sole critical signals. |
| A11Y-02 | Reduced Motion/Flash removes nonessential shake, zoom, parallax, full-screen flash, and intense particles. | Automated setting snapshots plus visual review pass; mechanics remain unchanged. |
| A11Y-03 | Independent music, effects, haptics, contrast, and assistance settings persist locally. | Save round-trip and reset tests pass. |
| A11Y-04 | Menus support VoiceOver/Switch Control and scalable readable text. | Accessibility Inspector and physical-device flow complete all non-gameplay actions. |
| A11Y-05 | Gameplay offers explicit pace, timing-window, and extra-hit modes. | Modes are available before failure, never sold, clearly labeled, and independently simulated. |

## Audio And Haptics

| ID | Requirement | Acceptance criteria |
|---|---|---|
| AUD-01 | Movement, landing, risk, collection, transformation, failure, and celebration have distinct responsive cues. | Event-to-cue latency meets device budget; repeated cues avoid fatigue in review. |
| AUD-02 | Music supports rhythm arcs without carrying timing requirements alone. | Muted play remains fully understandable; intensity transitions follow plan state. |
| HAP-01 | Haptics reinforce significant events and respect system/user settings. | Unsupported devices degrade silently; no continuous or excessive haptic pattern. |

## Saves And Offline Behavior

| ID | Requirement | Acceptance criteria |
|---|---|---|
| SAV-01 | Versioned local save uses atomic writes and migrations. | Golden fixtures migrate from every supported version; corruption falls back without crash and preserves recoverable data. |
| SAV-02 | Save separates progress, settings, task-selection evidence, and model artifacts. | Player can reset adaptation without deleting progress/purchases; full reset is adult-gated. |
| OFF-01 | All core gameplay, progression, and adaptation Levels 0-2 work offline. | Network-denied end-to-end suite passes from first launch through replay and unlock. |
| OFF-02 | Model/network unavailability is invisible to active play. | Forced failure always selects cached deterministic/authored plan within deadline. |

## Privacy And Parental Considerations

| ID | Requirement | Acceptance criteria |
|---|---|---|
| PRI-01 | No account, third-party analytics, ads, tracking, chat, location, contacts, microphone, photos, or free-form child input. | Binary/SDK/data-flow audit and privacy manifest agree. |
| PRI-02 | Gameplay observations remain local; raw events are not persisted beyond the active run. | Storage inspection proves no raw-event file, backup entry, log, crash field, or network transmission; aggregate selection evidence has deletion tests. |
| PAR-01 | Adult area contains purchases, restore, external links, privacy, adaptation reset, and full reset. | Parental gate tests cover success, failure, cancellation, and accessibility. |
| PAR-02 | Product does not claim a parental gate is legal consent. | Privacy/legal copy review passes before release. |
| PRI-03 | Derived selection evidence uses complete file protection, is excluded from device backup, and is deleted on adaptation reset or delete choice. | Locked-device, backup inventory, migration, crash/log redaction, reset, uninstall/reinstall, and corruption fixtures pass before collection exists. |
| PAR-03 | Adult area explains adaptation without profiling the child. | It shows enabled state, neutral task categories with repeated or insufficient evidence, next-plan rationale, and last reset; review confirms no raw weights, ability/personality labels, or raw event history. |

## Monetization

Preferred hypothesis: paid upfront with all launch gameplay included. Alternative
experiment: free deterministic demo plus one permanent full unlock. Both require
Family Sharing support where available, transparent price, restore behavior, and
no child-facing pressure.

| ID | Requirement | Acceptance criteria |
|---|---|---|
| MON-01 | No ads, subscriptions, consumables, loot boxes, paid revives, paid power, energy, or frustration sales. | Store configuration, code scan, economy schema, and reviewer flow contain none. |
| MON-02 | Purchases and external store surfaces are adult-gated. | Child cannot reach purchase flow without gate; Ask to Buy is not treated as a substitute. |
| MON-03 | Entitlements restore and work offline after receipt validation where platform permits. | StoreKit sandbox interruption/restore/family tests pass. |
| MON-04 | Expansion packs, if any, are substantial and permanent. | Pack acceptance is defined before sale; removing it does not degrade base balance. |

## Performance And Platform

The first experiment is engine-neutral and targets touch plus keyboard test
input. A later engine ADR selects SpriteKit, Godot, or another qualified path
using measured build reproducibility, fixed-timestep behavior, accessibility,
profiling, tooling, and factory maintainability.

| ID | Requirement | Acceptance criteria |
|---|---|---|
| PERF-01 | 60 logical updates/second and stable rendered 60 FPS on declared floor devices. | p99 frame-time and hitch budgets pass representative worst-case plan; no thermal degradation in 15-minute soak. |
| PERF-02 | Cold start to playable state <=3 seconds on floor device. | Median and p95 measured from clean launches. |
| PERF-03 | Gameplay memory, energy, battery, package size, and thermal budgets are versioned. | Release report compares baseline and fails material unexplained regression. |
| PLAT-01 | Initial commercial target is universal iPhone/iPad; exact minimum OS follows engine ADR and device evidence. | Every supported family/orientation/control claim has simulator plus physical-device evidence. |
| PLAT-02 | Unsupported Apple Intelligence hardware receives the complete base product. | Device matrix verifies no core feature, content, or entitlement is missing. |

## Release-Level Acceptance

The candidate product cannot enter implementation because `E0` has not passed.
If authorized after E0, each release candidate additionally requires:

- constitution conformance;
- deterministic replay and migration evidence;
- statistical simulation report;
- accessibility and child-safety review;
- observed human playtest for the phase's behavioral gate;
- device performance/energy evidence;
- privacy binary-manifest-listing agreement;
- rollback plan and prior-version save compatibility;
- App Store metadata and reviewer flow consistent with shipped behavior.
