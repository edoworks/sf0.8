# Evaluation Harness And Ethical Fun Testing

## L. Automated Evaluation Harness

Automation can reject impossible, unfair, repetitive, unstable, unsafe, or
misbalanced systems. It cannot establish fun.

### Deterministic Test Record

Every simulated or recorded run binds:

```text
build revision
content catalog version
rules version
director/provider/prompt/schema/tool versions
seed and canonical RunPlan digest
bot or input trace version
fixed timestep
device/simulator class where relevant
final state and metric digest
```

### Bot Players

Bots represent capabilities, not people or diagnoses.

| Bot | Policy | Primary use |
|---|---|---|
| `NoInputBot` | Never acts | Safe introductions, floor contact, automatic hazards |
| `RandomInputBot` | Legal random actions | Crash resistance and accidental completion |
| `LateReactorBot` | Correct action with high delay and jitter | Novice reaction margin |
| `LearningBot` | Improves timing estimate over repeated identical plans | Whether deterministic practice produces measurable learning |
| `SafeRouteBot` | Maximizes survival margin | Baseline solvability and low-risk route |
| `RiskRouteBot` | Maximizes skill bonus/route payoff under survival constraint | Risk/reward integrity |
| `CollectorBot` | Pursues optional items when reachable | Collection-route viability |
| `ExplorerBot` | Prefers unseen branches and secrets | Alternate-route reachability |
| `PrecisionBot` | Low-jitter near-optimal control | Expert ceiling and score bounds |
| `AssistModeBot` | Uses each declared assistance envelope | Assistance completeness and score separation |
| `AdversarialBot` | Boundary inputs, input spam, pause/interruption | State-machine and exploit discovery |

`NoviceBot`, `AverageBot`, and `ExpertBot` may be report aliases for calibrated
delay/jitter/capability profiles after E0 human evidence sets those parameters.
They must not pretend to simulate a seven-year-old.

### Required Simulations And Gates

Thresholds marked `PROVISIONAL` must be calibrated from E0/P1 human data before
becoming release law.

| Area | Metric | Gate |
|---|---|---|
| Playability | Canonical reachability solver | 100% of accepted transitions have a valid control path plus mode safety margin |
| Impossible plans | Accepted plan failures in exhaustive small-graph checks and >=1,000,000 generated plans | 0; any failure blocks change |
| Determinism | Repeated seed/plan/input digest | Bit-exact score, rewards, state transitions; position within declared engine tolerance |
| Collision fairness | Visible-to-logical inset, tunneling, contact order, near-miss fixtures | 100% fixture pass; no frame-rate-dependent contact |
| Reaction demand | Required response time by beat/mode | No accepted beat below a conservative design floor; `PROVISIONAL` initial review floor 500 ms standard, 750 ms paced. Percentile claims require a separately powered study. |
| Speed curve | Acceleration, readable distance, camera horizon | No telegraph budget violation; slope/breather constraints pass |
| Difficulty | Axis values and bot completion distribution | Within rhythm/mode bands; no more than two axes escalate simultaneously unless exception is approved |
| Spawn distribution | Type, transition, lane/height, cooldown | 99% confidence interval contains authored target; no prohibited adjacency |
| Rewards | Currency/item grants and route bias | Exact fixed rewards; random-placement aggregate within 1% of authored expectation over >=100,000 runs |
| Power-ups | Appearance, duration, overlap, exit | Frequency within authored band; no illegal overlap/state leak; every forced interruption returns valid state |
| Economy | Unlock time distribution by bot/style | No negative balance, duplicate grant, unreachable unlock, or >10% deviation from approved pacing bands |
| Repetition | Exact plan duplicate and chunk n-gram recurrence | No exact duplicate inside cooldown; repeated 3-gram rate <5% across 10,000 balanced runs unless authored refrain |
| Meaningful variety | Semantic signature diversity | Each claimed distinct plan differs on >=2 player-visible dimensions; effective count reported separately from combinations |
| Similarity | Pairwise structural/perceptual distance | p10 above catalog threshold; manual review of closest 1% |
| Story moments | Template occurrence/cooldown | Per-template authored range; no moment repeats inside cooldown or exceeds per-session cap |
| Save/progress | Transaction replay, migration, corruption | No duplicate/lost durable reward; all golden versions migrate; corrupt optional model data cannot corrupt progress |
| Offline | Network-denied end-to-end | 100% core flow pass |
| Accessibility | Each assistance/settings matrix | Every declared plan valid in each eligible mode; required cue always duplicated |

Statistical reports include sample count, seed strategy, distribution summaries,
confidence intervals where appropriate, baseline delta, and practical threshold.
Large `N` does not rescue a tiny or irrelevant effect.

### AI Evaluation

| Metric | Required gate before player test |
|---|---|
| Schema-decodable drafts | >=99.9% over frozen fixture suite; 100% safe fallback |
| Full validation acceptance | Baseline established; rejected drafts never execute |
| Forbidden identifier/field leakage | 0 accepted |
| Playability/economy/safety validator bypass | 0 possible by construction |
| On-device p50/p95 proposal latency | `PROVISIONAL` <=1.0 s / <=2.5 s after prewarm; never blocks play |
| Deadline fallback | 100% within 50 ms after deadline decision |
| Crash/session corruption rate | 0 in stress suite |
| Semantic variety | Non-inferior to Level 2 and practically better on preregistered metric |
| Energy/thermal | <=5% additional 15-minute energy impact versus Level 2 on each floor cohort, or explicit rejection |
| Age/safety fixtures | 100% rejected or mapped to authored safe content; no free text reaches child |
| Player outcome | Practically meaningful blind crossover improvement over Level 2, not merely reviewer preference |

