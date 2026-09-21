# Foculoom App Store Submission Patterns

Status: complete research snapshot  
Retrieved: 2026-09-21  
Audience: Foculoom/Edoworks product and release decision-makers  
Jurisdiction: Apple App Store distribution and App Store Connect metadata/review process  
Decision: determine which recurring patterns from Foculoom-related Apple apps should inform future submissions  
Cutoff: evidence available through 2026-09-21; historical listing dates are kept distinct from retrieval dates

## Scope And Cutoff

The authoritative local Apple set contains two current candidates: Product A
(Mews & Woofs direction, never released) and Vorynce (previously released). The
historical portfolio contains eleven named app records, including six known
rejections, two removals, and three prepare-for-submission records. This report
reviews reusable submission patterns, not market demand, legal clearance, or a
prediction of Apple's decision.

Source plan: Apple primary guidance and public App Store metadata first; local
Foculoom records are repository-primary evidence for internal history; secondary
and search results are lead-only unless independently verified.

Stopping rule: stop once each decision-relevant pattern has direct primary
support or is marked unknown, and more examples would not change the proposed
release gate.

Known facts: Apple requires app privacy information for new apps and updates;
the local factory separates preparation from human-authorized submission; the
Vorynce record is rejected/TestFlight-valid but does not preserve the literal
Apple reason.

Open questions: whether every historical record reflects an actual App Store
submission; what exact screenshots and review conversation Apple saw; whether
the patterns correlate with acceptance rather than merely with preflight quality.

Hypotheses: narrow product identity, truthful metadata, reviewer-complete
evidence, and privacy/permission clarity are the strongest repeatable patterns.

## Executive Answer

- **High confidence:** Build a product-specific preflight before submission.
  The same internal contract is consumed by Product A and Vorynce, and its
  historical fixture targets identity, metadata, orientation, paywall, review
  notes, archive, accessibility, age rating, privacy, and export evidence.
  This is a Foculoom process pattern, not evidence that Apple requires this
  exact checklist. [Repository primary, retrieved 2026-09-21]
- **High confidence:** Keep public identity and metadata product-true and
  complete. Apple says apps must provide accurate privacy information, and the
  local reviewer blocks unresolved codenames/placeholders rather than guessing
  a public name. [Apple primary; repository primary, retrieved 2026-09-21]
- **High confidence:** Treat privacy as an implementation-and-metadata
  contract, not copywriting. Apple includes third-party SDK collection in the
  disclosure responsibility and requires current answers for submission.
  Local-first products have a simpler claim only if actual transmission and
  SDK behavior support it. [Apple primary, retrieved 2026-09-21]
- **Medium confidence:** Universal iPhone/iPad claims need separate evidence,
  especially screenshots, orientation, accessibility, and interruption paths.
  This is strongly indicated by the Vorynce fixture, but its literal Apple
  rejection reason is unavailable, so causation is not proven. [Repository
  primary, retrieved 2026-09-21]
- **High confidence:** Do not infer approval from a passing archive, TestFlight,
  or a polished listing. The local workflow explicitly says readiness is not
  Apple approval and reserves submission for a human-authorized release.
  [Repository primary, retrieved 2026-09-21]

## Findings

### Claim 1: A narrow, authorized identity is a release prerequisite

**Evidence:** Apple describes the App Store as curated and says apps should
change and improve; its review guidelines also distinguish the App Store from
private/family distribution. The local reviewer requires an authorized public
name and blocks internal codenames/placeholders. Product A is currently blocked
because “Mews & Woofs” is not an authorized public identity, while Vorynce has
an authorized distinctive identity. [Apple App Review Guidelines, primary,
retrieved 2026-09-21; `docs/apple-distribution-dogfood.md`, repository primary,
retrieved 2026-09-21]

**Counterevidence:** A public listing can exist with a small or niche audience;
the evidence does not establish that a distinctive name or commercial scale is
required for acceptance.

**Implication:** Resolve product name, support URL, privacy URL, category,
copyright, and discoverability before screenshot or submission work. Never
rename a blocked product automatically.

### Claim 2: Reusable submission quality is a preflight pattern, not an app feature

**Evidence:** The same `apple-distribution-preflight` contract is consumed by
Product A and Vorynce. The historical inventory records Vorynce as
`APP_STORE_REJECTED_AND_TESTFLIGHT_VALID`; the preserved reusable failure
classes are universal-orientation evidence, paywall disclosure, and missing
review notes. [`.factory/artifacts/reuse-registry.json`, repository primary,
retrieved 2026-09-21; `apple-history.json`, repository primary, retrieved
2026-09-21; `vorynce-rejection.json`, repository primary, retrieved 2026-09-21]

**Counterevidence:** The historical record says the literal Apple reason was
not recovered and the exact historical submission metadata/screenshots are
missing. The three classes are therefore regression hypotheses inferred from
post-rejection fixes, not verified Apple wording.

**Implication:** Preserve the fixture as a recurrence guard, but label reports
as “preflight blockers,” not “predicted rejection reasons.”

### Claim 3: Privacy and permissions must agree across binary, manifest, listing, and review notes

**Evidence:** Apple says privacy answers must include data collected by the app
and third-party partners, must be accurate and current, and are required for
new apps and updates. Vorynce's preserved metadata declares no collected data;
Product A's microphone direction is separately blocked on identity, metadata,
age rating, screenshots, review information, accessibility, and export rather
than being treated as a copy-only task. [Apple App Privacy Details, primary,
retrieved 2026-09-21; `docs/apple-distribution-dogfood.md`, repository primary,
retrieved 2026-09-21]

