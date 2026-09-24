# Gameplay Grammar, Player Model, And Directors

Status: `CANDIDATE_SYSTEM_CONTRACTS`

Dependency: the Fun, Replayability, Retention, and Variety gates must pass before
the player model is implemented.

## G. Gameplay Grammar

### Authority Layers

| Layer | Responsibility |
|---|---|
| Authored | Movement rules, obstacle/enemy behaviors, chunk geometry, telegraphs, rhythm templates, rewards, moments, copy, art, and safety labels |
| Procedural | Seeded selection, transformation, and ordering within authored compatibility constraints |
| Adaptive | Selection weights within confidence-bounded local task-selection evidence |
| AI-assisted | Optional proposal of identifiers and bounded parameters through the same schema; no new executable content |
| Engine | Canonical decoding, validation, simulation, execution, score, economy, save, and fallback |

### Formal Content Model

```text
ContentCatalog(version)
  MovementRules[]
  Worlds[]
  Chunks[]
  Encounters[]
  Objectives[]
  Rewards[]
  PowerUps[]
  Modifiers[]
  MomentTemplates[]
  RhythmProfiles[]

RunPlan
  identity: {planID, catalogVersion, rulesVersion, seed, directorVersion}
  mode: {standard | assisted | challenge | discovery}
  worldID
  movementRulesID
  rhythmProfileID
  beats[]
  finale
  declaredMetrics
  provenance

RunBeat
  phase: {teach | flow | choice | tension | breather | escalation | payoff}
  chunkID
  transform: {mirror, variant, parameterOverrides}
  encounterIDs[]
  optionalMomentID
  transitionContract
```

### Example Schema

```json
{
  "schemaVersion": 1,
  "identity": {
    "planID": "plan-418022-a",
    "catalogVersion": "catalog-0.3.0",
    "rulesVersion": "rules-1.2.0",
    "seed": 418022,
    "directorVersion": "deterministic-2.1.0"
  },
  "mode": "standard",
  "worldID": "clockwork-garden",
  "movementRulesID": "movement-e0-b",
  "rhythmProfileID": "learn-risk-release-60",
  "beats": [
    {
      "phase": "teach",
      "chunkID": "rise-wide-01",
      "transform": {"mirror": false, "variant": "base", "parameterOverrides": {}},
      "encounterIDs": [],
      "optionalMomentID": null,
      "transitionContract": "grounded-wide"
    },
    {
      "phase": "choice",
      "chunkID": "fork-high-risk-02",
      "transform": {"mirror": true, "variant": "base", "parameterOverrides": {}},
      "encounterIDs": ["rival-glimpse"],
      "optionalMomentID": "rival-cog-glimpse",
      "transitionContract": "airborne-center"
    }
  ],
  "finale": {"chunkID": "garden-payoff-01", "momentID": "rival-cog-return"},
  "declaredMetrics": {"durationBand": "45-75s", "difficultyBand": "standard-2"},
  "provenance": {"kind": "deterministic", "contextDigest": "sha256:example"}
}
```

The authoritative engine overlays objectives, score opportunities, reward
placements, entitlements, and progression after the plan is accepted. All plan
identifiers resolve in the signed/versioned catalog. Parameter overrides use
per-component ranges; unknown fields, identifiers, combinations, and versions
fail closed to a safe plan.

### Content Contracts

Each chunk declares:

- entry/exit position, velocity, state, and camera envelopes;
- required and prohibited movement capabilities;
- reaction-time and precision estimates by assistance mode;
- intensity, novelty, decision density, and duration bands;
- compatible predecessors/successors, worlds, modifiers, and encounters;
- teaching prerequisites and cooldown tags;
- bot completion distribution and human-evidence status;
- age/safety/accessibility labels;
- semantic family and perceptual signature for similarity analysis.

### Meaningful Variety

Mathematical combinations are not treated as distinct experiences. Two plans
are meaningfully different only when they differ on at least two player-visible
dimensions such as route topology, technique, rhythm, world interaction,
objective, encounter consequence, or finale. Palette, mirrored geometry alone,
reward location alone, and numeric speed changes do not qualify.

The catalog report counts:

- valid combinations after compatibility filtering;
- unique semantic signatures;
- pairwise structural and perceptual similarity;
- repeated chunk n-grams;
- novelty exposure by player history;
- effective variety under each mode/director, not theoretical Cartesian size.

## H. Player Model

### Allowed Observations

Aggregated locally per run:

- chosen route and voluntary risk tier;
- action timing distribution relative to safe windows;
- near-miss, collision, recovery, and clean-execution counts;
- optional collectible pursuit when it creates a route cost;
- secret-route attempts and discoveries;
- objective selection/completion/abandonment;
- interaction with transformations, world actors, and story moments;
- explicit mode and finite-format selection;
- explicit player/parent settings and adaptation enable/reset.

