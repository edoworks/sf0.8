# Roadmap, Factory Work, Risks, And Smallest Experiment

## N. Sequential Implementation Roadmap

No phase begins because code compiles. Each depends on the prior behavioral gate.

### Phase Authorization Contract

Before implementation begins, each phase must create and review a
`PREREGISTRATION` record for one primary behavioral
outcome, comparator, observation window, practical effect threshold, minimum
complete sample, denominator, exclusions, missing-data handling, safety vetoes,
and `PASS`, `REVISE`, `STOP`, and `INCONCLUSIVE` consequences. Numeric thresholds
after E0 remain `TBD_BY_PILOT` until prior-phase variance and feasibility evidence
exist; they cannot be chosen after results are visible.

The canonical phase record conforms to [phase-gate.schema.json](phase-gate.schema.json).
Its reviewed preregistration with `implementation_authorized: true` authorizes
only the named phase implementation; its
completed `RESULT` binds protocol, build, analysis, and reviewer digests. A future canonical
product repository must add a CI transition guard that rejects Phase N+1 work
without a reviewed Phase N `PASS` record. This research repository specifies
that control but cannot enforce a transition for a product repository that does
not yet exist. An owner override may record an exceptional protocol or scheduling
deviation if policy permits, but it cannot authorize the next phase or relabel a
stopped or inconclusive experiment as passed.

### Phase 0: Movement

- **Objective:** select one movement system that is understandable, fair,
  expressive, and voluntarily replayed without progression.
- **Dependencies:** candidate constitution, reviewed E0 preregistration, and
  approved consent/data-handling materials.
- **Implementation:** build the three equal-polish prototypes for experiment E0
  below; use placeholder geometry, neutral but responsive audio/haptics, fixed
  courses, and instant retry.
- **Tests:** input/state/collision, deterministic replay, frame pacing, restart,
  accessibility settings.
- **Evaluation:** identical-course learning and failure-attribution report.
- **Human playtest:** randomized movement bake-off.
- **Exit:** E0 success gate passes for one candidate and no fairness/accessibility
  veto appears.
- **Kill:** no candidate earns reward-free voluntary replay after one focused
  tuning cycle.

### Phase 1: Core Loop

- **Objective:** prove obstacles, routes, near misses, score, one collectible,
  one rule-changing power-up, failure, and replay form a coherent loop.
- **Dependencies:** Phase 0 movement contract frozen for the phase.
- **Implementation:** one 2-5 minute authored experience composed from <=10
  obstacles and 8-12 chunks.
- **Tests:** grammar, reachability, reaction windows, score reconstruction,
  power-up state, simulation, replay.
- **Evaluation:** novice-to-expert bot distributions and human improvement.
- **Human playtest:** voluntary replay and next-goal observation.
- **Exit:** Preregistered Replayability Gate passes without meta progression;
  threshold is `TBD_BY_PILOT` before Phase 1 implementation.
- **Kill:** rewards are the primary stated reason for replay, or repeated failure
  remains unclear after one tuning cycle.

### Phase 2: Retention

- **Objective:** test whether earned characters, small missions, secrets, and
  visible accomplishment create healthy return interest.
- **Dependencies:** Core Loop Gate.
- **Implementation:** one additional character expression, three teaching
  missions, one collection page, two secrets, one recurring authored callback.
- **Tests:** save/migration/economy/achievement/accessibility and no-obligation
  policy tests.
- **Evaluation:** progression pacing and feature-use observation.
- **Human playtest:** delayed return choice and recall, with no notification.
- **Exit:** Preregistered Retention Gate passes over its declared delay; child
  can stop comfortably and later names a self-chosen reason to return. Threshold
  and delay are `TBD_BY_PILOT` before Phase 2 implementation.
- **Kill:** return interest depends on streak, scarcity, grind, or reward reveal.

### Phase 3: Variation Engine

- **Objective:** prove seeded grammar composition creates meaningful variation
  without fake variety or impossible plans.
- **Dependencies:** Retention Gate and versioned content contracts.
- **Implementation:** 20-30 validated chunks, 3 rhythm profiles, 2 world rules,
  deterministic director, simulation farm.
- **Tests:** >=1,000,000 generated plans, similarity/repetition, difficulty,
  determinism, performance.
- **Evaluation:** blind authored-versus-composed plan review and repeated play.
- **Human playtest:** identify whether runs demand different decisions and remain
  learnable.
- **Exit:** Preregistered Variety Gate passes player-perceived and computed
  effective-variety criteria, set before Phase 3 implementation.
- **Kill:** most combinations differ only cosmetically or composition weakens
  fairness/rhythm versus authored runs.

### Phase 4: Player Model