**Counterevidence:** Public metadata cannot prove runtime behavior, SDK
behavior, or App Store Connect answers. A “local” claim is not sufficient
evidence by itself.

**Implication:** For each app, test the actual data flow and permissions,
inventory SDKs, then derive privacy labels, purpose strings, review notes, and
support/privacy pages from that evidence.

### Claim 4: Universal iPhone/iPad delivery needs device-family-specific proof

**Evidence:** Vorynce is recorded as universal iOS/iPadOS, with valid
screenshots and reviewer validation but a missing orientation matrix. The
factory's release ladder separately requires iPhone and iPad simulator evidence,
accessibility review, physical-device smoke testing, and recovery testing.
[`vorynce-rejection.json`, repository primary, retrieved 2026-09-21;
`apple-distribution-dogfood.md`, repository primary, retrieved 2026-09-21;
`edoworks-factory-issues.json` F-010/F-014, repository primary, retrieved
2026-09-21]

**Counterevidence:** This is internal process evidence, not a controlled
comparison of accepted versus rejected universal apps. The App Store listing
API can show `iosUniversal` and screenshot arrays, but cannot show review
quality or actual device behavior.

**Implication:** Treat each declared device family and orientation as a tested
claim. Do not use one iPhone capture as evidence for an iPad product promise.

### Claim 5: Public listing patterns are useful for completeness, not acceptance prediction

**Evidence:** Apple's public lookup response exposes app name, description,
version/release dates, supported devices, screenshots, price, genre, seller,
ratings, and privacy-linked listing fields where present. That makes listings
useful for comparing metadata structure and user-facing claims. [Apple iTunes
Search API response for `Foculoom`, primary public catalog data, retrieved
2026-09-21]

**Counterevidence:** A public listing does not expose App Store Connect review
notes, rejected metadata versions, reviewer communication, binary evidence, or
the causal reason for approval. A search for “Foculoom” also returned unrelated
apps, so name matching is not reliable evidence of Foculoom ownership.

**Implication:** Use public listings as a presentation checklist only. Verify
ownership, bundle identity, and provenance before treating an app as a
Foculoom comparator.

## Conflicts And Unknowns

- The local registry calls Vorynce “previously released,” while the historical
  Apple record says the reviewed build was rejected. Both can be true across
  versions, but the exact accepted version is not recovered.
- Vorynce has a complete-looking metadata fixture, but its orientation matrix
  and paywall disclosure evidence are false/missing. Metadata completeness is
  not release evidence.
- Product A is described as a local microphone pet experiment, but its public
  identity is unresolved; no public App Store comparator was verified for it.
- Historical records name eleven apps, but only one exact rejection fixture is
  preserved. The remaining outcomes should not be generalized into patterns.
- No controlled evidence shows that any pattern increases acceptance
  probability. Apple review remains an external decision.
- The Apple help pages for some App Store Connect subsections are dynamic or
  moved over time. The stable App Review Guidelines and App Privacy Details
  pages were used for policy claims; broken/moved URLs were not treated as
  evidence.

## Decision Implications

Adopt the following minimum pattern for future Foculoom submissions:

1. Authorize public identity and discoverability before release metadata.
2. Maintain one product truth table covering binary behavior, privacy,
   permissions, age rating, export compliance, purchases, device families,
   screenshots, support, privacy URL, and reviewer instructions.
3. Require iPhone and iPad evidence for universal products, including
   orientation, accessibility, interruption, persistence, and recovery.
4. Require a reviewer runbook that explains first launch, permission denial,
   offline behavior, paid paths, and how to reproduce the core value.
5. Keep preflight, TestFlight, and App Review statuses distinct; require human
   authorization for upload and submission.

The conclusion would change if the missing exact Vorynce rejection message,
accepted historical submission metadata, or a second independent Foculoom
acceptance record showed that these checks were irrelevant or false blockers.
It would also change if Apple published a new requirement affecting privacy,
screenshots, device support, or AI/audio products.

## Sources

### Primary

- Apple, “App Review Guidelines,” https://developer.apple.com/app-store/review/guidelines/ — policy guidance; retrieved 2026-09-21.
- Apple, “App Privacy Details,” https://developer.apple.com/app-store/app-privacy-details/ — privacy disclosure requirements; retrieved 2026-09-21.
- Apple, iTunes Search API public software response, `https://itunes.apple.com/search?term=Foculoom&entity=software&limit=50` — public catalog fields and false-positive risk; retrieved 2026-09-21.
- Foculoom repository, `docs/apple-distribution-dogfood.md` — current Product A/Vorynce readiness; retrieved 2026-09-21.
- Foculoom repository, `.factory/artifacts/portfolio-archaeology/apple-history.json` — historical Apple outcomes; retrieved 2026-09-21.
- Foculoom repository, `.factory/artifacts/portfolio-archaeology/fixtures/vorynce-rejection.json` — preserved regression fixture; retrieved 2026-09-21.
- Foculoom repository, `.factory/artifacts/reuse-registry.json` — shared preflight contract; retrieved 2026-09-21.

### Secondary

- None relied upon for material claims. No secondary source was stronger than
  the direct Apple or repository-primary evidence available.

### Lead-only

- Generic search-engine results for Foculoom/Vorynce and unrelated public app
  listings. Not used as evidence because ownership and relevance could not be
  verified directly.
