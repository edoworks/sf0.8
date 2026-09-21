# Continuous Human Competence in the AI Era

Decision dossier for Foculoom issue #50

Status: `RUN EXPERIMENT`
Scope: evidence review and cheapest falsifiable adult experiment; no product
authorization, external recruitment, publication, purchase, or integration.
Cutoff and retrieval date: 2026-09-20

## 1. Executive Finding

The strongest defensible finding is narrower than the original narrative:

- AI is already materially present in software-development work. This is
  `CONFIRMED` for adoption, but not for every claimed productivity or labor
  market effect.
- AI-assisted output can improve short-term task performance while reducing
  unaided performance or cognitive effort in some settings. This is
  `PARTIALLY SUPPORTED`, not proof of general skill atrophy.
- Retrieval practice, spacing, explanation, transfer tests, and calibration
  have credible learning-science foundations. A deliberate AI-skeptic exercise
  is plausible, but its incremental value over ordinary practice is
  `UNPROVEN`.
- Existing products already cover tutoring, coding practice, interview
  preparation, flashcards, adaptive practice, and AI-assisted learning. The
  proposed job is not visibly empty.
- No local or external evidence found here demonstrates a repeated buyer pain,
  adult software-engineer demand, daily retention behavior, willingness to pay,
  or a Foculoom-specific moat.

The appropriate next step is therefore one small behavior-and-learning
experiment, not an app, platform, curriculum, integration, subscription, or
software-engineering product. The experiment should be killed if it cannot
show an incremental effect over ordinary AI-assisted learning or if adults do
not repeatedly use it without prompting.

### Delivery constraint update

The Customer Zero has supplied direct evidence that a desktop-only workflow is
not acceptable: available time is fragmented across two jobs, parenting, and a
spouse, and the preferred context is mobile and on the go. This establishes a
delivery constraint, not a native-app requirement. The first experiment must
therefore be mobile-first and resumable, while treating native iOS, a ChatGPT
surface, a Claude surface, a skill, and a responsive web/PWA as competing
delivery hypotheses.

The cheapest initial surface is an existing mobile chat or responsive static
flow. Native device features become justified only if observed behavior shows
that push notifications, voice input, offline operation, camera access, or OS
integration changes completion or retention materially.

### Customer Zero update

The founder has volunteered as an admissible first Customer Zero in two roles:

1. **Software engineer:** builds software rapidly with AI, has difficulty
   keeping up with understanding the resulting code, and periodically needs to
   prepare for interviews and refresh fundamentals.
2. **Father:** may have a parent-side need to know whether a child understands
   something independently rather than merely completing AI-assisted work.

These are two different jobs, triggers, alternatives, outcomes, and buyers.
They must not be treated as evidence that one product serves both. The engineer
track can begin as a self-observation and learning-feasibility experiment. The
father track can begin as a parent workflow observation. A child is not the
initial efficacy population: any child observation requires the existing consent,
assent, minimization, and stop rules, and adult evidence should be collected
first.

## 2. Claim-Evidence Matrix

Ratings describe the claim as stated, not a weaker nearby claim.

