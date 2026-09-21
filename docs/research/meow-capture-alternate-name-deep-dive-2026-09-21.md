# Meow-Capture Alternate Name Deep Dive

## Scope And Cutoff

- Audience: sf0.8 owner and iOS/iPadOS product and release decision-makers.
- Jurisdiction: Apple App Store public identity and metadata, with public-web
  name-collision screening; this is not trademark or legal clearance.
- Decision: identify one provisional alternate public name for the internal
  `meow-capture` experiment, or document why no candidate is yet defensible.
- Cutoff: evidence retrieved through 2026-09-21; event, publication, and
  retrieval dates remain distinct where relevant.
- Source plan: repository-primary product contract and release gates first;
  Apple primary guidance and Apple public catalog checks next; direct official
  trademark/search records where available; independent public product pages as
  secondary evidence; search snippets and unverified listings are lead-only.
- Stopping rule: stop after the product constraints are explicit and at least
  one candidate has direct collision checks across Apple/public web sources, or
  after the strongest candidates all fail a material check. Do not claim legal
  clearance from this screen.

## Current State Before Search

### Known facts

- `meow-capture` is an internal working identifier, not an authorized public
  name. [Repository primary, retrieved 2026-09-21]
- The product is a narrow, local iOS/iPadOS experiment that automatically
  retains, replays, and deletes a likely cat-meow clip during an owner-started,
  bounded session. [Repository primary, retrieved 2026-09-21]
- Public identity is deferred and publication is not currently authorized.
  [Repository primary, retrieved 2026-09-21]

### Open questions

- Which candidate is sufficiently distinctive and understandable for a future
  App Store listing?
- Does an existing Apple listing or established public product create a direct
  collision or likely confusion?
- Has the owner authorized any candidate for public use?

### Hypotheses

- A short, concrete name combining cat-audio cues with a capture/replay cue is
  more understandable than the technical identifier.
- Distinctiveness and collision risk matter more immediately than final brand
  polish because identity is a release gate.

### Recommendation status

Not yet determined. Any result will be a provisional naming recommendation,
not authorization, trademark advice, or a submission decision.

## Executive Answer

- **Medium-high confidence:** Use **WhiskerEcho** as the provisional alternate
  public name to unblock product-identity work. The name is short, readable,
  aligned with local cat-audio replay, and the exact Apple Search API query
  returned zero software results. [Apple primary public catalog, retrieved
  2026-09-21]
- **High confidence:** Do not use `MeowMemo`; Apple returned a current app named
  “MeowMemo - Cat Food & Journal,” creating an obvious category and name
  collision. [Apple primary public catalog, retrieved 2026-09-21]
- **High confidence:** Do not use `PurrEcho` as the first choice; the exact
  Apple query returned three software results, so the collision screen is not
  clean. [Apple primary public catalog, retrieved 2026-09-21]
- **High confidence:** `WhiskerEcho` is only a provisional candidate, not an
  authorized identity or legal clearance. Apple requires a unique app name,
  accurate metadata, and no use of another developer's name without approval;
  a zero-result catalog query cannot establish worldwide availability.
  [Apple primary policy and catalog, retrieved 2026-09-21]

## Findings

### Claim 1: The blocker is real and decision-relevant

**Evidence:** The product contract explicitly says `meow-capture` is an
internal working identifier and defers public identity. The local App Review
workflow treats an unresolved codename, placeholder, or unauthorized public
name as a readiness blocker. [Repository primary, retrieved 2026-09-21]

**Counterevidence:** The current contract also defers App Store submission and
publication, so the name is not an immediate external release requirement.

**Implication:** A provisional name can unblock product-copy, UI, and identity
design without authorizing publication, provided internal and public identity
remain explicitly separate.

### Claim 2: `WhiskerEcho` is the strongest screened alternate

**Evidence:** The name describes the cat-audio domain without claiming
classification accuracy, health interpretation, or cloud capability. It is 12
characters including no spaces, well under Apple's 30-character app-name limit.
The exact Apple Search API query for `WhiskerEcho` returned `resultCount: 0`.
[Repository primary product contract; Apple primary policy and public catalog,
retrieved 2026-09-21]

**Counterevidence:** Apple Search API coverage is not a trademark register and
can vary by storefront, indexing, and query behavior. A web search is not
reliable negative evidence here: Bing returned unrelated search noise and the
automated DuckDuckGo path triggered a bot challenge. No direct trademark
clearance was established.

**Implication:** Adopt `WhiskerEcho` as a provisional candidate for internal
product-facing artifacts only. Before any public repository, TestFlight,
App Store Connect, domain, or marketing use, run a qualified trademark search
and obtain explicit owner authorization.

### Claim 3: The strongest alternatives found are weaker

