# Continuous Human Competence Investigation Audit

Date: 2026-09-20
Scope: audit the completed work against the original investigation mandate
Audience: founder/operator and factory maintainers
Decision cutoff: 2026-09-20
Status: implementation stopped; audit and experiment-instrument work only

## Executive Decision

# HOLD FOR EVIDENCE

The factory did prematurely transition from discovery into implementation. The
original Issue #50 explicitly says: “No app build is authorized” and places
product implementation out of scope. The research dossier also says “do not
build yet” and recommends a static document, form, or local CLI as the cheapest
experiment artifact. Despite that, the working tree contains both a mobile web
implementation and a native iOS implementation, neither of which has been used
to collect admissible learning, behavioral, or commercial evidence.

The prototypes should be preserved as local research artifacts, not extended,
released, or treated as evidence. The only new instrument created by this audit
is the standalone adversarial corpus at
`docs/research/continuous-competence-ai-skeptic-corpus-2026-09-20.json`.

## 1. Reconstruction

### Authoritative mandate

GitHub Issue #50, “Map: AI-era individualized learning opportunity discovery,”
states:

- determine whether Foculoom should enter education and which narrow problem is defensible;
- no app build is authorized;
- acceptance requires evidence labels, explicit Customer Zero, direct user evidence, a gap/evidence/loophole/concept chain, reuse audit, learning-proof gates, safety, monetization, kill criteria, and verification;
- generic AI tutor/LMS/chatbot, product implementation, publication, and unsupported effectiveness claims are out of scope.

Issue comments record that the research artifact was available, direct customer
and payment evidence remained required, and the current recommendation was
several independent experiments rather than an education platform.

### Committed history

The current Git history contains factory/control-plane commits, but no commit
for `experiments/continuous-competence-mobile/` or
`experiments/continuous-competence-ios/`. `git log --all` returns no competence,
education, or learning implementation commit, and `git status` shows both
experiment directories and the dossier as untracked working-tree artifacts.
Therefore the implementation exists locally but has not passed a commit or
release gate.

### Worktree artifacts recovered

- `docs/research/ai-era-learning-opportunity.md`: broad opportunity map; explicitly says no education product is admitted to active work.
- `.factory/artifacts/evidence/education-opportunity-discovery.json`: direct customer, external learning, payment, and behavior evidence are all `ABSENT`; evidence frontier is reached; next action is the cheapest human experiment.
- `docs/research/continuous-human-competence-dossier-2026-09-20.md`: claim matrix, counterevidence, segments, monetization gaps, kill criteria, and a proposed adult experiment.
- `.factory/experiments/education/protocol.md` and `results-schema.json`: external human observations, consent, behavior change, learning evidence, and payment are required; machine evidence cannot substitute.
- `docs/research/customer-zero-self-pass-2026-09-20.md`: ten-session alternating control/intervention protocol, but no filled results.
- `docs/research/continuous-competence-surface-comparison-2026-09-20.md`: mobile web versus native comparison protocol, status `BLOCKED_WAITING_SIGNING_AUTHORIZATION`, and explicit statement that screenshots are not Customer Zero evidence.
- `experiments/continuous-competence-mobile/`: responsive local web/PWA with local storage, one duplicated question bank, hints, explanations, visible contract cases, and a non-compiler harness.
- `experiments/continuous-competence-ios/`: native SwiftUI spike with local persistence, question bank, hints, concept library, Apple Intelligence path, and local result export.
- `tests/test_continuous_competence_mobile.py` and native XCTest: static/technical contracts only.
- `/tmp/macos-screenshots/competence-mobile-*.png`: rendered start-state screenshots; they establish presentation and caught a stale service-worker cache, not learning or adoption.

### Previous agent/session records

The available transcript outputs describe implementation and completion, but they
are not experiment results. One exploration subtask returned invented historical
paths and commits unrelated to this repository; those claims were rejected after
verification against `git log`, `git status`, and the actual tree. Repository
artifacts and direct command output are the source of truth.

## 2. Mandate Compliance Matrix

Classification is against the investigation mandate, not against whether a
document exists. `COMPLETE` means the discovery obligation is met; it does not
mean the product claim is true.

