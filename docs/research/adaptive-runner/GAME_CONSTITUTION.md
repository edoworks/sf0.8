# Game Constitution

Status: `CANDIDATE_PERMANENT_PRINCIPLES`
Authority: research package until a successful experiment and product assignment

These laws survive changes in engine, content, business model, director, and
model provider. A product PRD may make them stricter but may not weaken them.

## Player Experience

1. The first meaningful action occurs within ten seconds of starting play.
2. Controls respond immediately and consistently. Input buffering, coyote time,
   and collision forgiveness are tuned from observation, not folklore.
3. Movement must be enjoyable before scores, rewards, progression, collection,
   adaptation, or AI are added.
4. Failure must be understandable, attributable, and fair. The game shows what
   happened without blame or humiliation.
5. Restart is immediate. Failure never creates a sales opportunity.
6. Difficulty cannot substitute for novelty, and speed cannot be the only
   difficulty axis.
7. Every run has an intentional rhythm: teaching, tension, choice, breather,
   escalation, and payoff as appropriate to its duration.
8. Power-ups materially change decisions or movement. A larger number alone is
   not a power-up.
9. Surprise must obey established world rules. Randomness cannot excuse
   incoherence or unfairness.
10. Every session offers a clean stopping point. The game never implies that a
    player is failing friends, losing status, or wasting rewards by stopping.

## Correctness And Generation

11. No obstacle arrangement may be impossible for its declared movement and
    assistance mode.
12. Physics, collision, spawning, scoring, economy, purchases, saves, and
    achievements are deterministic engine responsibilities.
13. Authored content is the vocabulary. Procedural systems compose that
    vocabulary; they do not invent executable behavior.
14. Every run is reproducible from content version, rules version, seed, plan,
    and input trace within documented tolerances.
15. Generated or adaptive proposals are untrusted input and pass schema,
    allow-list, bounds, rhythm, difficulty, economy, safety, and simulation
    validation before execution.
16. Validation failure selects a known safe plan. It never blocks play.
17. The game remains excellent when all model-backed features are unavailable.
18. A model upgrade never silently changes rules, scores, economy, content
    eligibility, or difficulty policy.

## Adaptation And Intelligence

19. Adaptation serves agency, accessibility, discovery, and variety. It does not
    optimize session duration, spending, return pressure, or stopping resistance.
20. Stable rules remain stable. Hidden dynamic difficulty, collision rescue,
    reward-odds changes, and unannounced speed manipulation are prohibited.
21. Assisted and standard records are clearly distinguishable when assistance
    changes comparability. Assistance is never stigmatized.
22. Behavioral evidence is limited to observed task selections needed to choose
    content. The system does not construct a psychological profile.
23. Selection-evidence confidence must be explicit. Low confidence causes exploration
    among safe plans, not confident personalization claims.
24. Players and parents can inspect, disable, and reset adaptation without
    losing purchases or core progress.
    Internal task-selection weights are not presented as traits about the child.
25. AI proposes; deterministic systems validate; the engine executes.
26. Every AI feature has a non-AI baseline, measurable benefit, deterministic
    fallback, and kill criterion. Failure to beat the baseline removes it.

## Children, Privacy, And Safety

27. The game minimizes data by design: no account, chat, advertising profile,
    third-party analytics, or cross-app tracking.
28. Production persists no raw gameplay event stream beyond the active run.
    Derived task-selection evidence remains protected on device and out of backups.
29. The game must not infer health, diagnosis, neurotype, intelligence, emotion,
    identity, protected characteristics, household attributes, or spending
    susceptibility.
30. Child-directed text, images, audio, characters, and combinations are age
    reviewed. Model guardrails do not replace product-specific review.
31. Purchases, external links, privacy controls, and destructive resets are in a
    designated adult area with an appropriate parental gate.
32. A parental gate is not treated as legal consent for data collection.
33. Core play works offline. Any future network feature must justify each datum,
    recipient, retention period, and child benefit before implementation.
34. Human playtests require guardian consent, participant assent, minimal
    recording, anonymized notes, and a right to stop without penalty.

## Accessibility And Wellbeing

35. Necessary information is never conveyed by color, sound, haptics, motion,
    or text alone.
36. Reduced motion, reduced flash, independent audio/haptic controls, readable
    contrast, scalable text, and non-audio telegraphs are first-class behavior.
37. Assistance widens access without silently changing identity or commercial
    treatment.
38. The game measures healthy replay signals, not compulsive engagement. Longer
    sessions are not inherently better.

## Economy And Trust

39. No advertisements, loot boxes, paid randomness, consumable boosts, energy,
    paid revives, pay-to-skip frustration, or purchasable score advantage.
40. Prices and entitlements are understandable to a parent before purchase.
41. Paid content is permanent, restorable, substantial, and never required to
    repair intentionally degraded play.
42. Monetization must not damage game balance, stopping points, or player dignity.

## Factory And Release

43. Every improvement names a hypothesis, expected effect, implementation
    boundary, automated verification, human test, regression risk, and rollback.
44. Statistical simulation is required for gameplay-system changes, but no
    automated metric may claim that a game is fun.
45. Rejected hypotheses remain recorded so future agents do not resurrect them
    without new evidence.
46. Content and rules are versioned independently from prompts, schemas, tools,
    models, and evaluation sets.
47. A clean build or passing unit test is progress, not evidence of product value.
48. Failure at an earlier gate blocks investment in later gates:
    `FUN -> REPLAYABILITY -> RETENTION -> VARIETY -> PERSONALIZATION -> AI VALUE -> SCALE`.
49. The smallest correct system is preferred. Cleverness, feature count, and AI
    sophistication are not quality metrics.
50. If the core game is not sufficiently fun, the project stops or changes game
    concept. Progression and AI may not be used to conceal that failure.