| # | Claim | Rating | Evidence and limitation |
|---|---|---|---|
| 1 | AI is materially changing software-development workflows. | CONFIRMED | Stack Overflow's 2025 survey reports 84% of respondents using or planning to use AI in development and 51% of professional developers using it daily (26,004 professional-developer responses; self-report). This establishes adoption, not improved outcomes. [S1] |
| 2 | Software engineers are expected to use AI professionally. | PARTIALLY SUPPORTED | Adoption surveys and commercial coding tools establish professional availability and use. They do not establish a universal employer mandate or a causal career requirement. HackerRank's 2025 report documents an active skills/hiring market, but vendor-sponsored survey data is not an employment census. [S2] |
| 3 | Technical hiring still frequently tests independent fundamentals. | PARTIALLY SUPPORTED | HackerRank, Educative, Codecademy, LeetCode, Codility, and CodeSignal continue to market coding, algorithms, system design, and technical assessments. Product availability is evidence of category supply, not frequency across employers. [S2, S8-S13] |
| 4 | Developers perceive a mismatch between assessments and real work. | PARTIALLY SUPPORTED | HackerRank's developer-skills research and the continuing market for real-world-question and interview products support perceived assessment friction. The available evidence is primarily vendor research and self-report; no representative causal estimate was found. [S2, S9-S13] |
| 5 | Increased AI usage can reduce practice of underlying skills. | PARTIALLY SUPPORTED | Bastani et al. found unrestricted GPT-4 assistance improved in-practice math performance but worsened later unaided performance; a tutor-style condition avoided that harm. Microsoft Research found knowledge workers reported reduced cognitive effort, with confidence in AI associated with less reported critical-thinking effort. Both are bounded and do not prove universal decay. [S3, S4] |
| 6 | Reduced practice produces meaningful skill degradation. | UNPROVEN | Learning science predicts that retrieval and spacing matter, but no strong longitudinal software-engineering study was found that isolates AI delegation, measures foundational-skill decay, and connects it to workplace outcomes. Short-term productivity studies cannot answer this. [S5-S7] |
| 7 | Foundational knowledge improves detection of incorrect AI output. | PARTIALLY SUPPORTED | Verification logically requires an oracle, tests, domain knowledge, or reliable procedures. Automation-bias and critical-thinking evidence support the risk of over-trust. Direct experimental evidence connecting retained software fundamentals to AI-error detection remains missing. [S4, S14] |
| 8 | Existing AI tutors adequately address the problem. | UNPROVEN | ChatGPT Study Mode, Khanmigo, Brilliant Koji, and other tutors explicitly use guided questions, mastery checks, and feedback. Their feature claims do not establish durable independent competence or robust AI-output verification. [S15-S17] |
| 9 | Existing interview-preparation products adequately address it. | UNPROVEN | LeetCode, HackerRank, CodeSignal, Educative, Codecademy, and Exercism offer practice and assessment. They optimize different jobs and do not clearly provide continuous competence maintenance during AI-assisted work. Adequacy requires outcome comparison, not feature comparison. [S8-S13] |
| 10 | People care enough to maintain independent competence through changed behavior. | UNPROVEN | Survey sentiment and product use show interest in learning and AI. No direct evidence was found for repeated, unprompted, daily independent-recall practice by working engineers. |
| 11 | People or organizations might pay to solve this problem. | UNPROVEN | Existing paid learning, interview, coding, and enterprise-training categories prove spending exists nearby. They do not prove payment for this job, a buyer, price, retention, or acceptable acquisition economics. |

No claim is made that AI caused software-engineering employment changes. The
available evidence does not establish that causal relationship.

## 3. Problem Evidence

### Observed evidence

- AI use is widespread among surveyed developers, with daily professional use
  reported by a large respondent group. [S1]
- In a randomized study of approximately 1,000 high-school mathematics
  students, unrestricted GPT-4 assistance improved practice performance but
  harmed later unaided performance; a constrained tutor condition produced a
  better learning result than unrestricted assistance. [S3]
- In a CHI 2025 survey of 319 knowledge workers, respondents reported reduced
  cognitive effort on AI-assisted tasks. Higher confidence in AI was associated
  with less reported critical-thinking effort; the study is correlational and
  self-reported. [S4]
- In one randomized study of 16 experienced open-source developers completing
  246 tasks, early-2025 AI tools increased completion time by 19% despite
  participants predicting a reduction. The result is important counterevidence
  to simplistic productivity narratives, not evidence of skill decay. [S18]
- Retrieval practice and distributed practice have substantial experimental and
  meta-analytic support as general learning mechanisms. [S5, S6]

### Inference

The evidence supports a risk condition: AI can make assisted performance look
better than unaided capability, and confidence in assistance can reduce effort
spent checking. It does not establish that working engineers are currently
losing foundational competence or that they would purchase a remedy.

### Hypothesis

Repeated independent recall followed by controlled AI-error inspection may
improve delayed independent performance and error detection more than ordinary
AI-assisted practice.

### Speculation to reject

- AI is the primary cause of software-engineering job losses.
- Every engineer needs daily practice.
- Memorizing more facts is the right response to AI.
- A new app is required.
- Verification can be reduced to spotting hallucinations.

## 4. Counterevidence and Falsification

The strongest evidence against the opportunity is:

1. Structured AI tutoring can improve learning rather than degrade it. The
   proposed mechanism may be a property existing tutors already provide. [S3,
   S15-S17]
2. AI can increase immediate productivity and compensate for experience gaps.
   This may reduce the value of a separate maintenance product. [S19, S20]
