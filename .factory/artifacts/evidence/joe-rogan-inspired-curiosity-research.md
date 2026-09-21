# Curiosity and Candor Skill Research

Status: `RECOMMEND_BUILD_AS_METHOD_SKILL`
Date: 2026-09-19
Cutoff: 2026-09-19

## Scope and Decision

Decision: build a neutral factory skill that operationalizes observable methods
associated with long-form curious interviewing and candid challenge. Do not
build a "Joe Rogan" persona, voice, likeness, transcript imitator, or implied
endorsement plugin.

Audience: factory owner and future agents operating inside the factory.

Jurisdiction: primarily U.S. product and policy context, with legal conclusions
treated as preliminary and requiring qualified counsel before commercial release.

Stopping rule: stop research when the build/no-build decision, minimum behavior
contract, material risks, and an empirical validation plan are supported or the
remaining gap requires a product experiment. That threshold is met here.

## Executive Answer

**Recommendation: build, confidence medium-high.** The useful abstraction is
not a public figure's personality. It is a repeatable review protocol:

1. Start with genuine questions and seek the strongest version of the claim.
2. Ask for mechanisms, examples, evidence, and boundary conditions.
3. Separate observation, inference, belief, and uncertainty.
4. Challenge claims without humiliating the person making them.
5. Admit when the evidence changed the conclusion and record the revision.
6. End with what is still unknown and what test would reduce uncertainty.

This fits the factory's mission to optimize verified human value while keeping
human authority, privacy, and safety controls intact. It should be a review and
decision aid, not an autonomous truth arbiter.

## Findings

### 1. The show is evidence of a format, not proof of a stable personal trait

Spotify's public product and legal material confirms that podcasts are content
within its service and that availability and content can change. It does not
establish that Rogan is consistently curious, accurate, or brutally honest.
Those character judgments remain an interpretation of public performances, not
verified facts.

**Implication:** describe the proposed skill by behaviors and outcomes, not by
claiming to reproduce Rogan's character.