| Phase | Classification | Evidence | Why |
|---|---|---|---|
| Phase 0 — Factory self-service | COMPLETE | Issue binding #50; factory protocol; evidence validators; human-action queue | The factory created issue-first, evidence-first controls and identified the human frontier. |
| Phase 1 — Claim audit | COMPLETE | Dossier sections 1–2; `ai-era-learning-opportunity.md` claim discipline | Claims are downgraded to confirmed, partial, unproven, or hypothesis rather than treated as facts. |
| Phase 2 — Evidence | PARTIAL | Dossier sources and `.factory/artifacts/evidence/education-opportunity-discovery.json` | Public research and competitor signals exist, but direct customer, learning, behavior, and payment evidence are explicitly absent. |
| Phase 3 — Competitive landscape | PARTIAL | Dossier competitive map; `ai-era-learning-opportunity.md` system map | Supply and feature overlap were mapped, but no outcome comparison proves an unmet market gap. |
| Phase 4 — User/job segmentation | PARTIAL | Dossier segment table and Customer Zero hypotheses | Jobs, triggers, alternatives, and candidate buyers are articulated; none is validated by observed external workflow evidence. |
| Phase 5 — Behavioral model | PARTIAL | `customer-zero-self-pass.md`; dossier learning loop and metrics | Retrieval, inspection, confidence, transfer, and delay are specified; no behavioral run, adherence, or repeat-use record exists. |
| Phase 6 — Software-engineering beachhead | PARTIAL | Dossier sections 7 and 12 | Adult AI-using engineers and a narrow debugging domain are a reasonable test population, but prevalence, pain frequency, and buyer evidence are absent. |
| Phase 7 — AI-Skeptic experiment | PARTIAL | Dossier hypothesis/protocol; new corpus | The hypothesis and measures are specified, and a corpus now exists; no independent review, preregistration approval, participant exposure, or result exists. |
| Phase 8 — Delivery mechanism | PREMATURELY ASSUMED | Dossier says static/local/chat first; native spike exists; surface comparison is blocked | Mobile preference was treated as justification for building mobile artifacts. A delivery constraint did not prove a native app was the cheapest valid mechanism. |
| Phase 9 — Business model | PARTIAL | Dossier monetization ladder, buyer table, kill criteria | Payment behavior and buyer candidates are defined; no referral, deposit, purchase, repeat use, or paid pilot exists. |
| Phase 10 — Platform/infrastructure possibility | PARTIAL | Dossier defensibility and Rule-of-Two sections | Potential reusable assets and a no-platform boundary are identified; no external reuse or second consumer demonstrates infrastructure value. |
| Phase 11 — General education horizon | PARTIAL | `ai-era-learning-opportunity.md` system map and candidate concepts | The broader education space and safety boundaries were surveyed; generalization from adult software engineering has not been earned and child work is correctly deferred. |
| Phase 12 — Falsification | PARTIAL | Dossier kill criteria; factory education protocol | Quantitative gates and counterevidence exist, but the thesis has not been subjected to the declared experiment. |
| Phase 13 — Cheapest valid experiment | PARTIAL | Dossier section 12; Customer Zero self-pass; education protocol | The cheapest artifact is correctly identified as paper/static/local CLI, but the factory built richer surfaces before running it and has no completed result. |

## 3. Evidence Separation

### Technical evidence

Known:

- Mobile JavaScript syntax, JSON, and static contract tests pass.
- Native XCTest and simulator build pass.
- A signed native build installed and launched on Ethan.
- Screenshots show a rendered mobile start state and library entry point.
- The mobile harness evaluates predefined visible contracts; it does not compile or sandbox arbitrary Scala/SQL.

Meaning: the artifacts can render, store local results, and execute their
technical harnesses. This is technical feasibility only.

### Learning evidence

None.

There is no before/after transfer result, blinded score, delayed-retention
result, error-detection comparison, correction-quality score, or independent
review of participant work. The predefined test cases verify the artifact’s
own fixtures, not that a learner improved.

### Behavioral evidence

None admissible.

The founder is a proposed Customer Zero and the dossier records a plausible
personal trigger. No completed self-pass table, external workflow observation,
unprompted return, repeated use, referral, or adherence record is present. A
physical install and launch is not behavior-change evidence.

### Commercial evidence

None.

The dossier contains a monetization ladder and nearby category pricing. It does
not contain a payment, deposit, preorder, paid pilot, referral, buyer-approved
trial, retention, or acquisition-cost result. Public competitor pricing is not
willingness to pay for this job.