3. Experienced developers may actively reason, inspect, test, and revise during
   AI-assisted work. AI use is not equivalent to passive delegation.
4. Flashcards and spaced repetition are mature, low-cost substitutes. Anki
   already schedules recall and supports large, user-created knowledge bases.
   [S7]
5. Existing coding education and interview products already sell practice,
   assessment, and technical fundamentals. [S8-S13]
6. The 10-minute daily habit may fail because professional engineers do not
   experience an urgent trigger outside interviews, incidents, certification,
   or role transition.
7. Deliberately flawed AI output may train suspicion or pattern matching rather
   than transferable verification.
8. Verification may be better handled by tests, type systems, static analysis,
   peer review, and domain-specific checklists than by human memory practice.
9. A successful learning intervention may still be non-monetizable because
   free AI tutors, Anki, documentation, and employer training are sufficient.
10. A competence-maintenance engine would likely be assembled from commodity
    scheduling, assessment, telemetry, and model APIs. No moat is established.

The experiment below is designed to kill the thesis if these counterclaims
hold.

## 5. Competitive Map

| Existing solution | Primary optimization | Relevant overlap | Evident gap, not yet a market gap |
|---|---|---|---|
| ChatGPT Study Mode | Guided learning, explanations, quizzes, reflection | Active participation, knowledge checks, personalization | No independent evidence here of durable transfer or systematic AI-error verification; product is a strong free/paid substitute. [S15] |
| Claude education features | General AI assistance and higher-education use | Explanation and collaborative work | No verified competence-maintenance outcome found in this review. [S16] |
| Khanmigo | Guided tutoring, teacher assistance, mastery-oriented help | Socratic questioning and not simply giving answers | Primarily broad tutoring, not specifically AI-output skepticism for working adults. [S17] |
| Brilliant Koji | Interactive tutoring and mastery assessments | Adaptive practice, coding/math fundamentals, progress tracking | Strong direct competitor to any interactive learning loop; vendor claims are not independent efficacy evidence. [S18] |
| Anki | Recall and spaced scheduling | Long-term memory maintenance | Requires users/content; does not natively model AI collaboration or flawed-output verification. [S7] |
| Quizlet | Flashcards, generated study guides, tests, games | Recall and short habits | Broad study workflow; no demonstrated verification-specific moat. [S19] |
| LeetCode/HackerRank/CodeSignal | Interview performance and technical assessment | Independent coding and assessment | Optimizes hiring/interview outcomes, not necessarily continuous workplace competence. [S8-S10] |
| Educative/Codecademy/Exercism | Structured technical learning and practice | Fundamentals, exercises, interview/system design | Existing content and practice make content production a weak differentiator. [S11-S13] |
| GitHub Copilot/Cursor and IDE tools | AI assistance, code generation, review, workflow speed | The normal AI-collaboration environment | Optimize assisted output, not intentionally preserved independent capability. This is a capability distinction, not proof of unmet demand. [S20, S21] |

The proposed category is therefore not unoccupied. The only plausible gap is a
narrow measurable outcome: whether controlled error inspection adds transfer or
calibration beyond ordinary tutoring, retrieval, tests, and code review.

## 6. Learning-Science Assessment

The proposed loop should be simplified to:

`RECALL -> PREDICT -> ATTEMPT -> USE AI -> INSPECT -> VERIFY -> EXPLAIN -> RETEST`

Credible components:

- Retrieval without seeing the answer tests access to knowledge rather than
  recognition. [S5]
- Spacing and delayed retesting support retention over time. [S6]
- Explanation and prediction expose misconceptions and metacognition.
- Transfer tasks test whether the learner can use a principle in a changed
  context rather than repeat a memorized item.
- Confidence before and after verification permits calibration measurement.

Unproven component:

- AI-skeptic mode, specifically controlled plausible defects, has a credible
  mechanism but no evidence here that it beats ordinary debugging, code review,
  tests, or errorful examples.

Preliminary competence boundary:

| Category | Software-engineering examples |
|---|---|
| MUST KNOW | Core language semantics used routinely; data representation; basic complexity vocabulary; security and correctness invariants; test and failure concepts. |
| MUST UNDERSTAND | Tradeoffs, assumptions, causal behavior, failure modes, concurrency/data consistency principles, and why a solution works. |
| MUST BE ABLE TO VERIFY | Expected behavior, edge cases, complexity claims, API existence, security properties, tests, observability, and whether evidence supports the claim. |
| SAFE TO DELEGATE | Boilerplate, syntax lookup, repetitive transformations, documentation search, test scaffolding, and candidate alternatives, provided the human retains the specification and verification duty. |

