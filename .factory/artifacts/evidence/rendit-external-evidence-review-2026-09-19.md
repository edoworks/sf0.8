# Rendit External Evidence Review

Status: `EVIDENCE_COMPLETE_NOT_MARKET_VALIDATED`
Date: 2026-09-20
Audience: sf0.8 founder and Rendit maintainers
Jurisdiction: technical opportunity evidence only; no publication, legal,
licensing, financial, or product authorization
Decision: whether Rendit’s deterministic rendering/provenance workflow has
enough independent evidence to advance beyond an internal shovel hypothesis
Date cutoff: 2026-09-20 inclusive

## Source Plan And Stopping Rule

Primary sources: official reproducible-builds guidance, SLSA requirements,
GitHub artifact-attestation documentation, Docker BuildKit reproducibility
documentation, and local Rendit/project provenance records.

Counterclaims: established build/provenance systems may solve the relevant
problem without Rendit; technical standards may document best practice without
showing buyer demand; public documentation may not reveal workflow frequency,
switching, or payment.

Stop when public sources establish the problem category and alternatives, or
when remaining uncertainty requires interviews, observed workflows, repeat use,
or payment. No outreach or publication is authorized.

## Executive Answer

**Problem category: externally evidenced, medium-high confidence.** Independent
technical standards and platform documentation treat deterministic outputs,
consistent build processes, and provenance as real engineering concerns.

**Rendit-specific opportunity: plausible but unvalidated, low-medium
confidence.** Rendit has multiple internal consumers and passed a clean
deterministic rendering probe, but no independent customer behavior or payment
evidence connects those facts to a Rendit product opportunity.

**Recommendation: retain `SHOVEL` / `VALIDATE`.** Do not publish, split into
standalone packages, or invest in a product until a reachable external user
and economic signal are observed.

## Findings

### Claim 1: Reproducibility is an independently documented engineering problem

**Evidence:** Reproducible Builds states that builds vary due to uncontrolled
inputs such as filesystem ordering and current time, and recommends stable
inputs, stable outputs, and minimizing environment capture. [Primary technical
guidance, retrieved 2026-09-20: https://reproducible-builds.org/docs/deterministic-build-systems/]

**Counterevidence:** This source addresses software/build systems broadly, not
Rendit users, visual assets, or a paid workflow.

**Implication:** Rendit’s deterministic-output concern is not invented, but
the source only supports a problem-category signal.

### Claim 2: Provenance and consistent build processes are independently valued

**Evidence:** SLSA’s artifact-producing requirements state that producers must
follow a consistent build process and distribute provenance to consumers. The
specification describes provenance generation and build isolation as platform
responsibilities. [Primary standard, retrieved 2026-09-20:
https://slsa.dev/spec/v1.0/requirements]

**Counterevidence:** SLSA is a security/supply-chain standard, not evidence
that users need Rendit’s rendering workflow or would pay for it.

**Implication:** Provenance is a credible enabling requirement and possible
shovel dimension, but not Rendit-specific demand evidence.

### Claim 3: Existing platforms already monetize or operationalize adjacent controls

**Evidence:** GitHub documents artifact attestations for establishing build
provenance and verifying consumed software, including offline verification.
Docker documents reproducible builds using `SOURCE_DATE_EPOCH` in BuildKit
workflows. [Primary platform documentation, retrieved 2026-09-20:
https://docs.github.com/en/actions/security-for-github-actions/using-artifact-attestations/;
https://docs.docker.com/build/ci/github-actions/reproducible-builds/]

**Counterevidence:** These are platform capabilities and documentation, not
proof that they displace a deterministic visual-asset workflow or that a new
Rendit skill would win against them.

**Implication:** The competitive bar is high. Rendit must demonstrate a
distinct asset/rendering job, not merely repeat generic provenance language.

### Claim 4: Rendit has internal evidence of technical reuse

**Evidence:** A clean pinned Rendit probe produced identical PNG bytes and
hash sidecars across two runs. Gem Cascade, Endless Runner Template, and
Docketloom provenance records identify Rendit as an asset-generation tool.
[Primary local evidence: `.factory/artifacts/evidence/rendit-workflow-probe-completion-2026-09-19.json`]

**Counterevidence:** All observed consumers are within the Foculoom portfolio;
internal reuse is not external validation or willingness to pay.

**Implication:** Rendit has earned continued internal maintenance and bounded
reuse investigation, not public packaging.

## Conflicts And Unknowns

- Standards evidence supports reproducibility and provenance generally, while
  the Rendit-specific buyer, workflow frequency, and economic value remain
  unknown.
- GitHub and Docker provide adjacent capabilities; it is unknown whether they
  are sufficient substitutes for Rendit’s visual recipe/provenance contract.
- Internal consumer records establish use, not voluntary external adoption,
  repeat use, switching, or payment.
- Asset, font, binary, and dependency licensing remains incomplete for public
  sharing.

## Decision Implications

- Keep Rendit as one canonical internal runtime.
- Do not create standalone skills or packages from this review.
- The cheapest next validation is a founder-authorized, real external workflow
  observation or interview with a defined job and current substitute, followed
  by an observable economic signal if the problem is repeated.
- The conclusion would strengthen if independent users repeatedly use the
  workflow, request it again, and spend time or money solving the same job.
- The conclusion would weaken if established alternatives solve the job with
  no measurable dissatisfaction, or if internal consumers do not need the
  proposed boundary.

## Evidence Classification

- `FACT`: public standards document deterministic/provenance requirements;
  Rendit probe and internal provenance records are present.
- `EVIDENCE`: independent public technical sources corroborate the problem
  category.
- `INFERENCE`: Rendit may be a useful shovel for a narrower asset workflow.
- `ASSUMPTION`: an external user may value Rendit’s integrated recipe,
  rendering, and provenance contract.
- `UNKNOWN`: customer identity, repeat use, payment, pricing, and external
  distribution.

## Sources

### Primary

- Reproducible Builds, “Deterministic build systems,” retrieved 2026-09-20:
  https://reproducible-builds.org/docs/deterministic-build-systems/
- SLSA v1.0, “Producing artifacts,” retrieved 2026-09-20:
  https://slsa.dev/spec/v1.0/requirements
- GitHub Docs, “Using artifact attestations,” retrieved 2026-09-20:
  https://docs.github.com/en/actions/security-for-github-actions/using-artifact-attestations/
- Docker Docs, “Reproducible builds with GitHub Actions,” retrieved 2026-09-20:
  https://docs.docker.com/build/ci/github-actions/reproducible-builds/
- sf0.8 and local Foculoom provenance records, retrieved 2026-09-20.

### Secondary

- None required for the bounded conclusion.

### Lead-only

- Search snippets, rankings, vendor marketing claims, and generated summaries
  were not used as evidence.
