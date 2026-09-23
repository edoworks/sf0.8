# Identity Governance Audit

Date: 2026-09-23
Scope: redacted read-only review of canonical factory records and relevant local
public/legal/product surfaces
Legal conclusion: none

This report records operational inconsistencies and review requirements. It does
not determine legal rights, clearance, registration, filing obligations, or the
correct disposition of an external record. No residential address, phone value,
credential, signing identifier, private filesystem root, or source snippet is
included.

## Discoveries

- The canonical legal entity is Foculoom LLC. Current California record facts
  still require a human check against the live Secretary of State record.
- The scanner records sanitized blockers in company documentation and
  structured product observations. These include conservative trademark-state
  mismatches, application-as-registration wording, address occurrences, and
  lifecycle, pricing, platform, feature, and privacy contradictions.
- The Foculoom public-site scan produced 32 warnings in generated Pagefind
  assets. They are email-like dependency tokens, not verified public contacts,
  and require classification or a narrow generated-asset exclusion.
- The Edoworks source text scan produced no direct text finding, but NowNest
  terms and availability state still conflict with its provisional,
  uploaded/processing status.
- Canonical public emails are `hello@foculoom.com`,
  `support@foculoom.com`, and `billing@foculoom.com`. No public phone value is
  approved by the registry.
- The observed Beverly Hills record needs a human amend-versus-close decision.
  No disposition is inferred.
- Applicable DBA/FBN jurisdiction, name, use, deadline, and
  amend/renew/abandon posture remain unknown.

Machine evidence is under
`.factory/artifacts/evidence/identity-governance/`. The scanner report contains
only codes, severity/classification, relative paths, line numbers, canonical
identity references, and redacted hashes.

## Public Inconsistencies

The following summarizes direct scanning and structured observations. Repeated
lines in the scanner report represent distinct claims or observations.

| Finding | Public paths | Disposition |
|---|---|---|
| Trademark-state wording differs from the conservative registry | `.specify/asset-provenance.md`; `AGENTS.md`; `README.md`; `docs/business/executive-summary.md`; `docs/business/full-business-plan.md`; `docs/finance/funding-readiness-checklist.md`; `docs/legal-ip/ip-asset-register.md`; `docs/legal-ip/trademark-domain-summary.md`; `docs/ops/founder-input/operations-and-compliance-workbook.md` in the Foculoom LLC company-documentation source | Update only after claim-by-claim review; rerun scanner |
| Application described as registration | `docs/legal-ip/ip-asset-register.md`; `docs/legal-ip/trademark-domain-summary.md` | Hard blocker; use application wording unless verified registration evidence exists |
| Address-like value present | `docs/business/full-business-plan.md`; `docs/ops/compliance-checklist.md` | Hard blocker; values omitted here; approve remediation strategy |
| EDOWORKS state claim exceeds registry | `docs/legal-ip/ip-asset-register.md` | Keep `CLEARANCE_REQUIRED` pending review |
| Vorynce state claim exceeds registry | `docs/legal-ip/ip-asset-register.md` | Keep `CLEARANCE_REQUIRED` pending review |
| VEILSORT state claim differs from registry | `docs/legal-ip/ip-asset-register.md` | Keep `LEGAL_REVIEW_REQUIRED` pending separate application review |
| Generated email-like tokens | `pagefind/pagefind-component-ui.js`; `pagefind/pagefind-ui.js` in the Foculoom public-site source | Warning; classify generated assets without suppressing authored-source checks |
| Veilsort state | Site and app sources disagree on App Store/TestFlight/dormant status, lifetime versus recurring pricing, supported platforms, and absolute no-network wording despite StoreKit behavior | Human product-state and privacy review |
| Skiplet state | Canonical history and current rebuild disagree on lifecycle and bundle identity; macOS export, catalog, CloudKit, and network claims are not reconciled | Human product-state and legal/privacy review |
| Docketloom state | Site surfaces say in review, coming soon, and pre-review; pricing and export claims differ from source; claims registry is incomplete | Human and legal review |
| Vorynce state | Site surfaces say in review, TestFlight, pre-review, and previously live; pricing, platform requirements, trademark wording, and retrospective claims differ | Human and legal review |
| NowNest state | Terms assert trademark treatment while the canonical identity is provisional; availability wording does not clearly reflect uploaded/processing and not accepted | Human review; preserve provisional wording |
| Rung state | Canonical state is active/degraded while source describes it as former/unsupported; paid-report and sponsorship strategy are unresolved | Human review and rename review |

The scan remains bounded. Private organization inventory is incomplete, and no
result proves that every deployed, archived, or historical surface is
consistent.

## Address Exposure

Only paths and counts are retained:

| Source | Path | Count |
|---|---|---:|
| Foculoom LLC company documentation | `docs/business/full-business-plan.md` | 1 |
| Foculoom LLC company documentation | `docs/ops/compliance-checklist.md` | 2 |

Repository history, local archived copies, and external records require a
human-approved remediation strategy. This audit made no sibling-repository,
history, archive, website, municipal, state, or federal change.

Six additional company-documentation paths reference address/public-filing
handling and require stale-reference review: `AGENTS.md`,
`docs/business/business-plan-input-checklist.md`,
`docs/finance/funding-readiness-checklist.md`, `docs/ops/pending-items.md`, and
the two founder-input tracker/workbook paths recorded in the machine evidence.