Raw touch paths and frame-by-frame events remain in memory only for the active
run, then are discarded. Production does not record screen, voice, text, or identity.

### Derived Task-Selection Evidence

These are internal weighted counts for choosing tasks, not durable traits. Raw
weights are never presented to a child or parent as scores or trait labels.

| Internal field | Narrow selection meaning | Evidence examples | Excluded interpretation |
|---|---|---|---|
| `offeredPaceSelections` | Counts explicit pace/mode choices | paced or standard mode selected | age, cognition, disability |
| `optionalRiskRouteSelections` | Counts visible route tradeoffs | high route chosen while safe route available | personality or impulsivity |
| `timingChallengeSelections` | Counts self-chosen timing tasks | timing route selected or reselected | intelligence or motor diagnosis |
| `optionalRouteSelections` | Counts alternate/secret choices | detour selected at understood cost | curiosity as personality |
| `optionalArtifactSelections` | Counts collection routes | artifact route selected at opportunity cost | spending susceptibility |
| `transformationRouteSelections` | Counts temporary-rule routes | transformation route selected | stimulation need or neurotype |
| `explicitFormatSelections` | Counts short/standard/challenge choices | explicit pre-run format choice | schedule or household routine |
| `familiarNovelPlanSelections` | Counts explicit familiar-versus-new choices | mastery or unseen plan selected | boredom proneness |

Combat and humor are omitted until the product contains validated, observable
choices that can distinguish them. “Engagement,” challenge persistence, session
duration, return frequency, stopping behavior, purchases, and notification
response are prohibited features and optimization targets.

### Representation

Each selection family stores `{weightedCounts, confidence, evidenceWeight, updatedAtRun}`.
Implementation may use bounded beta distributions or another interpretable
online estimator. Requirements:

- prior counts are neutral, confidence low;
- positive and negative evidence definitions are versioned;
- decay applies to stale evidence, not permanent identity;
- no update from unavoidable choices or failed comprehension;
- a single run cannot change normalized selection weight more than `0.10` or
  cross two plan bands;
- confidence requires repeated independent opportunities;
- adaptation uses a dimension only above a validated confidence threshold;
- 15-25% of eligible plans remain safe exploration to avoid a filter bubble;
- explicit setting overrides behavior and is reversible.

### Storage, Reset, And Cold Start

- Store locally in a separately versioned `TaskSelectionEvidence` file with
  complete file protection and backup exclusion.
- Do not include raw events, device identifiers, dates of birth, or real-world
  time patterns beyond aggregate recency necessary for decay.
- Cold start uses authored balanced plans and direct mode choices, not a survey.
- “Reset what the game learned” deletes selection evidence and adaptation history while
  preserving progress and purchases.
- Disabling adaptation stops all use immediately and freezes or deletes the file
  according to the adult control choice, then returns to balanced deterministic selection.
- The adult area provides a non-scored inspection summary: whether adaptation is
  enabled, which neutral task categories have repeated evidence or insufficient
  evidence, why the next plan was selected, and when reset last occurred. It
  never shows inferred ability, personality, diagnosis, or raw event history.
- Logs and crash reports contain reason codes, not gameplay event detail or
  selection evidence. Removed fields are deleted during migration; corruption
  deletes optional selection evidence without affecting progress.

## I. Director Contract

```swift
protocol ExperienceIntentProvider {
    var version: DirectorVersion { get }
    func propose(context: RunContext) async -> ExperienceIntent
}

protocol RunDirector {
    var version: DirectorVersion { get }
    func build(intent: ExperienceIntent, context: RunContext) -> RunPlan
}

struct RunContext {
    let catalogVersion: CatalogVersion
    let rulesVersion: RulesVersion
    let eligibleContent: EligibleContentDigest
    let progress: ProgressSummary
    let selectionEvidence: TaskSelectionEvidenceSummary?
    let recentSemanticSignatures: [Signature]
    let requestedMode: RunMode
    let seed: UInt64
    let deadline: Duration
}
```

The engine does not execute `ExperienceIntent`. An algorithmic provider or the
AIDirector may propose its bounded semantic fields. The DeterministicDirector
canonicalizes that intent and uses seeded constrained search to construct a
`RunPlan`, then the engine validates, simulates, caches, and only then schedules
it. Identical deterministic construction remains downstream of both providers,
so the model never gains plan-field authority.

### DeterministicDirector

1. Filter catalog by rules, progression, mode, safety, and compatibility.
2. Select a rhythm profile for requested duration.
3. Calculate target ranges from neutral defaults or confidence-qualified local
   task-selection counts.
4. Use seeded constrained search to assemble beats.
5. Penalize recent semantic signatures and repeated n-grams.
6. Reserve novelty budget and story-moment cooldown.
7. Score candidates for rhythm, selection-evidence fit, variety, difficulty, and
   objective coherence.
8. Return the highest-scoring `RunPlan` with a machine-readable rationale.