This boundary avoids the false objective of memorizing everything an AI can
retrieve.

## 7. Segment Analysis

| Segment | Trigger/pain | Current alternative | Frequency/consequence | Payment/distribution/measurability |
|---|---|---|---|---|
| Working software engineers | Suspected over-reliance, incident, role change, review failure | IDE tools, tests, peers, documentation, employer training | Potentially recurring; consequence is unknown | Reachable through communities/employers, but no direct payment evidence; measure independently. |
| Junior engineers | Need to learn while using AI; weak mental models | Mentors, courses, Stack Overflow, AI tutors | Frequent learning; skill and confidence consequences plausible | Existing crowded market; employer/university distribution possible; measure transfer. |
| Experienced engineers | Domain shifts, unfamiliar systems, AI review burden | Practice sites, reading, incidents, peer review | Episodic triggers; high consequence in critical work | Potential employer buyer, but opportunity cost and habit risk are high. |
| Interviewing/laid-off engineers | Hiring assessment preparation | LeetCode, HackerRank, CodeSignal, Educative, coaching | Triggered and urgent, not necessarily continuous | Existing willingness to pay is nearby; risk of collapsing into interview prep. |
| Engineering organizations | Safe AI adoption and confidence in output | Policies, tests, review, training, platform controls | Recurring organizational process | Plausible budget, but procurement and proof burden high; no buyer evidence. |
| Other knowledge workers | AI-mediated judgment and verification | Training, peer review, domain procedures | Broad but heterogeneous | Larger theoretical market, weaker initial measurability. |
| Regulated professions | Accountability for AI-assisted decisions | Formal supervision, continuing education, audit | High consequence and recurring | Potentially valuable but high legal/domain burden; not an initial population. |
| University students | Learning while using AI | Campus tutoring, ChatGPT, Khanmigo, courses | Frequent; academic integrity and learning consequences | Existing buyers and channels, but student/child safety and attribution burden. |
| Children/parents/educators | Learning and AI literacy | Schools, tutors, Khanmigo, Brilliant, worksheets | Recurring but safety-sensitive | Do not use as first population; existing local work shows direct evidence is absent. |

The best initial population is a consenting adult who already uses AI for
software work and has a near-term reason to maintain independent competence.
This is a test population, not a validated market segment.

The founder's engineer experience makes this population reachable and gives a
specific trigger that was previously missing: rapid AI-assisted construction
creates an understanding/review burden, while interviews create a separate
fundamentals-refresh trigger. This is direct Customer Zero evidence of a
personal problem, not prevalence or willingness-to-pay evidence. The first
experiment should test whether the problem changes behavior and performance,
not whether the founder can articulate it persuasively.

The founder's father experience is useful for identifying the parent-side job,
but it does not validate a child learning product. The first parent session
should record the parent's current workaround, time, uncertainty, and decision
without introducing a child-facing intervention.

## 8. Existing Foculoom Leverage

Reusable without creating new platform infrastructure:

- Issue #50 and its evidence-first education discovery artifact.
- `evidence-research` skill for claim-level provenance and counterclaims.
- Education protocol, participant script, observation sheet, results schema,
  and ingestion validator.
- Customer Zero discipline and the monetization ladder.
- Deterministic local-first experiment artifacts.
- Existing privacy, accessibility, safety, and evidence validators.
- ReuseFirst gate and Rule of Two: no shared learning engine until two real
  consumers independently require the same tested capability.

Genuine gaps:

- No adult software-engineer participant record.
- No direct observation of AI-assisted work and verification behavior.
- No validated item bank for software fundamentals and controlled AI defects.
- No evidence that a 10-minute daily intervention is retained.
- No payment, repeat-use, employer, or distribution evidence.

The existing child/family education kits should not be repurposed as evidence
for this adult hypothesis. They provide method infrastructure only.

## 9. Opportunity Boundaries

Do not build yet:

- A mobile app, browser extension, IDE plugin, ChatGPT/Claude integration, or
  LMS integration.
- A generic AI tutor, interview-preparation clone, coding curriculum, or
  subscription service.