## Trademark Status

| Mark | Serial | Canonical state | Conservative statement |
|---|---:|---|---|
| FOCULOOM | `99673253` | `LEGAL_REVIEW_REQUIRED` | Live/pending application; no registration claim; separate USPTO review required |
| SKIPLET | `99731845` | `FILED` | Live/pending application; filing does not establish registration or clearance |
| VEILSORT | `99769769` | `LEGAL_REVIEW_REQUIRED` | Live/pending application; no registration claim; separate USPTO review required |

Each application needs a separate review of owner, correspondence, domicile
handling, goods, basis, status, deadlines, specimen, and statement of use. This
report does not recommend or authorize a filing.

## Identity Readiness

| Identity | Lifecycle | Identity state | Trademark state | Readiness |
|---|---|---|---|---|
| FOCULOOM | active | `ESTABLISHED` | `LEGAL_REVIEW_REQUIRED` | Existing identity; public trademark claims remain restricted |
| EDOWORKS | active | `CLEARANCE_REQUIRED` | `CLEARANCE_REQUIRED` | Not ready for unrestricted brand adoption |
| Skiplet | dormant | `ADOPTED` | `FILED` | Historical/dormant; application review still required |
| Veilsort | dormant | `ADOPTED` | `LEGAL_REVIEW_REQUIRED` | Hold further adoption pending review |
| NowNest | validating | `PROVISIONAL` | `PROVISIONAL` | Blocked from established/public-release treatment |
| Vorynce | dormant | `CLEARANCE_REQUIRED` | `CLEARANCE_REQUIRED` | Name review required before further adoption |
| Docketloom | dormant | `HISTORICAL` | `CLEARANCE_REQUIRED` | Name review required before revival |
| Rung | active | `CLEARANCE_REQUIRED` | `CLEARANCE_REQUIRED` | Name and rename review required before further promotion |

## Domain Recommendations

Ownership or prior spend does not establish name clearance.

| Classification | Domains | Recommendation |
|---|---|---|
| `CORE` | `edoworks.com`, `foculoom.com` | Maintain as core operational domains; retain separate identity review |
| `DEFENSIVE` | `foculoom.net`, `foculoom.org`, `playskiplet.com` | Maintain defensively; do not infer brand adoption |
| `PRODUCT` | `getskiplet.com`, `veilsort.com`, `docketloom.com`, `vorynce.com`, `jumpyloo.com` | Use only where `adoption_allowed` is true; otherwise hold pending identity review |
| `DO_NOT_USE_AS_BRAND` | `kanyee.com`, `taylerr.com`, `weekndd.com`, `zendayaa.com`, `rihanno.com`, `dojaaa.com` | Do not use as brands |
| `REVIEW` | `blooplo.com` | Hold for legal review |
| `RETIRE_CANDIDATE` | `legalexception.com`, `lawgaps.com`, `findmyloophole.com`, `edglex.com`, `noraze.com` | Human review before renewal, transfer, lapse, or retirement action |
| `CANDIDATE` | `diffrek.com`, `emtosa.com`, `reliatra.com`, `skiplet.com` | Hold; no adoption or additional spend without review |
| `EXPERIMENT` | `drawtobloom.com` | Hold as experiment; no adoption inference |

The deterministic row-level matrix is
`.factory/artifacts/evidence/identity-governance/final-matrix.json`; it covers
the legal entity, every governed brand/product, and every registry domain.

## App Store Blockers

Before the next NowNest App Store submission can be considered:

1. Resolve `PUBLIC_IDENTITY_UNRESOLVED` with an owner-authorized identity after
   applicable review.
2. Resolve `IDENTITY_CLEARANCE_UNRESOLVED`; `PROVISIONAL` cannot be represented
   as established.
3. Resolve `SCREENSHOTS_INVALID` with current-build device-correct evidence.
4. Clear hard public-identity scanner findings on relevant public,
   privacy/support/terms, owner/seller, trademark, and address surfaces.
5. Reconcile the website and app on lifecycle, pricing, supported platforms,
   available functionality, privacy, and trademark state.
6. Verify the Foculoom LLC seller/developer identity in App Store Connect; local
   metadata alone cannot verify the live seller record.
7. Verify that the uploaded build completed Apple processing. Current evidence
   records uploaded/processing only, not acceptance.
8. Obtain separate human submission authority after every preflight gate passes.

`can_submit` remains false. No API, upload, submission, or external mutation was
performed.

## Changes In This Increment

- Added redacted source inventory, categorized findings, address paths,
  trademark status, contact/phone inventory, App Store blockers, structured
  observations, scanner output, deterministic matrix, and two bounded root-cause
  records.
- Added a deterministic matrix generator and sanitization/coverage tests.
- Added human-action entries for government, municipal, DBA/FBN, USPTO,
  EDOWORKS, product-name, and private-address decisions.
- Added issue #132's capability binding.

## Unresolved Actions

The canonical human-action queue contains the decision records. No action is
implicitly authorized by this report. Highest-risk unresolved areas are the
private-address remediation strategy, three separate USPTO reviews, external
government/municipal record verification, EDOWORKS clearance, and Vorynce,
Docketloom, and Rung name review.