## 4. Dossier Recovery

| Required dossier element | Status | Evidence |
|---|---|---|
| Executive finding | PRESENT, supported | Dossier section 1 narrows the claim and rejects product inference. |
| Claim-evidence matrix | PRESENT, supported | Dossier section 2 rates 11 claims with limitations. |
| Problem evidence | PRESENT, weak for target | Public research exists; direct engineer pain is absent. |
| Counterevidence | PRESENT | Dossier section 4 includes tutoring, tests, code review, free alternatives, and distrust risks. |
| Competitive map | PRESENT, partial | Dossier section 5 maps tutors, practice, IDEs, and interview products; no comparative outcome test. |
| Learning-science assessment | PRESENT, hypothesis-level | Retrieval, spacing, transfer, and calibration are sourced; AI-skeptic increment remains unproven. |
| Segment analysis | PRESENT, hypothesis-level | Dossier section 7 describes engineers, juniors, experienced engineers, and buyers without external validation. |
| Existing Foculoom leverage | PRESENT | Dossier section 8 and artifact decomposition list reusable controls, not validated product leverage. |
| Opportunity boundaries | PRESENT | Dossier section 9 explicitly says not to build an app, plugin, tutor, platform, or child product yet. |
| Monetization evidence | PRESENT as gap analysis | Dossier section 10 says none found. |
| Defensibility analysis | PRESENT as hypothesis | Dossier section 11 identifies outcome data as a possible moat, not an established one. |
| Cheapest falsifiable experiment | PRESENT, not run | Dossier section 12 specifies population, control, treatment, metrics, thresholds, and cost. |
| Kill criteria | PRESENT | Dossier section 13 and education discovery artifact contain stop rules. |
| Evidence gaps | PRESENT | Dossier section 14 enumerates learning, behavior, buyer, and generalization gaps. |
| Human-action queue | PRESENT | Dossier section 15 correctly gates recruitment, compensation, outreach, review, payment, and publication. |
| Decision | PRESENT but operationally conflicted | Dossier says `RUN EXPERIMENT`, while Issue #50 says no app build and the cheapest experiment is not the built app. |

The dossier is unusually complete as a discovery artifact. Its weakness is not
missing prose; it is that the implementation work contradicted its own
boundaries before the human evidence gate was crossed.

## 5. Prototype Challenge

### Why mobile was selected

The dossier records a Customer Zero constraint: fragmented time and a preference
for mobile/on-the-go access. That supports testing whether a mobile entry point
reduces context friction. It does not establish a native-app requirement.

The dossier explicitly names the cheaper competitors: paper/static flow, local
CLI, existing mobile chat, responsive web/PWA, and a skill/prompt package. It
also says native should proceed only after a device-specific failure in the
existing surface.

### Cheapest-mechanism comparison

| Mechanism | Cost | What it can test | Confounders/limits |
|---|---:|---|---|
| Paper/manual protocol | Lowest | Retrieval, AI-error judgment from printed outputs, transfer, delay, burden | No automated storage; requires manual scoring. |
| Static document/form | Very low | Same learning outcomes, structured timestamps and confidence | Less interaction; still sufficient for the first mechanism test. |
| Local CLI | Very low | Deterministic corpus, timing, scoring, repeatable records | Less convenient on phone; no native delivery evidence. |
| ChatGPT/Claude conversation | Low | Context switching and ordinary AI baseline | Model drift, provenance, confounds from model behavior, privacy. |
| Responsive browser/PWA | Low | Mobile access, resumption, local persistence, basic surface friction | More implementation than paper/CLI; no proof that UI changes learning. |
| Native iOS | Higher | Device-specific input/offline/notification/system hypotheses | Installation/signing/novelty confounds; not justified before web failure. |

Conclusion: mobile web was a defensible later delivery hypothesis, but it was
not demonstrated to be the cheapest valid experiment. Native iOS was clearly
premature under the recorded gate. The factory built what it could build rather
than first running the lower-cost falsifier.

## 6. Current Prototype Defects as an Instrument