- **Objective:** determine whether local behavioral adaptation improves content
  selection while preserving agency and stable rules.
- **Dependencies:** Variety Gate; sufficient validated plans for real choice.
- **Implementation:** local confidence-bounded dimensions, decay, reset, explicit
  on/off, DeterministicDirector weighting.
- **Tests:** estimator fixtures, cold start, decay, bounded updates, filter-bubble
  exploration, privacy/storage, reset.
- **Evaluation:** synthetic style separation and blind crossover.
- **Human playtest:** selection fit, surprise, trust, and control comprehension.
- **Exit:** Preregistered Personalization Gate shows the declared practical
  effect versus balanced Level 2 selection, with no safety/trust veto.
- **Kill:** selection evidence fails to differentiate, misadaptation persists,
  players cannot perceive
  benefit, or trust/variety declines.

### Phase 5: AI Director

- **Objective:** test whether Foundation Models proposals outperform the Level 2
  algorithmic director.
- **Dependencies:** Personalization Gate and supported-device test matrix.
- **Implementation:** off-path adapter, static structured schema, no side-effect
  tools, deadline, cache, deterministic fallback.
- **Tests:** frozen fixtures, validation/fallback, model cohorts, latency, energy,
  safety, simulation, upgrade rollback.
- **Evaluation:** preregistered head-to-head against Level 2.
- **Human playtest:** blind crossover on validated builds.
- **Exit:** AI Value Gate passes practical player benefit with no material
  availability, safety, privacy, latency, or battery regression.
- **Kill:** AI is non-inferior only, adds superficial novelty, or increases
  operational burden beyond measured benefit. Remove or defer it.

## O. Factory Work Breakdown

| Unit | Goal and inputs | Files/systems affected | Contract and constraints | Tests/evaluation/DoD | Regression and rollback |
|---|---|---|---|---|---|
| F0 | Freeze movement candidate specification from E0 brief | Movement spec, input fixtures | No progression/AI; equal presentation | Unit/replay/perf tests; adult smoke; candidate build reproducible | Input feel drift; revert candidate data revision |
| F1 | Implement one candidate movement toy | Simulation, renderer, audio/haptics | Fixed timestep; placeholder assets; one input | Same seed/input replay; restart/perf; observed internal pass | Candidate contamination; delete disposable branch |
| F2 | Package randomized E0 builds | Experiment manifest, build receipts | Counterbalanced labels; no persuasive branding | Hash/build verification; moderator rehearsal | Order bias; regenerate manifest |
| F3 | Record E0 results | Restricted consent ledger, pseudonymous sheets, analysis | No PII in repo; preregistered access/retention/deletion; N and intervals required | Dual-review scoring; missing-data audit; exit/kill verdict | Interpretation bias; preserve only within consented retention window, revise analysis |
| F4 | Freeze selected movement contract | Rules schema, golden traces | Only after E0 pass | Trace replay and owner decision | Premature lock; revert and rerun E0 |
| F5 | Add core-loop grammar | Catalog/chunk schemas, validators | Authored vocabulary; no arbitrary scripts | Reachability, reaction, million-plan future harness seed | Impossible/fake variety; disable new catalog version |
| F6 | Add score/power/reward | Score/economy state machines | Reconstructable score; no monetized relief | Property/state/transaction tests; player replay gate | Exploits/economy drift; feature flag and schema rollback |
| F7 | Add retention slice | Save, missions, collection, secrets | No streak/scarcity/grind | Migration and ethical-policy fixtures; delayed playtest | Reward replaces fun; remove meta layer while preserving save migration |
| F8 | Build deterministic director | Planner, similarity index, run cache | Same context+seed byte-identical | Distribution/similarity/simulation report | Rhythm regression; fallback authored playlist |
| F9 | Add local selection evidence | Evidence store/estimator/controls | Allowed dimensions only; reset separate | Estimator/privacy/reset/crossover | Misadaptation/evidence creep; disable/delete adaptation |
| F10 | Add AI adapter experiment | Provider adapter, prompt/schema fixtures | Between runs; no side effects; deadline/fallback | Model matrix, safety, energy, head-to-head | Model drift/availability; remove adapter, retain Level 2 |
| F11 | Release qualification | Accessibility, privacy, StoreKit, device matrix | Product truth must match binary/listing | Full release evidence and human gate | Platform/policy regression; retain previous compatible release |

Every unit begins with an issue containing Goal, Inputs, Files/Systems,
Constraints, Implementation Contract, Tests, Evaluation, Definition of Done,
Regression Risks, and Rollback. Commits and evidence reference that issue.

## P. Risk Register

