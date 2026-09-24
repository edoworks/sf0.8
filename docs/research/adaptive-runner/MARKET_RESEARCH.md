# Executive Assessment And Market Research

Issue: [prior work, market, and child mechanics](https://github.com/edoworks/sf0.8/issues/136)

Cutoff and retrieval date: `2026-09-23`

## A. Executive Assessment

### Verdict

**Continue only to a small movement-first experiment. Do not fund the master
roadmap yet. Confidence: moderate.**

An excellent deterministic runner is plausible. A commercially meaningful new
runner, durable child replay, and added value from personalization are all
unproven. Existing Foculoom implementations demonstrate the ability to build
features; they do not demonstrate voluntary replay or willingness to pay.

### Strongest Aspects

- One-input action games can be understood quickly while retaining expressive
  skill through timing, route choice, momentum, and risk [M1-M6].
- Deterministic seeds make practice legible, bugs reproducible, and simulation
  trustworthy.
- A no-ad, no-tracking, offline product can create parent trust, though this is
  partly expected conduct in Apple's Kids Category rather than a gameplay moat
  [A12-A14].
- Foculoom already has reusable runner mechanics, deterministic replay ideas,
  playtest rubrics, and local persistence patterns [P1-P4].

### Weakest Assumptions

- **“Endless” creates replay.** It can create repetition instead.
- **Personalization creates delight.** It can erase stable rules, narrow
  discovery, or make scores incomparable.
- **Children's current viral interests transfer to a standalone premium game.**
  Roblox and Minecraft derive value from creation, social context, ownership,
  and content scale that a runner cannot copy [M8-M9].
- **More systems fix boredom.** Previous builds already contain missions,
  achievements, levels, worlds, collectibles, and progression without evidence
  that the movement itself earns another run [P1-P3].
- **A premium position implies premium demand.** Alto proves the format exists,
  not that an unknown runner can acquire enough paying families [M6, M16].

### Largest Risks And Opportunity

The largest risk is a polished, technically sophisticated game whose first two
minutes feel interchangeable with existing runners. The largest opportunity is
a compact movement toy in which a child recognizes personal improvement,
discovers authored surprises, forms a favorite character or route, and can tell
another person about an event that arose from play.

The product becomes exceptional if movement, world rules, and authored systems
combine into memorable situations while preserving fairness. It becomes
forgettable if novelty is palette changes, difficulty is mostly speed, rewards
replace mastery, or “AI” is the only sentence distinguishing it.

## Prior Foculoom Evidence

### FACT

- `endless-runner-template` implements one-touch jumping, double jump, coyote
  time, variable jump height, hazards, health, shields, stars, combos, authored
  patterns, ten YAML levels, missions, achievements, themes, audio, haptics,
  settings, onboarding, and local persistence [P1].
- Its `AGENTS.md` names `docs/PRD.md`, `docs/PHASES.md`, and several validation
  documents as canonical, but those files are absent [P1].
- Skiplet's draft PRD proposed three different value hypotheses: precision,
  run-rescue-build, and spectacle/transformation. Its validation plan correctly
  required observed voluntary replay and warned that small samples are
  directional [P2-P3].
- No reviewed artifact demonstrates that a prior runner passed a controlled fun
  gate with children. Automated tests establish behavior, not enjoyment.

### INTERPRETATION

The recurring failure was not inability to implement a runner. Product
definition, evidence continuity, and sequencing allowed feature breadth before
the core movement hypothesis was proven. This is a contributing-factor finding,
not a claim that one implementation defect caused boredom.

### Recurrence Guard

No content, progression, procedural, personalization, or AI phase may begin
until the preceding behavioral gate passes. A compiler, test suite, feature
count, or founder approval cannot substitute for observed voluntary play.

## B. Evidence-Backed Findings

### Evidence-Informed Design Interpretations

Except where a cited developer directly states intent, this table is
`INTERPRETATION` or `HYPOTHESIS`. Product pages establish that a mechanic exists;
they do not establish that it caused durability, retention, or child appeal.

| Mechanism hypothesis | Evidence | Interpretation for Foculoom |
|---|---|---|
| One-input depth | Jetpack Joyride's developer postmortem describes a one-button game, short sessions, and layered rewards [M1-M2]. Alto uses one-touch movement and trick mastery [M6]. | Prototype one verb with timing and trajectory depth before adding gestures. |
| Readable danger | Crossy Road, Alto, and Snake create near misses through visible geometry [M5-M7]. | Collision, telegraphing, and recovery must remain predictable. Reward near misses without secretly changing collision. |
| Immediate replay | Fast retry is present across the compared arcade products [M1-M6]; causal retention evidence was not found. | Test a restart target under 500 ms and one actionable comparison. |
| Layered goals | Missions, personal bests, collection, and route discovery coexist with the core score loop [M1-M6]. | Goals should teach existing possibilities, not require grind or intentionally poor play. |
| Mechanical transformations | Jetpack Joyride vehicles temporarily change the interaction rule [M1-M2]. | A power-up should change play, not merely increase a number. Omit from the first movement test. |
| Atmosphere | Alto differentiates with flow, animation, sound, and place rather than content volume [M6]. | Art and audio can be product value, but polish must not hide weak input feel during E0. |
| Failure with progress | Hades and Vampire Survivors pair runs with persistent story or unlocks [M10-M11]. | Preserve accomplishments after fair failure, but do not add a dense upgrade economy to the prototype. |
| Player-authored goals | Minecraft foregrounds creation, exploration, and persistent worlds [M8]. | Offer route, challenge, and collection choices; a runner cannot imitate Minecraft's construction scope. |

No primary evidence establishes that these mechanics caused commercial
durability or child replay. No primary evidence establishes a universal ideal session length. The proposed
30-120 second novice run and satisfying five-minute visit are hypotheses, not
market facts.

### Why Children May Return

General game-motivation research associates competence, autonomy, and
relatedness with enjoyment and future play motivation, but it is not a causal
study of ages 6-12 in runners [M17]. The candidate therefore treats these as
testable mechanisms:

| Driver | Healthy expression | Failure mode |
|---|---|---|
| Mastery | Same rule, visible improvement, achievable technique | Opaque scaling or humiliation |
| Autonomy | Route, character, and self-chosen goal | Infinite task pressure |
| Curiosity | Foreshadowed secrets and rare authored interactions | Random reward compulsion |
| Ownership | Earned collection recording accomplishments | Duplicate draws and rarity inflation |
| Expression | Recognizable character and play style | Paid power or status anxiety |
| Surprise | Rule-consistent, infrequent world events | Unfair exceptions or incoherent randomness |
| Relatedness | Family turn-taking or shared seed | Public chat, strangers, social obligation |
| Humor | Physical consequences and absurd combinations | Meme copying or generated unsafe dialogue |

### Multiple Timescales Of Fun

| Timescale | Change | Player reason | Anticipation/mastery/surprise |
|---|---|---|---|
| 1-5 seconds | Input, jump arc, landing, collect, near miss | Action feels good now | Immediate control causality and multisensory feedback |
| 10-30 seconds | First route decision and micro-pattern | “I see how this works” | Teach then remix one rule; first expressive choice |
| 30-90 seconds | Rhythm arc and one memorable event | Complete mini-story | Tension, breather, escalation, payoff |
| 2-5 minutes | Reattempt, compare, discover alternate line | “I can beat that” | Stable course supports learning; one curiosity hook |
| 5-15 minutes | Three challenges or a small collection goal | Self-chosen session arc | Rotate goals without obligation; clear stopping point |
| Daily | Deterministic optional challenge | Fresh comparison | No streak and no expiring loss |
| Weekly | Authored remix or personal mastery target | Return to a meaningful goal | New combination, not just faster numbers |
| Long term | World rules, earned characters, remembered rivals/secrets | Ownership and identity | New affordances and callbacks after validated demand |

## C. Competitive Mechanic Matrix

| Product | Core mastery | Replay layer | Durable lesson | Do not copy |
|---|---|---|---|---|
| Jetpack Joyride | One-touch altitude and hazard reading | Missions, vehicles, gadgets | Temporary rule changes create run texture | Economy pressure, protected characters, audiovisual expression |
| Temple Run | Swipe/tilt reaction vocabulary | Coins, power-ups, characters | Legible obstacle verbs | Commodity three-lane chase structure |
| Subway Surfers | Lane timing and route reading | World Tour, events, characters | Frictionless input and expressive collection | Live-ops burden, boosts, mystery rewards, branded expression |
| Crossy Road | Discrete spatial commitment | Score, characters, secrets | Every move is an understandable decision | Voxel-road identity and random duplicate collection |
| Alto | Landing and trick flow | Goals, unlocks, atmosphere | Premium value can be feel and place | Snowboarding identity and presentation |
| Snake variants | Steering, growth, spatial greed | Survival and competition | One rule can produce emergent stories | Network dependency, ads, skin economy |
| Hades/roguelites | Build and encounter mastery | Narrative and persistent unlocks | Failure can reveal progress | Combat/content scope for MVP |
| Minecraft | Creation, exploration, survival | Persistent authored goals | Ownership and autonomy drive return | Attempting to mimic world or UGC scale |
| Roblox | Experience-specific | Social graph and creator supply | Cultural context and expression matter | Open UGC, chat, recommendation loops |

**Table stakes:** immediate controls, fair failure, fast restart, personal best,
clear feedback, useful sound settings, offline reliability, and accessibility.

**Potential differentiator:** authored deterministic runs that remix validated
chunks into physical comedy, callbacks, rivals, secrets, and alternate routes,
with adaptation limited to selecting among safe plans rather than changing game
rules.

**Unexploited opportunity hypothesis:** a parent-trusted premium arcade game
could combine mastery, story-worthy systemic events, and local adaptation
without ads, accounts, feeds, streak loss, or live-ops obligation. No evidence
yet shows enough families will pay for it.

## Mechanics Foculoom Must Not Reproduce

- Loot boxes, paid random rewards, duplicates, rarity inflation, or hidden odds.
- Premium-currency conversion, paid revives, score multipliers, consumable
  boosts, energy, pay-to-skip missions, or frustration sold as relief.
- Interstitial ads, behavioral advertising, or third-party child profiling.
- Loss-framed streaks, expiring rewards, countdown pressure, or obligation
  notifications.
- Infinite task lists designed to prevent a clean stop.
- Public chat, stranger messaging, public location, or open UGC.
- Hidden adaptation of collision, speed, timing, reward odds, or score rules.
- Direct score comparison across materially different assistance rules.
- Protected characters, worlds, catchphrases, music, visual language, or level
  expression from comparators.

FTC enforcement over Fortnite's alleged unwanted charges and the UK regulator's
game principles reinforce the need for clear commercial information and no
pressure exploiting children's inexperience [M21-M22]. This is design guidance,
not a legal conclusion.

## D. Product Thesis

### Target Player

Primary: a child approximately 7-11 who likes immediate action, visible
improvement, absurd physical outcomes, collection, and discovery. Secondary: a
parent buying a complete, offline, respectful game. Ages 6 and 12 are important
test edges, not one homogeneous persona.

### Player Fantasy

**“I am a nimble little troublemaker who learns the world's tricks, takes the
riskier path, and leaves each run with a story only I caused.”**

### Experience Promise

- **30 seconds:** movement is legible, tactile, and expressive; the player makes
  one real route decision and sees one surprising physical consequence.
- **5 minutes:** the player retries voluntarily, improves on a stable challenge,
  discovers a route or secret, and chooses a next goal.
- **30 minutes:** several short visits reveal different rhythm arcs and
  interactions; the player begins to favor a style and owns visible evidence of
  accomplishments.
- **Long term:** worlds gain new rules, characters express identity, old events
  return in changed contexts, and rare combinations create stories without
  requiring attendance.

### Reason To Replay And Care

Replay is earned by the thought, “I know what I want to try differently,” not
“the reward timer told me to return.” Care comes from a favorite way of moving,
earned artifacts, discovered places, recurring rivals, and remembered events.

### Differentiation

The differentiation is **masterable authored systems that remember play without
changing the rules**. AI and personalization are implementation candidates, not
the product proposition.

## Monetization Assessment

| Model | Trust | Suitability | Commercial evidence | Disposition |
|---|---|---|---|---|
| Paid upfront | Highest clarity | Strong | Alto remains a paid precedent; demand for new IP unknown [M6] | Preferred launch hypothesis after fun validation |
| Free trial + permanent unlock | Clear if parent-gated | Strong | Super Mario Run warns that broad reach need not convert profitably [M16] | Best fallback/test model |
| Expansion packs | Clear when substantial and permanent | Acceptable | Attach rate unknown | Post-demand only |
| Cosmetic purchases | Can fragment parent trust | Weak for young children | No necessity demonstrated | Defer |
| Subscription | Ongoing value burden and cancellation friction | Poor for one runner | Catalog services exist [M19-M20] | Reject for standalone game |
| Ads/consumables | Conflicts with trust and game constitution | Poor | Common in competitors, not evidence of product quality | Reject |

Premium is commercially possible but not forecastable. Public sources do not
provide reliable child-runner conversion, retention, refund, or willingness-to-
pay distributions. Any price, including `$4.99-$7.99`, is an experiment input,
not a market fact.

## Counterevidence And Unknowns

- The strongest runners launched in an earlier mobile discovery environment.
- Major comparators have accumulated audiences, famous IP, platform featuring,
  social context, or sustained live operations.
- Minecraft and Roblox may dominate repeat attention because of creation,
  friends, and content breadth that this product intentionally excludes.
- Determinism can become repetitive; procedural variation can destroy learning.
- No evidence establishes child-specific retention, an ideal run duration,
  premium conversion, or the superiority of adaptive runs.
- Closure notices for Crash `On the Run` and Sonic Runners do not establish
  causal design failures [M14-M15].

## Decision Implication

Do not implement progression, personalization, or AI. Build the smallest
movement comparison in [ROADMAP.md](ROADMAP.md). Stop if no movement candidate
is fun without rewards, content rotation, or an adaptive director.