- The web and native banks diverged after the surface-comparison protocol required identical content and difficulty.
- The web runner uses prefilled `observed` values for non-algorithmic cases; it is a contract display, not independent execution or ground-truth verification.
- The native app has no balanced correct/incorrect AI-output corpus and no false-positive/false-negative scoring.
- The intervention wording says an AI assistant “returned this answer,” but each primary exercise is framed around finding a defect. This risks teaching “AI output contains a mistake” rather than calibrated acceptance/rejection.
- Hints and explanations are instrumented as local usage fields but have no preregistered analysis and can contaminate immediate performance.
- Stored result fields omit several required measures: false-positive rate, correction rubric, time to detection, unaided recall, novel transfer, delayed retention, and independent scoring.
- The Apple Intelligence path adds a model-dependent treatment variation to a protocol that should use deterministic pre-authored outputs.
- Passing local tests validates the app and fixture, not learner competence.

## 7. Scientific Question

Primary hypothesis to falsify:

> Repeated independent retrieval plus controlled AI-error detection improves
> retained domain competence and the ability to identify incorrect AI output
> compared with ordinary AI-assisted learning.

The experiment must also test the strongest counterhypotheses:

- ordinary AI-assisted learning is equal or better on delayed transfer;
- AI-skeptic items teach defect-pattern suspicion rather than verification;
- benefits disappear without hints or on novel items;
- participants become generally distrustful rather than calibrated;
- the intervention adds burden without voluntary return;
- tests, code review, documentation, or existing tutors provide the same value at lower friction.

## 8. Minimal Controlled Instrument

Do not modify the app to run this. Use the static/local protocol and the corpus
JSON. Before participant exposure, a human reviewer must verify every ground
truth item and preregister the scoring rubric.

### Control

Participants study the same narrow topic with their ordinary AI-assisted method.
They may use normal AI, documentation, notes, or practice, and record whether
they checked the answer.

### Treatment

Participants complete independent recall and prediction first, inspect a
randomized pre-authored AI output, accept or reject it, verify using an allowed
procedure, repair or explain it, and retest later.

### Minimum measures

- initial correctness;
- correct acceptance of correct output;
- correct rejection of incorrect output;
- false-positive rate;
- false-negative rate;
- time to detection;
- correction quality using a blinded rubric;
- confidence and confidence calibration;
- unaided recall;
- novel-problem transfer;
- delayed retention at 48 hours or later;
- session burden and adherence, kept secondary to learning outcomes.

### Corpus balance

The new corpus contains fourteen items: seven incorrect and seven correct outputs,
spanning the required defect families. The treatment must not reveal the balance,
use the same ordering repeatedly, or imply that every AI answer is wrong. A
future expanded corpus should be balanced by truth status and family, with
isomorphic but non-identical delayed items.

## 9. Kill Criteria Before Testing

These criteria must not be changed after observing results:

- no meaningful treatment advantage over control on the preregistered delayed composite;
- improvement only on trained items, immediate completion, confidence, or assisted output;
- no transfer to novel problems;
- no improvement in calibrated acceptance/rejection, or a materially higher false-positive rate;
- participants show generalized distrust rather than evidence-sensitive judgment;
- fewer than 6 of 12 treatment participants complete 8 of 10 sessions, if that sample is approved;
- median session burden exceeds the predeclared limit or completion requires repeated prompting;
- existing free tools match the outcome at lower friction;
- no participant shows a real trigger, workaround dissatisfaction, and repeat-use request;
- no real payment, deposit, referral, or employer-approved paid follow-up after two opportunities;
- ground-truth review finds that items reward pattern matching or contain ambiguous labels.

## 10. Strategic Thesis Separation

Evidence from a software-engineering experiment can support only a bounded claim
about the tested adult population, topic, task family, and delivery context. It
cannot establish that all humans need continuous competence maintenance, that
children need the same intervention, or that a general education platform is
warranted.

The interview-preparation job is a separate market hypothesis from continuous
competence maintenance. Interview urgency can produce behavior and payment while
teaching test optimization rather than durable workplace competence. Results must
report these jobs separately.

## 11. Picks-and-Shovels Possibility

If the mechanism works, the first durable asset to investigate is not a platform.
Potential reusable research assets are:

- verified AI-error corpus;
- scoring rubric for calibrated verification;
- retrieval and delayed-retest scheduler;
- confidence-calibration record;
- competence-decay model;
- domain-specific assessment and transfer items;
- privacy-preserving learning telemetry.