Scale: severity `S`, probability `P`, and hard-to-detect `D` are 1-5. Priority is
`S*P*D`; estimates are planning judgments, not measured probabilities.

| Rank | Risk | S/P/D | Priority | Detection | Mitigation |
|---|---|---:|---:|---|---|
| 1 | Core game simply is not fun | 5/4/4 | 80 | Voluntary replay and free choice | E0 before architecture/content; stop rule |
| 2 | Child interest fades after novelty | 5/4/4 | 80 | Delayed return/recall | Stable mastery and goals; no scale before retention gate |
| 3 | Fake procedural variety | 4/4/4 | 64 | Semantic similarity plus repeated play | Meaningful-difference contract and closest-1% review |
| 4 | Overengineering before evidence | 5/4/3 | 60 | Scope/diff and gate audit | Kill list; phase dependencies; disposable prototypes |
| 5 | Factory-generated technical debt/doc drift | 4/4/4 | 64 | Contract/link/test mismatch | Small issues, schema tests, reviewed evidence, rollback |
| 6 | Personalization narrows discovery or feels wrong | 4/3/4 | 48 | Crossover, reset use, profile audit | Confidence threshold, exploration budget, off/reset |
| 7 | Generated inappropriate content | 5/2/5 | 50 | Adversarial fixtures and human review | No free text; allow-listed authored IDs; deterministic safety |
| 8 | App Store child/privacy noncompliance | 5/2/4 | 40 | Preflight/legal review | Data minimization, no ads/chat/account, accurate disclosures |
| 9 | Monetization cannot sustain product | 5/4/4 | 80 | Purchase experiment and actual ASC data | Small investment, premium/trial test, portfolio not single-product forecast |
| 10 | AI adds no player value | 3/4/2 | 24 | Head-to-head Level 2 | Defer to Phase 5; remove on non-superiority |
| 11 | AI latency/refusal disrupts flow | 4/3/2 | 24 | Device cohort p95/fallback | Between-run generation, deadline, cache, deterministic fallback |
| 12 | Model unavailable by device/region/settings | 4/4/1 | 16 | Availability matrix | Complete Levels 0-2; no AI entitlement |
| 13 | Model/OS upgrade regresses plans | 4/3/4 | 48 | Frozen cohort fixtures | Version artifacts; app release gate; retain fallback |
| 14 | Battery, thermal, memory, or package cost | 4/3/3 | 36 | Energy/soak/floor device | No runtime generation; budget gate; remove model adapter |
| 15 | Collision or reaction unfairness escapes simulation | 5/2/4 | 40 | Human failure review and replay | Movement envelope, margins, visual cause, regression trace |
| 16 | Privacy scope expands through analytics/cloud | 5/2/4 | 40 | Data-flow/binary/manifest audit | No SDKs/endpoints; separate authorization for any transmission |
| 17 | Content production cost exceeds value | 4/3/4 | 48 | Time per validated chunk/world | Small catalog, reuse metrics, expansion only after demand |
| 18 | Older/unsupported devices receive inferior product | 4/3/2 | 24 | Device matrix | AI is optional; explicit floor from performance evidence |

## Q. Aggressive Kill List

Do not build yet:

- Foundation Models, PCC, Core AI, MLX, custom model providers, or AI dialogue.
- Player preference model or adaptive director.
- Bosses, combat, crafting, building, habitats, pets, quests, narrative campaign.
- Public leaderboards, Game Center, accounts, cloud save, sharing, chat, UGC.
- Daily streaks, notifications, battle pass, rotating shop, events, live ops.
- Character shop, premium currency, consumables, random rewards, paid boosts.
- Collectibles, rewards, unlocks, or progression in E0.
- Final art pipeline, mascot production, marketing site, trailer, localization,
  StoreKit, App Store metadata, or brand naming before Fun Gate.
- Procedural generation in E0. Fixed courses are necessary to observe learning.
- Analytics SDKs and production behavioral experiments on children.
- A generalized factory game framework before a second real consumer.

## R. First Playable: E0 Movement Bake-Off

### Question

Can any one-input movement system create understood, fair, self-motivated replay
before progression, procedural variation, personalization, or AI?

### Three Disposable Candidates

1. **Arc:** tap/hold/release controls a forgiving ballistic leap with landing
   technique and route height.
2. **Glide:** press/release controls continuous lift and descent through momentum
   gates, emphasizing smooth correction.
3. **Tether:** hold attaches to a visible anchor and release slingshots along a
   chosen tangent, emphasizing timing and trajectory.

These are hypotheses, not the product. If a cheaper paper/physics spike reveals
one is infeasible, replace it before child testing and record why.

### Must Include