- A child-facing product or open-ended model interaction.
- A mastery graph, adaptive-learning platform, telemetry system, or external
  API/SDK.
- A hiring assessment product or claims about employability.
- A platform based only on internal factory reuse.
- Any claim that AI caused employment losses or that the intervention prevents
  skill atrophy.

## 10. Monetization Evidence

Evidence that spending exists nearby:

- Paid/free tiers and institutional offerings exist across Brilliant, Quizlet,
  Educative, Codecademy, tutoring, interview preparation, and enterprise
  learning categories. [S7-S13, S18-S19]
- Technical hiring and interview preparation are established paid categories.

Evidence that this opportunity is monetizable:

- None found.

The buyer is unresolved. Candidates are the individual engineer, an employer,
an engineering manager, a university, or a regulated organization. Each has a
different trigger and proof requirement. “Would you pay?” is not admissible;
the next experiment must observe repeat use, referral, deposit, purchase, or an
employer-approved paid pilot.

## 11. Defensibility Analysis

Potentially compounding assets:

- A validated corpus linking specific AI defect types to human detection,
  confidence, repair quality, and delayed transfer.
- A reliable skill-decay or verification-risk measurement model.
- Domain-specific assessment and defect-generation quality.
- Distribution through an employer workflow where the intervention changes a
  measurable safety or review outcome.

Currently commoditized or weak:

- Spaced scheduling, flashcards, quizzes, chat tutoring, model access, and
  generic telemetry.
- Content libraries and interview questions.
- An API without unique data, workflow ownership, or validated outcome.

The only credible moat hypothesis is outcome data plus trusted domain-specific
measurement. It is not established and must not be built in advance.

## 12. Cheapest Falsifiable Experiment

### Hypothesis

Among adult software engineers who already use AI, 10 minutes per day of
independent recall followed by controlled AI-error inspection produces greater
improvement in delayed independent competence and analogous-error detection than
ordinary AI-assisted learning of the same material.

### Population

Twenty-four consenting adults, age 18+, who currently use an AI coding tool at
least weekly and have at least one year of software-development experience.
Recruitment and consent require human authorization. Do not recruit children or
collect employer-confidential code.

### Comparison

- Control: ordinary AI-assisted learning. Participants may use their normal AI
  assistant to study the same narrow topic and solve the same class of tasks.
- Intervention: recall, prediction, attempt, AI collaboration, controlled
  flawed-output inspection, repair, explanation, and scheduled retest.

Randomize 12/12 if feasible. If recruitment is too small, use a randomized
crossover with counterbalanced topic A/B and preregister the analysis before
starting.

### Scope

One narrow domain only: debugging and complexity of small Python functions.
Use six concepts and three defect families: off-by-one, incorrect complexity
claim, and missing edge case. Do not use live production code or model outputs
containing unsafe instructions.

### Duration and procedure

- Day 0: independent baseline: six recall items, two novel tasks, two flawed
  AI outputs; record accuracy, confidence, detection time, and explanation.
- Days 1-10: one 10-minute session per day. Intervention participants complete
  the full loop; control participants study/solve with their normal AI workflow.
- Day 5: unannounced independent probe with AI unavailable.
- Day 11: independent post-test with novel isomorphic tasks and analogous AI
  defects.
- Day 18: delayed retest without AI.

The experiment artifact can be a static document, form, or local CLI. No model
integration is required: the AI outputs are pre-authored and defects are
deterministic. This isolates the learning mechanism and avoids model drift.

### Customer-Zero feasibility pass

Before recruiting 24 engineers, run a bounded N-of-1 pass with the founder. It
is a feasibility and instrument test, not market or causal evidence:

- Select one real but non-confidential AI-assisted code task and one interview
  fundamentals domain.
- For 10 weekdays, alternate predeclared control and intervention sessions
  using the same 10-minute limit.
- Record independent recall, explanation, analogous-defect detection,
  confidence, time, and whether the session was started without a reminder.
- At the end of each week, complete an AI-free transfer check.
- Record the concrete current alternatives: tests/review, documentation,
  interview sites, notes, or doing nothing.

Run the pass from a phone wherever possible. Add delivery observations:

- whether the session completes without opening a computer;
- time from opening the experience to useful progress;
- whether the task can be resumed after interruption;
- context that must be re-entered;
- abandonment or correction caused by the mobile surface;
- whether notification, voice, or offline behavior would have changed the
  result.