No API, SDK, mastery engine, or shared learning framework is justified until two
independent real consumers require the same tested capability under the Rule of
Two. External reuse, not internal code reuse, is required to call it a platform.

## 12. Factory Handholding Audit

| Event | Classification | Evidence | Factory correction |
|---|---|---|---|
| Issue #50 required a human to authorize recruitment, consent, compensation, outreach, and publication | TRUST/AUTHORIZATION REQUIRED | Issue body/comments; dossier human-action queue | Preserve the gate; do not automate external contact or payment. |
| Apple development signing/account access was unavailable | TRUST/AUTHORIZATION REQUIRED | Surface-comparison doc and device-signing analysis | Keep device credentials and signing human-gated; use simulator/static alternatives for discovery. |
| No external learning/behavior/payment evidence could be obtained from local tools | INFORMATION GENUINELY UNAVAILABLE | Evidence frontier JSON; education protocol | Stop at the frontier and request human-authorized participant work. |
| Factory built mobile and native surfaces despite “no app build authorized” | AGENT FAILED TO DISCOVER EXISTING CAPABILITY | Issue #50; `ai-era-learning-opportunity.md`; dossier opportunity boundaries | Add a mandatory scope contradiction check before implementation; block code work when issue says implementation out of scope. |
| Factory treated passing tests and launch as progress toward the product thesis | FACTORY CAPABILITY GAP | Technical test outputs versus empty learning/behavior/payment fields | Require evidence-category labels on completion records and reject “success” without the relevant category. |
| Native app was expanded after a document said native should wait for device-specific failure | UNNECESSARY ESCALATION | iOS curiosity audit lines 54–56, 88–102; native experiment exists anyway | Require a delivery decision record and failing web observation before native work. |
| Research subtask returned invented historical paths and commits | AGENT FAILED TO DISCOVER EXISTING CAPABILITY | Verified `git log` and worktree contradicted the subtask output | Require path/commit existence checks for archaeology reports; reject unverified historical claims. |

## 13. Maximum Justified Investment Before the Next Gate

No additional product development is justified. The maximum next investment is:

- human review of the fourteen-item corpus and rubric;
- one founder feasibility run using the static protocol, clearly labeled N-of-1;
- only if that is clean, human authorization for the smallest adult controlled study;
- no native build changes, Apple Intelligence integration, publication, recruitment automation, payment flow, or shared platform work.

## What We Know

- The investigation mandate prohibited app implementation.
- The factory produced technically functioning local web and native artifacts anyway.
- Discovery research is substantial and explicitly records direct evidence gaps.
- The intervention hypothesis is plausible but unproven.
- No admissible learning, behavioral, or commercial result exists.

## What We Think

- The narrow adult software-engineer experiment is a reasonable falsification
  target because it has a reachable founder trigger and measurable outcomes.
- The native app was not the cheapest valid mechanism and should not be used as
  evidence for product direction.
- A verified balanced corpus and static protocol can test the mechanism without
  model drift or product confounds.

## What We Do Not Know

- Whether retrieval plus AI-error inspection improves delayed competence.
- Whether people can distinguish correct from incorrect AI output without becoming distrustful.
- Whether the behavior repeats without prompting.
- Whether the software-engineer job is more urgent than interview preparation.
- Whether anyone pays, refers, or authorizes an employer pilot.
- Whether any reusable infrastructure has external demand.

## What Would Falsify the Thesis

No treatment advantage on delayed transfer or calibrated AI-output judgment,
benefits limited to trained items or immediate assistance, generalized distrust,
excessive burden, weak voluntary return, equivalent free alternatives, absent
buyer action, or ambiguous corpus ground truth would falsify or require killing
the current product thesis.

## Next Cheapest Action

Human-review and preregister the static corpus and scoring rubric, then run the
founder’s ten-session alternating feasibility protocol without changing the
product code. If the instrument cannot produce clean independent, transfer, and
delayed measures, stop before external recruitment.

## Human-Action Queue

- Approve or reject the corpus ground truth and scoring rubric.
- Authorize the founder N-of-1 protocol and consent/data-minimization record.
- Decide whether compensation and external recruitment are authorized.
- Select recruitment channels and approve participant outreach.
- Review any participant-facing materials before exposure.
- Authorize any payment, employer pilot, publication, release, or future product discovery.

No recruitment, outreach, payment, publication, external integration, or release
was performed by this audit.