Given identical context and seed, output is byte-identical.

### AIDirector

The AIDirector receives a minimized, versioned, allow-listed projection of
eligible non-value-bearing semantic families and task-selection evidence. It has
no direct save/store access. Purchases, raw events, stop/duration/return signals,
reward state, and identifiers are excluded by construction.

It proposes an `ExperienceIntent` containing only rhythm-profile family,
world-theme family, familiar-versus-novel balance, and eligible non-value-bearing
moment/encounter families. The DeterministicDirector constructs the actual
`RunPlan` from difficulty- and score-opportunity equivalence classes. The engine
overlays objectives, rewards, progression, assistance, and score coefficients.
AI never chooses chunks, geometry, parameter overrides, reward placement,
entitlements, progression objectives, assistance, physics, or economy. It runs
between sessions with a deadline and never blocks play.

### Head-To-Head Evaluation

- Freeze catalog, rules, context fixtures, seeds, prompt, schema, tools, options,
  provider, and model cohort.
- Compare validity, fallback, latency, energy, semantic variety, difficulty
  fit, repetition, and simulation outcomes.
- Blind human reviewers compare plan summaries and recorded play without knowing
  director source.
- Player crossover tests compare voluntary replay, understood fairness,
  self-stated next goal, and delayed recall.
- AIDirector advances only with a practically meaningful preregistered advantage
  on player outcomes and no safety, availability, latency, or energy regression.

## AI Features Must Earn Existence

| Feature | User problem | Non-AI solution | AI proposal | Latency/privacy/failure | Evaluation and kill criterion |
|---|---|---|---|---|---|
| Experience-intent selection | Large validated catalog may make high-level variety selection harder | Seeded weighted intent selector | Propose non-value-bearing authored semantic families | Between runs, local preferred; malformed/refusal -> deterministic | Kill unless blind player outcomes beat Level 2 and validity >=99.9% before fallback |
| Story-moment selection | Callbacks may become repetitive | Authored state machine with cooldowns | Select a fitting authored template | No free text; local; failure -> state machine | Kill unless delayed recall/variety improve without frequency inflation |
| Mission wording | Authored combinations may need concise presentation | Templated localized copy | Generate phrasing | Text safety/localization risk; fallback template | Defer; kill if any child-safety review burden exceeds measured benefit |
| Dialogue | Desire for lively characters | Animation, reactions, authored barks | Generated NPC conversation | Interactive latency and open-ended child safety risk | Reject for v1; no core user problem requires it |
| Player inference | Sparse choices create uncertainty | Interpretable weighted counts | Model summarizes a player | Profiling and opacity risk | Reject; deterministic task-selection evidence is more inspectable |
| Difficulty control | Match player ability | Explicit modes and bounded adaptive selection | Model changes challenge | Fairness/comparability risk | Forbidden if it changes runtime rules; no experiment |

## J. Provider Architecture

See [APPLE_PLATFORM.md](APPLE_PLATFORM.md). The provider seam is:

```text
DirectorProvider
  deterministic
  systemLanguageModel (optional iOS 26+ adapter)
  futureLanguageModel (iOS 27+ protocol adapter)
```

Provider output always enters the same canonical draft decoder. Private Cloud
Compute, Core AI, MLX, and custom servers are not implementation dependencies.

## K. Safety And Validation Pipeline

```text
experience-intent proposal
  -> decode/version/schema validation
  -> identifier allow-list and non-value-bearing family resolution
  -> deterministic plan construction within difficulty/score equivalence classes
  -> combination and transition contracts
  -> movement-envelope playability
  -> reaction-time and difficulty budgets
  -> rhythm and novelty budgets
  -> economy/reward invariants
  -> age/safety/accessibility labels
  -> multi-bot simulation and deterministic replay
  -> similarity/repetition checks
  -> signed cache with provenance
  -> authoritative engine execution
```

| Stage | Rejects | Fallback |
|---|---|---|
| Decode/version | Unknown/missing/type-invalid data | Deterministic director |
| Allow-list | Unknown, value-bearing, or unavailable family | Deterministic director |
| Compatibility | Illegal predecessor/successor/modifier | Deterministic director |
| Playability | Unreachable or margin-deficient transitions | Try next deterministic candidate, then safe authored plan |
| Difficulty | Reaction/precision/intensity outside mode | Same |
| Rhythm | Missing teaching/breather/payoff or excessive novelty | Same |
| Economy | Reward cap, duplicate, progression, or entitlement violation | Same |
| Safety | Age, flash, motion, content, or accessibility violation | Same |
| Simulation | Bot failure distribution or deterministic divergence | Same |
| Similarity | Repetition threshold exceeded | Next candidate; repetition-safe authored set |

Rejected drafts are counted by local reason code for development evaluation.
Production does not upload player-linked failures. No prompt or guardrail can
waive an engine validator.