The self-pass can expose bad item design, reveal whether the trigger is real,
and measure burden at negligible cost. It cannot establish population effect,
market size, or willingness to pay. It must not be used to declare success on
behalf of other engineers.

### Parent-side Customer-Zero observation

Run one adult-only observation before any child intervention:

- Record a recent situation in which the founder wanted to know whether the
  child understood independently.
- Record the current workaround, time, uncertainty, and decision made.
- Test whether the parent would independently request a repeatable check or
  pay/deposit for a future parent-facing artifact.
- Do not collect child identity, voice, image, school details, or work samples.

If a later child session is authorized, use the existing education protocol and
separate parent workflow evidence from child learning evidence.

### Delivery decision rule

- Keep the first experiment mobile web/chat if it supports the measured task
  with no material context loss.
- Test a native app only if mobile-web/chat failure is attributable to a device
  capability and the capability changes observed completion or repeat use.
- Test a ChatGPT/Claude integration only if the model surface reduces context
  switching without weakening privacy, provenance, or independent-performance
  measurement.
- Do not infer product demand from a preference for mobile access alone.

### Metrics

Primary:

- Delayed independent competence score on novel tasks.
- Analogous-defect detection rate without AI assistance.

Secondary:

- Repair correctness.
- Explanation rubric score.
- Detection latency.
- Confidence before and after verification.
- Calibration error.
- Session completion and unprompted return rate.
- AI-assisted performance, reported separately from independent performance.

### Success threshold

Proceed to a second experiment only if all are true:

- Intervention beats control by at least 15 percentage points on the pre-
  registered delayed independent composite, or shows a standardized effect
  large enough to justify replication with the observed sample uncertainty.
- Intervention beats control on analogous-defect detection, not only on
  trained item recall.
- At least 8 of 12 intervention participants complete 8 of 10 sessions.
- At least 4 participants independently request another session, refer a peer,
  or accept a paid/reimbursed follow-up. This is an early behavior signal, not
  proof of a market.

### Failure threshold

Kill or redesign the concept if any are true:

- No intervention advantage on delayed independent competence or analogous
  defect detection.
- Improvement exists only on trained items, self-reported confidence, or
  AI-assisted output.
- Fewer than 6 of 12 intervention participants complete 8 sessions.
- Participants prefer ordinary AI assistance and do not return without a
  reminder.
- Controlled defects reward superficial pattern matching rather than
  transferable verification.
- The experiment cannot measure independent competence separately from assisted
  performance.

### Cost and decision rule

Expected cash cost: near zero using static local materials; participant
compensation, if any, requires separate human authorization and budget.

Decision rule:

- Success: run one independently designed replication with a second domain and
  test whether an identifiable buyer pays.
- Learning-only success without behavior or payment: retain as research, do not
  build a product.
- Null result, harmful result, or weak adherence: kill the AI-skeptic product
  thesis and retain only the research record.

## 13. Kill Criteria

Kill the broader concept if:

- Two bounded adult experiments fail to improve delayed independent competence
  over ordinary AI-assisted learning.
- AI-error inspection adds no value beyond normal tests, debugging, code review,
  or retrieval practice.
- Users complete only when prompted and do not return voluntarily.
- Existing tutors or workplace tooling match the measured outcome at lower
  friction and cost.
- No participant demonstrates a real trigger, workaround dissatisfaction, and
  repeat-use request.
- No individual or organization takes a real payment, deposit, referral, or
  paid-pilot action after two opportunities.
- Acquisition or content QA cost makes the observed buyer signal uneconomic.
- The only viable positioning is interview preparation already served by
  incumbents.
- A platform requires generic infrastructure before a second independent
  consumer exists.

## 14. Evidence Gaps

- Longitudinal software-engineering skill decay under AI delegation.
- Direct causal link between retained fundamentals and AI-error detection.
- Adult participant behavior and adherence.
- Generalization across domains and defect types.
- Comparison with Anki, ordinary debugging, code review, and AI tutoring.
- Employer or individual buyer identity.
- Price, retention, distribution, and support economics.
- Whether competence maintenance is a standalone job or a feature of existing
  AI/coding tools.
- Whether software engineering is the best beachhead.
- Whether any data advantage can be collected ethically and economically.

## 15. Human-Action Queue

The following actions genuinely require a human:

1. Approve recruitment of 24 adult software engineers and the consent/data-
   minimization protocol.
2. Decide whether participant compensation is allowed and set a ceiling.
3. Select a recruitment channel and authorize outreach; the factory must not
   contact people or organizations autonomously.
4. Review the preregistered experiment materials and defect validity before
   participant exposure.
5. After the experiment, authorize any payment, employer pilot, publication,
   or product-discovery step.

No recruitment, outreach, purchase, publication, or external integration was
performed for this dossier.

The founder may self-observe the engineer feasibility pass locally. That action
does not authorize claims about external users. The parent-side observation may
also begin as a private adult record, but any child participation remains gated
by consent, assent, minimization, and the existing education experiment
protocol.

## 16. Decision

### RUN EXPERIMENT

This decision advances only a cheap, reversible, adult research experiment.
It does not advance a product, market, platform, or business claim.

Why:

- AI adoption is sufficiently established to justify testing the risk.
- Retrieval, spacing, explanation, and calibration provide a credible mechanism
  worth falsifying.
- The proposed AI-skeptic differentiator is not established and requires a
  direct comparison.
- Existing products and free alternatives make building before measurement
  unjustified.
- Payment, retention, direct pain, and defensibility remain unproven.

The next valid evidence is behavioral: independent performance, analogous-error
detection, delayed retention, adherence, and an actual repeat-use or payment
action. Enthusiasm, survey agreement, feature availability, and passing local
tests are insufficient.

## Sources

Retrieval date for all URLs: 2026-09-20 unless noted.

- **S1.** Stack Overflow, *2025 Developer Survey: AI*,
  https://survey.stackoverflow.co/2025/ai
- **S2.** HackerRank, *2025 Developer Skills Report*,
  https://www.hackerrank.com/reports/developer-skills-report-2025
- **S3.** Bastani et al., *Generative AI Can Harm Learning*, 2024,
  https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4895486
- **S4.** Lee et al., *The Impact of Generative AI on Critical Thinking*, CHI
  2025, https://doi.org/10.1145/3706598.3713778
- **S5.** Roediger & Karpicke, *Test-enhanced learning*, 2006,
  https://doi.org/10.1111/j.1467-9280.2006.01693.x
- **S6.** Cepeda et al., *Distributed practice in verbal recall tasks*, 2006,
  https://doi.org/10.1037/0033-2909.132.3.354
- **S7.** Anki official product documentation, https://apps.ankiweb.net/
- **S8.** HackerRank assessment and interview products,
  https://www.hackerrank.com/
- **S9.** LeetCode interview practice, https://leetcode.com/
- **S10.** CodeSignal technical assessment product, https://codesignal.com/
- **S11.** Educative developer learning platform, https://www.educative.io/
- **S12.** Codecademy technical learning platform, https://www.codecademy.com/
- **S13.** Exercism practice platform, https://exercism.org/
- **S14.** Parasuraman & Manzey, *Complacency and bias in human use of
  automation*, 2010, https://doi.org/10.1016/j.humov.2010.02.007
- **S15.** OpenAI, *Introducing study mode*, 2025,
  https://openai.com/index/chatgpt-study-mode/
- **S16.** Anthropic, *Claude for higher education*,
  https://claude.com/solutions/education
- **S17.** Khan Academy, *Khanmigo*, https://www.khanmigo.ai/
- **S18.** Brilliant, *Personal tutor for math and coding*,
  https://www.brilliant.org/
- **S19.** Quizlet, *Study tools and learning resources*, https://quizlet.com/
- **S20.** Peng et al., *The Impact of AI on Developer Productivity*, 2023,
  https://arxiv.org/abs/2302.06590
- **S21.** Becker et al., *Measuring the Impact of Early-2025 AI on Experienced
  Open-Source Developer Productivity*, 2025,
  https://arxiv.org/abs/2507.09089

## Local Provenance

- `docs/research/ai-era-learning-opportunity.md`
- `.factory/artifacts/evidence/education-opportunity-discovery.json`
- `.factory/experiments/education/protocol.md`
- `.factory/experiments/education/results-schema.json`
- `.factory/control-plane-bindings.json`
- GitHub issue #50: https://github.com/edoworks/sf0.8/issues/50

This dossier is an evidence and experiment artifact. It is not product
authorization, customer evidence, educational-effectiveness evidence, or a
claim of monetizable opportunity.