**Evidence:** Exact Apple queries returned three results for `PurrEcho` and 45
results for `MeowMemo`; one returned App Store record is “MeowMemo - Cat Food &
Journal.” `PurrVault` produced a broad 32-result response, which does not prove
an exact collision but also does not provide a clean screen. [Apple primary
public catalog, retrieved 2026-09-21]

**Counterevidence:** Search-term result counts include token and relevance
matches, not necessarily exact title collisions. The counts alone cannot prove
confusion or legal conflict.

**Implication:** These candidates should not be selected over `WhiskerEcho`
without a better name search and human review.

### Claim 4: The name must not overclaim the product

**Evidence:** The product contract limits the first slice to local capture,
replay, and deletion and forbids translation, emotion, health, welfare, and
veterinary claims. Apple requires accurate metadata, a unique app name, and
metadata that reflects the core experience. [Repository primary; Apple primary
App Review Guidelines, retrieved 2026-09-21]

**Counterevidence:** The name alone cannot establish whether the implementation
is local, bounded, reliable, or privacy-preserving.

**Implication:** Pair any future `WhiskerEcho` listing with a subtitle and
description that state the actual local, owner-started capture/replay behavior;
do not imply a general pet monitor or diagnostic tool.

## Conflicts And Unknowns

- Zero Apple Search API results conflict with the possibility of unindexed,
  storefront-specific, web-only, or trademark uses. This is an availability
  signal, not clearance.
- Search-engine outputs were inconsistent and noisy; they are retained as
  lead-only evidence and do not support a material conclusion.
- The USPTO and WIPO search entry points are JavaScript-driven; this pass
  verified the official search portals but did not complete a candidate-level
  trademark search. [USPTO/WIPO primary portals, retrieved 2026-09-21]
- Owner authorization, legal-entity ownership, bundle identifier, domain,
  social handles, and final subtitle remain unknown.
- The current product is not authorized for publication, so no name should be
  written into public distribution metadata yet.

## Decision Implications

1. Record **WhiskerEcho** as the provisional alternate for the internal
   product identity review, while retaining `meow-capture` as the code/work
   identifier until an explicit identity decision is made.
2. Treat the name blocker as conditionally unblocked for local design and
   evidence labels, not for publication or App Review readiness.
3. Before external use, obtain owner authorization and complete candidate-level
   USPTO/WIPO and relevant-market searches, plus domain and App Store checks.
4. The conclusion would change if a direct Apple listing, trademark record,
   confusingly similar product, or owner objection is found, or if user testing
   shows that “WhiskerEcho” is not understandable for the intended audience.

## Recurrence Analysis

The blocker escaped earlier review because the workflow validated build and
distribution structure before requiring an authorized public identity; the
product contract then deliberately deferred identity while the implementation
lane advanced. The immediate correction is this bounded candidate screen and a
provisional identity record. The root-cause correction is to require an
identity decision, authorization state, and collision-screen evidence as an
explicit gate before any release-facing artifact. The existing reviewer test
`test_internal_codename_cannot_reach_app_review_ready` is the mechanical guard;
it should remain green and be applied to this experiment when its distribution
metadata is introduced.

## Sources

### Primary

- Apple, “App Review Guidelines,” https://developer.apple.com/app-store/review/guidelines/ — unique name, accurate metadata, 30-character limit, and third-party-name restrictions; retrieved 2026-09-21.
- Apple, iTunes Search API exact query for `WhiskerEcho`, https://itunes.apple.com/search?term=%22WhiskerEcho%22&entity=software&limit=50 — zero software results; retrieved 2026-09-21.
- Apple, iTunes Search API query for `MeowMemo`, https://itunes.apple.com/search?term=%22MeowMemo%22&entity=software&limit=50 — direct existing listing evidence; retrieved 2026-09-21.
- Apple, iTunes Search API query for `PurrEcho`, https://itunes.apple.com/search?term=%22PurrEcho%22&entity=software&limit=50 — three software results; retrieved 2026-09-21.
- Apple, iTunes Search API query for `PurrVault`, https://itunes.apple.com/search?term=%22PurrVault%22&entity=software&limit=50 — broad result set; retrieved 2026-09-21.
- USPTO, “Search our trademark database,” https://www.uspto.gov/trademarks/search — official search portal; retrieved 2026-09-21.
- WIPO, “Global Brand Database,” https://www.wipo.int/reference/en/branddb/ — official international search portal; retrieved 2026-09-21.
- sf0.8, `docs/decisions/2026-09-20-meow-capture-product-contract.md` — product scope and authority boundary; retrieved 2026-09-21.
- sf0.8, `docs/apple-distribution-workflow.md` and `.factory/artifacts/evidence/apple-distribution/product-identity-5whys.md` — identity gate and recurrence guard; retrieved 2026-09-21.

### Secondary

- None relied upon for material claims.

### Lead-only

- Bing and DuckDuckGo searches for exact candidate strings — noisy, incomplete,
  or bot-challenged; not used as evidence of availability or collision.