- 45-60 seconds of fixed, hand-authored challenge per candidate.
- One safe teaching pattern, one route decision, one technique test, one
  breather, one escalating remix, and one payoff.
- Placeholder geometry with equal legibility and polish.
- Responsive neutral sound/haptic feedback, visible cause of failure, instant
  retry, pause, mute, Reduced Motion, and pace/timing assistance.
- Same simple progress/split display; no currency or reward reveal.
- Fixed seed/course, deterministic input recording, performance overlay hidden
  from participants, and randomized candidate order.

### Must Not Include

Progression, missions, unlocks, cosmetics, story, procedural generation,
personalization, AI, final art, store, account, network, leaderboard, boss,
combat, dialogue, or marketing identity.

### Two-Step Sample

- **Internal smoke test:** founder plus one familiar child may expose obvious
  defects; this cannot pass E0. The familiar-child session uses the same guardian
  consent, child assent, stop rights, recording rules, and deletion rights.
- **Directional test:** 12 complete participants, four in each research band
  6-8, 9-10, and 11-12, guardian consent, counterbalanced order, maximum 20
  minutes. This research range does not set the marketed age. Report exact counts
  and Wilson intervals; do not claim market validation.

### Success Gate

The denominator is all 12 participants who received a technically valid exposure
to all three candidates. A technical failure excludes the session before outcome
scoring and requires replacement; choosing to stop remains observed evidence and
is not excluded. Fewer than 12 complete valid exposures, fewer than four per
research band, or unresolved scoring disagreement produces `INCONCLUSIVE`, not a
forced pass/fail.

One candidate advances only if all hold:

- **Primary outcome:** at least 9 of 12 voluntarily start a third attempt during
  the preregistered 10-second silent retry window after their second technically
  valid attempt and before a neutral next-candidate offer;
- at least 10 of 12 demonstrate the basic rule without moderator explanation;
- at least 9 of 12 correctly explain the cause of at least two observed failures;
- at least 7 of 12 improve the preregistered fixed-course performance metric
  between first and last comparable attempt; participants without three attempts
  remain in the denominator as not demonstrating improvement;
- at least 6 of 12 select that candidate for free choice after trying all candidates;
- if two participants in one research band show the same blocking comprehension
  or accessibility failure, the result is `INCONCLUSIVE` pending targeted review
  rather than averaged away;
- at least two participants independently demonstrate an unprompted expressive
  technique or route experiment;
- stopping produces no observed obligation/distress pattern attributable to the
  design;

Counts are directional at this sample size. A pass authorizes Phase 1 only, not
the product thesis, personalization, or AI. Founder judgment is recorded
separately as the portfolio authorization decision and cannot change the
empirical `PASS`, `REVISE`, `STOP`, or `INCONCLUSIVE` result.

### Kill Or Revise

- `REVISE`: complete initial evidence exists and no candidate meets the gate;
  allow one revision targeted at the single clearest movement/fairness bottleneck.
- `INCONCLUSIVE`: repair protocol, scoring, technical exposure, or sample cells;
  do not add product features.
- `STOP`: no candidate passes after the one allowed revision; stop the runner
  direction or test a different small arcade genre. Do not combine all three or
  add rewards.

## S. Success Gates

| Gate | Required evidence | Blocks |
|---|---|---|
| Fun | E0 movement success without rewards | Core-loop expansion |
| Replayability | Voluntary replay driven by understood mastery/choice | Progression |
| Retention | Delayed self-chosen return/recall without pressure | Large content investment |
| Variety | Meaningfully different, fair composed runs | Player modeling |
| Personalization | Level 2 improves fit/agency without narrowing or rule drift | AI adapter |
| AI Value | Level 3 materially beats Level 2 with safe fallback and acceptable cost | AI production use |
| Scale | Demand, economics, content cost, support, and release quality | Portfolio expansion/live investment |

## Why Start This Tomorrow?

A child chooses this game tomorrow because yesterday they learned a move they
almost mastered, glimpsed a route they now understand how to reach, and caused a
funny or dramatic chain of events they want to reproduce or top. Their favorite
character and discoveries make the world feel like theirs. A complete attempt
fits the time they have, failure feels fair, and opening the game leads directly
back to the skill or mystery they chose. It offers a specific, achievable story
for the next five minutes rather than an infinite demand for attention.

That experience, not AI or personalization, earns the return.

## Final Experiment

Build E0 exactly as specified above: three equal-polish, 45-60 second,
deterministic movement toys with no progression, procedural generation,
personalization, or AI. Run the internal veto, then the consented randomized
12-child directional test with four complete valid exposures in each research
band. Do not begin Phase 1 implementation unless one
movement candidate passes every E0 success criterion.