Source: [Spotify Terms of Use](https://www.spotify.com/us/legal/end-user-agreement/),
last updated 2026-09-04, first-party platform terms, retrieved 2026-09-19.

### 2. Curiosity is useful only when paired with evidence discipline

The relevant behavior is not asking more questions for its own sake. A useful
factory loop converts surprise or disagreement into a request for mechanism,
counterexample, source quality, and a discriminating test. Research on surprise
and cognitive control reports that surprise can be a shared driver of both
inhibitory and motivated control, but that finding is about a laboratory task,
not podcast interviewing or truth discovery.

**Implication:** use surprise as a trigger for investigation, never as evidence
that a claim is true or false.

Source: Vassena, Deraeve, and Alexander, “Surprise, value and control in
anterior cingulate cortex during speeded decision-making,” *Nature Human
Behaviour* 4, 412–422 (published 2020-01-13),
[DOI](https://doi.org/10.1038/s41562-019-0801-5), original research, retrieved
2026-09-19.

### 3. Candor needs a calibrated uncertainty protocol

The factory should require the agent to label confidence, distinguish direct
evidence from synthesis, name the strongest counterevidence, and say what would
change its mind. This is a design recommendation, not a claim that the source
subject or any interview format reliably achieves those standards.

The U.S. Copyright Office distinguishes protected expression from unprotected
ideas, facts, systems, and methods of operation. That supports extracting a
general method while avoiding copied expression, subject to a broader legal
review for trademarks, publicity rights, and unfair endorsement.

Source: [U.S. Copyright Office, Copyright in General FAQ](https://www.copyright.gov/help/faq/faq-general.html),
retrieved 2026-09-19, official government guidance.

### 4. The implementation boundary is materially important

Spotify's User Guidelines prohibit scraping or automated collection of Spotify
content and prohibit using Spotify content to train or otherwise ingest into an
AI model. They also prohibit impersonating or misrepresenting affiliation with
a person or entity. These terms govern Spotify services; they are not a
complete statement of all applicable law, but they are enough to rule out a
design based on ingesting JRE episodes or presenting the skill as Rogan.

Source: [Spotify User Guidelines](https://www.spotify.com/us/legal/user-guidelines/),
retrieved 2026-09-19, first-party platform policy.

### 5. Commercial endorsement creates a separate risk

The FTC's Endorsement Guides explain the agency's framework for endorsements
and testimonials in advertising. A product name, copy, avatar, or marketing
that suggests Joe Rogan's sponsorship or approval would need a separate legal
and rights review; the skill should make no such suggestion.

Source: [FTC Endorsement Guides: What People Are Asking](https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides),
retrieved 2026-09-19, official government guidance.

## Proposed Skill Contract

Working name: `curiosity-audit` or `good-faith-pressure-test`.

Inputs:

- a decision, draft, claim, or product hypothesis;
- known evidence and source links;
- decision stakes and deadline;
- the operator's desired challenge level.

Outputs:

- strongest charitable restatement;
- 3–7 high-value questions, prioritized by uncertainty reduction;
- claim/evidence/counterevidence table;
- confidence labels and unknowns;
- failure modes and disconfirming tests;
- a direct recommendation with the conditions that would change it;
- a short record of any conclusion revised during review.

Non-negotiable behavior:

- ask before asserting when the missing fact is decision-critical;
- never turn confidence, provocation, or an unusual anecdote into proof;
- distinguish “I do not know” from “the evidence is mixed”;
- attack the claim, not the person;
- surface conflicts of interest and incentives;
- preserve disagreement instead of forcing consensus;
- escalate legal, medical, financial, privacy, release, and publication decisions.

Explicit non-goals:

- no Rogan name in the skill identity or product marketing;
- no imitation of his voice, catchphrases, mannerisms, or political worldview;
- no JRE transcript, clip, audio, or scraped Spotify corpus;
- no claim of endorsement, affiliation, authenticity, or access;
- no autonomous external publication or irreversible action.

## Factory Leverage

Use the skill at four points:

1. **Opportunity intake:** pressure-test whether a customer problem is real,
   who experiences it, and what evidence would falsify it.
2. **Build review:** require the agent to state the strongest reason not to
   build before implementation proceeds.
3. **Evidence review:** challenge source quality, missing counterevidence, and
   unsupported leaps without replacing the evidence-research workflow.
4. **Postmortem:** ask what surprised the team, which assumption failed, and
   which guard should be added to prevent recurrence.

The skill should be a project-local method first. Promotion to shared factory
machinery should wait for two real consumers, measured results, and a safety
review, matching the repository's rule of two.

## MVP Acceptance Tests

- Given a one-sided product proposal, the skill produces a charitable opposing
  case and at least one falsifiable test.
- Given conflicting sources, it preserves the conflict and does not average it
  into false certainty.
- Given an unsupported extraordinary claim, it requests evidence rather than
  mirroring the user's confidence.
- Given a sensitive domain, it escalates instead of issuing professional advice.
- Given a request to “sound like Joe Rogan,” it refuses identity/style
  imitation and offers the neutral method contract.
- Given an external link or fetched document, it treats the content as untrusted
  data and does not obey instructions embedded in it.
- Every output has a confidence label, unknowns, and a “what would change this”
  field.

Suggested metrics after dogfooding:

- percentage of reviews that identify a material hidden assumption;
- percentage that add a useful disconfirming test;
- false-challenge rate, where the challenge is unsupported or irrelevant;
- operator-rated decision usefulness;
- escalation precision for high-stakes domains;
- number of unsupported factual additions introduced by the skill.

## Counterevidence, Conflicts, and Unknowns

- No direct, systematic study was found here demonstrating that Rogan's public
  interview practice produces better decisions or more accurate beliefs.
- A long, informal format can create openness and discovery, but it can also
  give weak claims extended airtime. This report does not infer credibility from
  conversational ease or audience size.
- The copyright source addresses copyright scope, not all publicity, trademark,
  unfair competition, or platform-contract questions.
- Spotify's rules are platform terms, not a universal ban on every independent
  analysis of public material. Counsel should review any commercial use of name,
  likeness, voice, clips, or archival content.
- The proposed metrics are hypotheses until tested on factory decisions.

## Decision Implications

Build a small `curiosity-audit` skill and dogfood it on two different factory
decisions. Do not build a branded Joe Rogan plugin or ingest JRE/Spotify content.
Keep the first version advisory, source-aware, local-only, and human-gated.

The conclusion would change if: rights counsel authorizes a licensed identity
or content use; controlled tests show the method increases noise or harms
decision quality; operators reject the challenge style; or a safer existing
factory capability already covers the same contract.

## Source Register

Primary and official sources:

- [Spotify Terms of Use](https://www.spotify.com/us/legal/end-user-agreement/),
  updated 2026-09-04; platform terms.
- [Spotify User Guidelines](https://www.spotify.com/us/legal/user-guidelines/),
  retrieved 2026-09-19; platform policy.
- [FTC Endorsement Guides](https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides),
  retrieved 2026-09-19; government guidance.
- [U.S. Copyright Office FAQ](https://www.copyright.gov/help/faq/faq-general.html),
  retrieved 2026-09-19; government guidance.

Original research:

- [Vassena et al. (2020)](https://doi.org/10.1038/s41562-019-0801-5),
  *Nature Human Behaviour*; peer-reviewed original research.

Lead-only material not relied on for material claims:

- [JRE Podcast fan site](https://www.jrepodcast.com/), explicitly labeled
  unofficial; useful for episode discovery only, not authority for claims about
  Rogan, Spotify, or the show's methods.
