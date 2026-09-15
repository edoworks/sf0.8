# Initial Public Surface Audit

Reviewed: 2026-09-15

## Inventory

### Websites and ChatGPT Sites

- `https://edoworks.com/`
- `https://edoworks.com/portfolio/`
- `https://edoworks.com/blog/`
- `https://edoworks.com/rung/`
- `https://foculoom.com/`
- `https://mews-and-woofs.foculoom-5388.chatgpt.site/`
- `https://rung-evidence.foculoom-5388.chatgpt.site/`

### Public Edoworks repositories

- `https://github.com/edoworks/edoworks.github.io`
- `https://github.com/edoworks/rung`
- `https://github.com/edoworks/asc-client`
- `https://github.com/edoworks/factory-constitution`
- `https://github.com/edoworks/trycycle`

## P0 findings

None newly discovered in the 2026-09-15 snapshot. Existing Mews/Rung
placeholder defects were remediated and tracked in closed issues #18 and #19.

## P1 findings

### F-001: Foculoom Rung link uses deprecated hostname

- Persona: Portfolio and Lifecycle Curator
- Surface: `https://foculoom.com/`
- Observed: the Rung link points to `https://rung.edoworks.com/`.
- Evidence: `https://edoworks.com/rung/` is the canonical working page; the
  subdomain has a recorded Cloudflare failure and deprecation task.
- Audience consequence: visitors can be sent to an unavailable duplicate.
- Recommended change: link to `https://edoworks.com/rung/` and retain the old
  hostname only as a 301 redirect.
- Follow-up: `sf0.8 #11`, `edoworks.github.io #68`.

### F-002: Foculoom description appears to say “manufacturing evidence”

- Persona: Claims and Evidence Auditor
- Surface: `https://foculoom.com/`
- Observed: “Edoworks researches, builds, verifies, and documents
  manufacturing evidence.”
- Evidence: the Edoworks site and repositories describe software engineering
  and repository evidence, not manufacturing evidence.
- Audience consequence: the factory's purpose is unclear and may appear to be a
  public copy error.
- Recommended change: owner-confirm the intended phrase; likely replace with
  “software engineering evidence.”
- Follow-up: `sf0.8 #25`.

### F-003: Public repository portfolio coverage is incomplete

- Persona: Portfolio and Lifecycle Curator
- Surfaces: Edoworks portfolio and public Edoworks organization.
- Observed: public repositories include `asc-client`,
  `factory-constitution`, and a `trycycle` fork, while the portfolio primarily
  presents Rung and Mews & Woofs.
- Audience consequence: visitors cannot tell which repositories are products,
  templates, forks, or dependencies.
- Recommended change: add lifecycle labels or explicitly exclude non-products
  with an explanation.
- Follow-up: `sf0.8 #24`.

### F-004: Edoworks homepage is coherent but abstract

- Persona: Plainspoken Audience Advocate and Human Voice Editor
- Surface: `https://edoworks.com/`
- Observed: “Intent → verified software,” “Evidence at every handoff,” and the
  five-stage “Research / Plan / Build / Verify / Review” pipeline.
- Evidence: no audience, concrete job-to-be-done, example outcome, or direct
  “use this today” path appears on the homepage.
- Audience consequence: a prospective user or collaborator may understand the
  factory philosophy without understanding what Edoworks offers them.
- Recommended change: add one concrete audience sentence and one example-led
  path to the portfolio, Rung, or active experiments. Preserve the manifesto as
  secondary positioning.
- Follow-up: `sf0.8 #25`.

### F-005: Public website README lags the live page inventory

- Persona: Portfolio and Lifecycle Curator
- Surface: `https://github.com/edoworks/edoworks.github.io`
- Observed: README structure describes landing, blog, portfolio, and Rung but
  omits the Mews & Woofs experiment directory and new posts.
- Audience consequence: a maintainer cloning the repository cannot reconstruct
  the current public surface model from the README.
- Recommended change: update the README structure and publication instructions.
- Follow-up: `sf0.8 #24`.

## P2 findings

### F-006: Rung is useful but dense

- Persona: Plainspoken Audience Advocate
- Surface: `https://github.com/edoworks/rung` and `https://edoworks.com/rung/`.
- Observed: strong quick-start and limitation content, but the README is long
  and repeats evidence terminology before showing task-oriented examples.
- Recommended change: add a short “Use Rung when…” section with two concrete
  scenarios; do not remove the reproducibility detail.

### F-007: Mews & Woofs is distinctive but still an experiment

- Persona: Claims and Evidence Auditor
- Surface: `https://mews-and-woofs.foculoom-5388.chatgpt.site/`.
- Observed: the visual voice is specific and the page clearly says “Concept
  preview · Beta not open,” while the sample is fictional and local-only.
- Recommended change: retain the status and use interaction evidence rather
  than treating visual polish as product validation.

## Positive evidence

- Mews & Woofs has a clear concept-preview status, no active form, no audio
  collection, and a fictional sample interaction.
- Rung has concrete source, release, PyPI, reproducibility, and limitation paths.
- Edoworks uses a stable canonical Rung page and explicitly distinguishes free
  software from unlaunched commercial offerings.
- The current public surfaces avoid fabricated testimonials, user counts, and
  unsupported adoption claims.

## Research basis

- [WCAG 2.2](https://www.w3.org/TR/WCAG22/)
- [Nielsen Norman Group usability heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/)
- [Google people-first content guidance](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)
- [Digital.gov plain-language guidance](https://digital.gov/guides/plain-language/)