### Model Upgrade Gate

```text
archive old cohort inputs, outputs, metrics, and artifacts
  -> run prompt/schema/tool fixtures on the available candidate cohort
  -> compare validity, plan metrics, safety, latency, energy, refusals
  -> run multi-bot gameplay simulations for accepted plans
  -> blind human review of closest and worst deltas
  -> limited opt-in internal/playtest release
  -> ship app update with explicit artifact versions or disable Level 3 for that cohort
```

Version prompts, instructions, schemas, tools, generation options, catalog
digest format, evaluation fixtures, expected invariants, and fallback policy.
Golden text equality is used only where exact text is required; structured and
gameplay invariants are the primary oracle. Apple's prior system model generally
cannot be frozen or restored after an OS update; rollback means Level 2 fallback,
not an implied rollback to an unavailable model.

### Regression Report

Every gameplay-system pull request must attach:

- changed rules/content/director versions;
- simulation counts and seed provenance;
- baseline/current distribution deltas;
- failed and waived thresholds, with owner and expiry;
- closest-similarity examples;
- representative replay traces;
- performance/energy delta when runtime work changes;
- rollback revision and save/content compatibility.

## M. Human Fun Testing Protocol

### Purpose

Determine whether play is enjoyable, understandable, fair, memorable, and worth
repeating. Do not optimize children toward longer or more frequent use.

### Ethics And Recruitment

- Guardian informed consent and child assent are required.
- State that the game is being tested, not the child.
- The child may stop, switch, skip questions, or delete a recording at any time.
- No compensation depends on performance or continued play.
- Collect age band only when needed; never names in analysis artifacts.
- Default to observer notes. Video/screen recording is separate, optional
  consent with a deletion date no later than 30 days after scoring and access
  restricted to named study roles.
- The study coordinator assigns a random participant code; the child does not
  enter a name or choose an identifier.
- Store contact/scheduling data, participant-code mappings, consent records,
  recordings, observer notes, and analysis in separate encrypted locations with
  role-limited access. No raw study artifact enters the source repository.
- Before recruitment, the protocol declares deletion dates for mappings,
  recordings, notes, and participant-level analysis. Delete them no later than
  90 days after the E0 decision; retain only the aggregate decision report.
  Consent records follow the separately disclosed legal retention schedule.
- Sessions are capped at 20 minutes with a visible natural end.
- Moderator never urges “one more” and never uses loss-framed language.
- Use adult/internal tests first to remove obvious defects before child exposure.

### Session Structure

1. Parent sees purpose, data handling, stop rights, and neutral instructions.
2. Moderator uses the assigned participant code and tells the child: “Try this
   game. You can stop or change at any time. I am testing the game, not you.”
3. Moderator launches a randomized candidate and remains silent unless safety or
   a technical blocker requires intervention.
4. Observe first action, rule understanding, failures, retries, strategies,
   ignored features, reactions, and stopping.
5. After the second technically valid attempt, leave retry available for a
   preregistered 10-second silent window. If no retry starts, offer the next
   candidate neutrally; counterbalance order across participants.
6. After all candidates, ask behavioral recall questions without praise cues.
7. Offer a free choice among candidates, another neutral activity, or stopping.
8. Parent receives a brief debrief and a deletion option covering recordings,
   mappings, notes, and participant-level analysis. Disclose any consent-record
   retention that cannot be deleted for a stated legal reason.

### Observation Sheet

Record events, not inferred mental states:

- time to first meaningful action;
- moderator intervention and reason;
- first three failures and whether the child could identify cause;
- repeated route/technique attempts;
- voluntary replay count during the fixed silent retry window before another
  option is offered;
- immediate replay after failure versus confusion/withdrawal;
- features and routes ignored, repeatedly selected, or explained;
- spontaneous laugh, exclamation, call-over, or attempt to show someone;
- concrete next goal stated without suggestion;
- free choice after exposure to all candidates;
- stopping behavior and any distress/obligation language;
- event remembered after a short delay and, in later phases, a later day.

Never label a participant “risk-taking,” “low skill,” “attention deficient,” or
similar. Code only observed choices under the offered conditions.

### Interpretation

**Healthy replayability:** replay follows understood failure, experimentation,
mastery, discovery, or self-chosen goal; stopping remains comfortable.

**Engagement maximization:** the system prolongs play through uncertainty,
loss, scarcity, social pressure, interruption, or escalating rewards. Such a
signal is a defect even if session duration increases.

Report `N`, age bands, order, build, facilitator interventions, missing data,
and Wilson 95% intervals for proportions. Small samples are directional. Quotes
are paraphrased unless explicit consent allows exact anonymous quotation.

### Fun Gate Evidence

Automated evidence can block a candidate. Only observed play can pass the Fun
Gate. Parent purchase intent is collected separately from child preference and
is not treated as a proxy for fun.
