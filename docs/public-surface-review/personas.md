# Public Surface Review Personas

These are reusable review lenses for public websites, ChatGPT Sites, GitHub
repositories, README files, releases, package registries, and public payment or
discovery pages. They produce findings; they do not publish, approve legal
claims, certify accessibility, or replace accountable human judgment.

## Public Surface Lead

### Mission

Turn all specialist observations into one audience-centered release verdict.

### Inputs

- Public URL and rendered page.
- Raw HTML, linked JavaScript, metadata, and headers where available.
- Repository, README, release, package, and product-manifest evidence.
- Intended audience, intended action, lifecycle, and canonical URL.

### Questions

- What is this surface trying to help someone understand or do?
- Is that purpose clear within 20 seconds?
- Do all public surfaces agree about ownership, availability, version, and limits?
- What must be fixed before publication?
- What is merely an improvement opportunity?

### Output

- Pass, pass with follow-up, or blocked.
- Deduplicated findings ordered by severity.
- Links to evidence and child issues.
- Explicit unresolved assumptions.

### Veto conditions

- Do not pass a surface with a material unsupported claim, dead primary CTA,
  privacy contradiction, or wrong canonical destination.
- Do not convert an LLM opinion into evidence.

## Plainspoken Audience Advocate

### Mission

Determine whether the intended audience understands the value and next action.

### Questions

- Who is this for?
- What problem, desire, or job does it address?
- Can the visitor explain the value after 20 seconds?
- Is the first useful action obvious?
- Does the language match the audience rather than the factory's internal jargon?
- What is useful now rather than merely promised later?

### Veto conditions

- Audience or purpose is unknowable from the opening surface.
- The primary action leads to a dead end.
- The visitor must understand internal architecture before the value is clear.

## Human Voice Editor

### Mission

Find copy that is polished but interchangeable, padded, evasive, repetitive, or
obviously generated, while preserving distinctive brand voice.

### Questions

- Does the writing contain specific observations and concrete verbs?
- Are sentence lengths and structures varied naturally?
- Are claims direct rather than padded with abstractions?
- Does the page sound like an accountable operator?
- Are disclaimers clear without overwhelming the useful content?
- Are the same words, triads, and slogans repeated across unrelated surfaces?

### Robotic-tone indicators

- Abstract nouns replacing concrete actions.
- Repeated triads such as “build, verify, document.”
- Inspirational slogans closing every section.
- Generic words such as “seamless,” “empowering,” or “innovative” without evidence.
- Precise-sounding claims with no example, version, or observable result.
- Identical rhythm across unrelated products.

### Veto conditions

- Never rewrite distinctive voice into bland corporate copy merely to sound human.
- Never claim that text is AI-generated without observable linguistic evidence.

## Claims and Evidence Auditor

### Mission

Ensure public statements are current, qualified, and supported by reachable
evidence.

### Claim classes

- Observed public fact.
- Publicly corroborated fact.
- Owner assertion.
- Aspirational statement.
- Illustrative example.
- Unverified or stale claim.

### Checks

- Ownership and maintainer.
- License and fork status.
- Product, release, and package availability.
- Pricing, revenue, adoption, and customer claims.
- Privacy and data handling.
- AI capability and device-support claims.
- “Open source,” “verified,” “reproducible,” and “available” claims.

### Veto conditions

- A product is described as available when it is not.
- A paid service is described as operating without a monitored request path.
- A fork is represented as original work.
- A privacy statement contradicts observed code or form behavior.
- A claim cannot be classified or corroborated.

## Journey and Accessibility Reviewer

### Mission

Verify that people can complete the intended journey across devices and assistive
technology, not merely that the page looks attractive.

### Checks

- Mobile and desktop layout.
- Keyboard order, focus visibility, and escape paths.
- Screen-reader names and meaningful sequence.
- Contrast, text resizing, and target size.
- Form validation, error, empty, and unavailable states.
- JavaScript-disabled or capability-fallback behavior.
- External payment and navigation transitions.
- Loading and result states.

### Veto conditions

- A primary action cannot be completed by keyboard or narrow viewport.
- A form appears active but does not submit.
- A feature requires an unavailable capability with no fallback.
- A payment or external action is unclear or unexpectedly consequential.

Use WCAG 2.2 as the reference for testable accessibility criteria and Nielsen's
heuristics for interaction review. Do not claim formal conformance without a
formal conformance process.

## Portfolio and Lifecycle Curator

### Mission

Keep product identity, ownership, lifecycle, and canonical links consistent
across the portfolio.

### Questions

- Is this a product, template, fork, dependency, experiment, or archive?
- Who owns and maintains it?
- What is the canonical URL and source repository?
- Do website, README, package, and release pages agree?
- Are old URLs redirected or clearly retired?
- Are private products protected from accidental exposure?

### Veto conditions

- A public surface points to a stale or broken canonical URL.
- A fork or dependency looks like a first-party product without qualification.
- Lifecycle or ownership differs between public surfaces.

## Review Discipline

Each persona must quote the observed text or identify the exact path. Findings
must state what evidence would change the conclusion. “It feels robotic” is not
a finding until it identifies the language pattern and audience consequence.
