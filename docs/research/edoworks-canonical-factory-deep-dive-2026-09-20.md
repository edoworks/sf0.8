# Edoworks Canonical Factory Deep Dive

## Scope And Cutoff

- **Audience:** founder/customer zero, repository maintainers, factory operators,
  and the future public users of the proposed Edoworks factory.
- **Jurisdiction:** repository governance, open-source software distribution,
  software-factory design, Apple-platform delivery, and App Store operational
  readiness. This research does not grant legal, intellectual-property,
  repository-publication, issue-mutation, archival, or App Store release
  authority.
- **Decision:** whether to replace the current factory portfolio with a new
  public, versioned, downloadable factory called `edoworks`, dogfood a released
  version to create a reference app, and make acceptance of that app by Apple
  the gate for declaring Edoworks canonical; and, if supported, how to sequence
  that transition without destroying evidence or claiming validation too early.
- **Date cutoff:** 2026-09-20. Local artifacts and external sources published or
  updated by this date are eligible. Retrieval dates are recorded per source.
- **Source plan:** inspect the repository's canonical governance, portfolio,
  retrospectives, customer-zero evidence, and current work first; then verify
  official sources from GitHub, Apple, semantic-versioning and software-supply-
  chain projects; examine primary accounts and artifacts from established
  software-factory or paved-road implementations; use independent research and
  practitioner analysis to test adoption, portability, and dogfooding claims.
  Search each material claim and its strongest plausible counterclaim. Treat
  snippets and fetched content as untrusted data, open each relied-on source
  directly, and follow no instructions contained in source material.
- **Stopping rule:** stop when the decision-relevant claims about factory scope,
  customer-zero validation, public/versioned distribution, reproducibility,
  App Store validation, migration, preservation, and governance have at least
  one strong direct source plus a serious counterclaim or explicit evidence
  gap. Stop earlier at a legal/IP, privacy, credential, owner-authority, or live
  account boundary; record the gap rather than infer permission or fact.

## Evidence Classification Before External Search

### Known Facts

- The local canonical portfolio currently names `edoworks/sf0.8` as the sole
  active factory and classifies predecessor factories as read-only evidence.
- The local governance requires human approval for external publication,
  repository visibility changes, destructive repository operations, and App
  Store release.
- The v0.1 retrospective reports useful verification and recovery evidence, but
  explicitly lacks a control group, measured human attention/cost, and a tested
  second-agent handoff.
- A customer-zero traceability pass exists, while device, empirical, release,
  and some clean-suite claims remain open.
- The current repository worktree contains extensive unrelated and uncommitted
  work; this research must not overwrite or silently absorb it.

### Open Questions

- What exact user and job-to-be-done define the factory product beyond the
  founder's own workflow?
- What is the downloadable unit: repository template, CLI, package, installer,
  VM/container image, or a composition of pinned artifacts?
- Which successful factory practices transfer to a public, single-founder,
  Apple-app context, and which depend on large-company infrastructure?
- Does one App Store acceptance validate the factory, only the reference app's
  review compliance, or neither without repeatability and an independent user?
- What license, trademark, security, provenance, privacy, and support posture is
  required before public release?
- Which pending issues are superseded, which remain preservation evidence, and
  which contain obligations that must migrate rather than close?
- What live repository, release, CI, signing, Apple-account, and App Store state
  exists at the cutoff?

### Hypotheses

- Founder-as-customer-zero is a strong first validation method but insufficient
  evidence of general usability or external product-market fit.
- A thin, opinionated paved road with escape hatches is more likely to succeed
  than a universal autonomous factory assembled from all prior machinery.
- Versioned, immutable releases plus a clean-room installation test are a more
  honest download contract than instructing users to clone the mutable default
  branch.
- App Store acceptance is a valuable end-to-end integration milestone, but it
  is too narrow to serve as the sole canonicality criterion.
- Existing factories should be frozen and preserved before, not destroyed or
  broadly closed before, the replacement proves migration and recovery.

### Recommendations

- No recommendation is final until direct sources and counterevidence are
  reviewed. Any proposed transition should initially be reversible, staged,
  and explicit about human-only publication, archival, issue, and release acts.

## Executive Answer

- **HIGH confidence:** Proceed with `edoworks` as a new public, versioned factory
  product, but do not immediately deprecate `sf0.8`, archive the other factories,
  or blanket-close their issues. Build and release the smallest useful factory
  first, then use the downloaded release, not its mutable working tree, to create
  a separate reference app. [L1, L2, P1, P2]
- **HIGH confidence:** Define the initial product as one opinionated Apple-app
  golden path: initialize a repository, preserve intent and authority, verify in
  clean environments, produce release evidence, and leave App Store submission
  to an explicit human. Do not reproduce the entire `sf0.8` control plane or a
  general autonomous-agent platform. [L1, L3, P3, P4, S1]
- **HIGH confidence:** App Store acceptance is a valuable end-to-end integration
  test of one generated app, but it validates neither general factory usability
  nor product-market fit. It can gate **founder-internal canonicality** for the
  Apple-app path; a second independent clean consumer should gate any claim that
  Edoworks is generally validated. [L4, P5, P6]
- **HIGH confidence:** Publish actual immutable release artifacts with a declared
  compatibility contract, checksum/attestation, exact source revision, license,
  security policy, and clean-install verification. A public repository or moving
  `main` branch alone is not a downloadable product contract. [P1, P2, P7, P8,
  P9]
- **MEDIUM-HIGH confidence:** Use pre-1.0 semantic versions while the reference
  app exposes the contract, for example `v0.1.0`; pin the reference app to an
  exact immutable release and upgrade it only through explicit version changes.
  Declare `v1.0.0` only after the public API and compatibility promise are stable.
  [P2, P7]
- **HIGH confidence:** Transition old repositories only after preservation,
  dependency, security/IP/privacy, and recovery checks. Issues should be
  classified as migrated, completed, superseded, rejected, duplicate, or retained
  evidence; closure is a documented outcome, not the objective. [L1, L5, P10]

## Findings

### Claim 1: Founder-as-customer-zero is the right first customer, not sufficient market evidence

**Evidence:** DORA describes a platform as a product for developers and advises
starting with a minimum viable platform for the most common workflow, gathering
feedback, and improving iteratively. The local design review independently
recommends an aggressively small factory around one real iOS/iPadOS app and says
repeated product pain must earn new factory capabilities. The local North Star
caps steady-state factory work and freezes it when product delivery stalls.
[Industry research/primary project records, retrieved or inspected 2026-09-20;
P3, L1, L2]

Spotify provides a relevant direct account: Backstage began as an internal
developer portal, encoded standard templates, ownership, CI/CD and documentation,
and was used internally for about four years before its open-source release.
Spotify also warned that the initial open-source version was nascent and lacked
end-to-end use cases, despite the mature internal installation having more than
100 integrations. [Company engineering primary account, retrieved 2026-09-20;
P4]

**Counterevidence:** CNCF's platform benefits are partly multiplicative: a small
number of platform teams serve many product teams and reduce duplicated work.
Those economics do not automatically apply to a single founder. The local v0.1
retrospective has no control group and did not measure human attention or agent
cost, so it establishes that the factory did not prevent useful work, not that it
outperformed a simpler workflow. [Industry consensus and repository primary,
retrieved or inspected 2026-09-20; S1, L3]

**Implication:** Treat the founder as customer zero and the reference app as a
high-fidelity first workload. Measure setup time, active human minutes, lead time,
failed attempts, escaped defects, release reproducibility, and factory bypasses.
Do not infer an external market or general developer experience from self-use.

### Claim 2: The minimum successful factory is a bounded paved road, not a universal runtime

**Evidence:** Backstage's reusable mechanism is a software template with embedded
best practices plus ownership/catalog metadata, not an assertion that every tool
must be replaced. DORA recommends a minimum viable platform, developer
independence, extensibility, and clear failure feedback. CNCF defines a platform
as an integrated collection of capabilities presented according to user needs
and emphasizes user experience. The local design review reaches the same shape:
Git, concise intent, one primary route, Xcode, deterministic verification, a tiny
ledger, and a bypass path. [Project/company/industry sources, retrieved
2026-09-20; P3, P4, S1, L1]

**Counterevidence:** DORA's 2024 research reports that internal platforms can
improve productivity and organizational performance while also decreasing change
stability and throughput when implemented poorly. Backstage solves fragmentation
at Spotify scale; adopting its portal/plugin architecture for one founder would
create the second-product failure already documented locally. [Industry research
and company primary, retrieved 2026-09-20; S2, P4, L1]

**Implication:** Edoworks v0.1 should expose one complete journey and stable
escape hatch:

```text
download verified release -> doctor -> init Apple app repo -> write/confirm PRD
-> execute one bounded increment -> deterministic verify -> release evidence
-> human-authorized Apple submission
```

The generated app must remain buildable with normal Git/Xcode commands if the
factory is unavailable. Exclude dashboards, learned routing, transcript stores,
general portfolio automation, autonomous publication, and self-modifying policy
until observed failures repeatedly justify them.

### Claim 3: Versioned downloadability requires an explicit, immutable contract

**Evidence:** GitHub defines releases as deployable iterations based on Git tags
and supplies source archives and attached assets. Its immutable releases lock the
tag and assets and generate a cryptographically verifiable release attestation.
Semantic Versioning requires a declared public API, forbids changing released
contents, and reserves `0.y.z` for unstable initial development. SLSA requires a
consistent build process and distributed provenance for produced artifacts.
[Platform/specification primary sources, retrieved 2026-09-20; P1, P2, P7, P8]

**Counterevidence:** A GitHub release archive is not automatically installable,
reproducible, supported, secure, or compatible with a user's Xcode/macOS/tool
versions. SLSA also distinguishes producer responsibilities from build-platform
controls; provenance records how an artifact was produced but does not prove it
is useful or defect-free. [Specification primary, retrieved 2026-09-20; P8]

**Implication:** Each Edoworks release should include a platform/toolchain matrix,
install and uninstall path, public API/compatibility statement, changelog and
migration notes, exact commit, immutable artifact, attestation or published
digest, license, security contact, and a clean-machine smoke receipt. The
reference app records the exact Edoworks version and artifact digest. Factory
fixes are released as new versions; the founder must not patch an unversioned
checkout and call that customer-zero validation.

### Claim 4: Public visibility is not equivalent to open-source or safe distribution

**Evidence:** The Open Source Initiative states that open source means more than
source visibility and requires distribution terms meeting the Open Source
Definition. GitHub states that an open-source license grants use, modification,
and distribution rights. GitHub's repository guidance recommends README,
license, contribution expectations, secret scanning, push protection, code
scanning, Dependabot, and a security policy; its Actions guidance emphasizes
least-privilege tokens and treating contributor-controlled values as untrusted.
[Standards/platform primary sources, retrieved 2026-09-20; P9, P11, P12]

**Counterevidence:** More community files and scanners can become ceremony and do
not establish ownership of imported material, remove secrets from history, or
make an agent workflow safe. The local design review identifies public issues,
pull requests, code, and documentation as attacker-controlled inputs and forbids
public PRs from reaching privileged release credentials. [Repository primary,
inspected 2026-09-20; L1]

**Implication:** Prefer a fresh, allowlisted public repository over changing the
visibility of `sf0.8`. Publish only after human IP/privacy/license review and
history/secret scanning. Public PR verification must be credential-free and
least-privilege; Apple credentials belong in a separately authorized trusted
release path.

### Claim 5: Apple acceptance is a strong vertical integration milestone with narrow scope

**Evidence:** Apple's review guidelines organize review around Safety,
Performance, Business, Design, and Legal and state that every App Store app is
reviewed. App Store Connect documents a submission workflow and statuses for the
submitted app/version. The local distribution contract correctly distinguishes
`APP_REVIEW_READY` from `SUBMITTED` and says readiness never means Apple will
approve. [Apple and repository primary sources, retrieved or inspected
2026-09-20; P5, P6, L4]

**Counterevidence:** Apple's sources review the app, metadata, business model,
privacy and compliance presented to Apple; they do not inspect or certify the
factory's external usability, reproducibility, architecture, cost, security, or
fitness for another developer. Approval can also depend on app-specific content
and policies unrelated to factory quality. [Apple primary source scope,
retrieved 2026-09-20; P5]

**Implication:** Make Apple acceptance one mandatory canonicality gate, not the
only gate. Record it as “one reference app produced by Edoworks release X was
accepted on date Y.” Do not state “Apple validated Edoworks.” Internal
canonicality also requires clean-download use, deterministic verification,
recovery, no unresolved critical security/privacy defect, and measured founder
value. General validation requires at least one independent second consumer.

### Claim 6: Immediate blanket issue closure and archival would destroy useful state before replacement is proven

**Evidence:** GitHub recommends closing issues and pull requests and updating the
README/description before archiving; archival then makes code, issues, releases,
tags, branches, comments, and permissions read-only. The local factory design
defines issue dispositions such as validated, superseded, invalid assumption,
duplicate, blocked, and not planned, and explicitly says lowering issue count is
not inherently success. Existing code and issues are evidence rather than
authority, but can retain defect, migration, accessibility, and user-expectation
knowledge. [Platform and repository primary sources, retrieved or inspected
2026-09-20; P10, L1]

**Counterevidence:** Leaving old issues open after a replacement is canonical can
mislead contributors and fragment attention. GitHub's own archive guidance favors
closing work first. [Platform primary, retrieved 2026-09-20; P10]

**Implication:** Use a two-stage lifecycle. At **replacement candidate**, freeze
new work in old factories, inventory refs/releases/issues/dependencies, preserve
recovery evidence, and map each still-relevant obligation. At **canonical
cutover**, close or transfer every pending issue with a machine-readable reason
and successor link, update archive notices, then archive repositories. Do not
delete repositories or rewrite history. Keep any unresolved security, legal,
privacy, retention, or migration obligation explicitly tracked until resolved.

### Claim 7: The current local state does not support an immediate cutover

**Evidence:** The canonical portfolio names `edoworks/sf0.8` as the sole active
factory. `NOW.md` names a current meow-capture product lane and parks factory
construction and repository consolidation unless they directly unblock it. The
governance file reserves publication, visibility changes, destructive repository
operations, and App Store release for a human. The current readiness audit calls
`sf0.8` partial rather than production-ready and identifies missing integrated
execution, enforced isolation, credential brokering, protected audit, and a
governed release path. [Repository primary, inspected 2026-09-20; L2, L5, L6]

**Counterevidence:** The founder's stated direction is strong evidence that the
portfolio objective may have changed. The repository already contains reusable
PRD, verification, lifecycle, recovery, and Apple-distribution components, so a
fresh thin extraction may be faster and safer than extending `sf0.8`. [User
direction and repository primary, 2026-09-20; L1-L6]

**Implication:** Record a new owner decision and make Edoworks a bounded successor
program. Do not infer that the direction itself completed publication, issue
mutation, archive, or release approvals. Reconcile the current product lane
explicitly: either choose its app as the reference workload or preserve/stop it
with a reason before beginning another app.

## Conflicts And Unknowns

- **Naming conflict:** `edoworks` is already the organization/brand while the
  proposed product is also called Edoworks. `edoworks/edoworks` is technically
  plausible, but CLI/package/domain/trademark collisions and user comprehension
  have not been checked.
- **Priority conflict:** the user direction proposes a new canonical factory,
  while current local authority names `sf0.8` active and meow-capture as the
  single lane. Only an owner decision can supersede that state.
- **Canonicality conflict:** “canonical after Apple acceptance” is reasonable for
  the founder's Apple path but overclaims if it means validated for external
  developers or non-Apple products.
- **Issue conflict:** GitHub recommends closing issues before archive, but local
  governance requires implementation/verification for “completed.” This is
  resolved by closure with explicit non-completion dispositions, not by claiming
  all pending work was done.
- The exact public repository, downloadable packaging format, supported macOS and
  Xcode versions, agent/provider dependencies, license, trademark policy,
  support promise, telemetry posture, and update mechanism are undecided.
- The reference app is not selected. Reusing meow-capture would preserve current
  focus; selecting another app would require an explicit stop/preservation
  decision and would weaken continuity evidence.
- Live GitHub repository settings, issues, protections, archives, releases,
  consumers, and organization rules were not mutated or fully inventoried.
- Live Apple Developer/App Store Connect roles, agreements, signing identities,
  bundle ID, app record, metadata, and submission state are unknown.
- No clean-machine installation of a released Edoworks artifact, independent
  user trial, support-cost measurement, or comparative baseline exists.
- License/IP/privacy review is a human or qualified-professional boundary. This
  report makes no ownership or legal conclusion.
- DORA/CNCF evidence primarily concerns organizational/internal cloud platforms;
  transfer to a solo Apple-app factory is an informed analogy, not direct proof.

## Decision Implications And What Would Change The Conclusion

1. **Record the charter before implementation.** Define Edoworks' one customer,
   one Apple-app journey, non-goals, public API, success metrics, authority
   boundaries, and candidate repository/package names. Reconcile the current
   meow-capture lane explicitly.
2. **Create a fresh public-source candidate privately first.** Extract only
   allowlisted, provenance-reviewed components from prior factories. Do not
   publish `sf0.8` history or copy private control-plane data.
3. **Ship `v0.1.0` as a real release candidate.** Include license, README,
   SECURITY, contribution/support boundaries, compatibility matrix, immutable
   artifact and attestation/digest, release notes, bootstrap/doctor/verify, and
   uninstall/recovery instructions. Verify installation from the downloaded
   asset on a clean supported environment.
4. **Dogfood without source-tree privilege.** In a separate reference-app repo,
   install the exact `v0.1.0` artifact, record its digest, and use only its public
   contract. Every factory correction becomes `v0.1.1`, `v0.2.0`, and so on;
   upgrade the app explicitly and retain migration evidence.
5. **Use product pain to control scope.** Add factory behavior only for an
   observed reference-app blocker, repeated friction, security/privacy failure,
   or release/recovery defect. Continue measuring direct-Xcode bypass as a valid
   simpler alternative.
6. **Require a release ladder.** Clean build/tests, physical-device and
   accessibility/privacy review, TestFlight, real use, exact archive, human
   submission approval, Apple disposition, and post-acceptance smoke/recovery
   evidence remain distinct gates.
7. **Declare founder-internal canonicality only after all gates pass:** the app
   was created from a downloaded immutable release; acceptance criteria and
   recovery pass; the selected app is accepted by Apple; no unresolved critical
   security/privacy issue exists; and measured founder value beats or clearly
   simplifies the baseline. Label the result narrowly.
8. **Cut over reversibly.** Freeze old factories, publish successor notices and a
   preservation manifest, map obligations, disposition every open issue with
   successor links, test recovery, then archive. Keep repositories available as
   read-only evidence; do not delete them.
9. **Gate general canonicality on a second consumer.** Require another clean
   environment or independent developer to create and verify a second app from a
   released artifact without private knowledge. This may follow internal
   canonicality; it should precede claims of general usability or `v1.0.0`.

The recommendation would change toward **immediate cutover** only if a clean
released artifact already exists, independently installs, creates the selected
app, preserves/replaces all active obligations, and proves rollback. It would
change toward **stopping Edoworks** if direct Xcode plus a small repository
template repeatedly delivers the reference app with less attention and risk, if
factory work again displaces product delivery, or if publication cannot clear
IP/privacy/security review. It would change toward a broader factory only after
multiple consumers demonstrate the same recurring needs.

## Sources

### Primary

- **[L1] Repository primary:** `docs/factory-v0.1-design-review.md`, inspected
  2026-09-20.
- **[L2] Repository primary:** `NORTH_STAR.md`, `.factory/governance.yaml`, and
  `.factory/portfolio.yaml`, inspected 2026-09-20.
- **[L3] Repository primary:** `docs/v0.1-retrospective.md` and
  `docs/decisions/2026-09-18-customer-zero-validation.md`, inspected 2026-09-20.
- **[L4] Repository primary:** `docs/apple-distribution-workflow.md`, inspected
  2026-09-20.
- **[L5] Repository primary:** `NOW.md` and `.factory/human-action-queue.json`,
  inspected 2026-09-20.
- **[L6] Repository primary:** `docs/production-readiness-audit.md` and
  `FACTORY_CONSTITUTION.md`, inspected 2026-09-20.
- **[P1] Platform primary:** GitHub, “About releases,”
  https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases,
  retrieved 2026-09-20.
- **[P2] Platform primary:** GitHub, “Immutable releases,”
  https://docs.github.com/en/code-security/concepts/supply-chain-security/immutable-releases,
  retrieved 2026-09-20.
- **[P3] Research/project primary:** DORA, “Platform engineering,”
  https://dora.dev/capabilities/platform-engineering/, retrieved 2026-09-20.
- **[P4] Company primary account:** Spotify Engineering, “What the Heck is
  Backstage Anyway?”, https://engineering.atspotify.com/2020/03/what-the-heck-is-backstage-anyway,
  retrieved 2026-09-20.
- **[P5] Regulator/platform primary:** Apple, “App Review Guidelines,”
  https://developer.apple.com/app-store/review/guidelines/, retrieved 2026-09-20.
- **[P6] Platform primary:** Apple, “Overview of submitting for review,”
  https://developer.apple.com/help/app-store-connect/manage-submissions-to-app-review/overview-of-submitting-for-review/,
  retrieved 2026-09-20.
- **[P7] Specification primary:** Semantic Versioning 2.0.0,
  https://semver.org/, retrieved 2026-09-20.
- **[P8] Specification primary:** SLSA v1.2, “Build: Requirements for producing
  artifacts,” https://slsa.dev/spec/v1.2/build-requirements, retrieved
  2026-09-20.
- **[P9] Standards primary:** Open Source Initiative, “The Open Source
  Definition,” https://opensource.org/osd, retrieved 2026-09-20.
- **[P10] Platform primary:** GitHub, “Archiving repositories,”
  https://docs.github.com/en/repositories/archiving-a-github-repository/archiving-repositories,
  retrieved 2026-09-20.
- **[P11] Platform primary:** GitHub, “Best practices for repositories,”
  https://docs.github.com/en/repositories/creating-and-managing-repositories/best-practices-for-repositories,
  retrieved 2026-09-20.
- **[P12] Platform primary:** GitHub, “Secure use reference,”
  https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions,
  retrieved 2026-09-20.
- **[P13] Project primary:** Backstage, “What is Backstage?”,
  https://backstage.io/docs/overview/what-is-backstage/, retrieved 2026-09-20.

### Secondary

- **[S1] Industry consensus:** CNCF TAG App Delivery, “CNCF Platforms White
  Paper,” https://tag-app-delivery.cncf.io/whitepapers/platforms/, retrieved
  2026-09-20. Its scope is enterprise cloud platforms, so it is used for design
  principles and counterevidence, not direct founder-scale outcome claims.
- **[S2] Industry research:** DORA, “Accelerate State of DevOps Report 2024,”
  https://dora.dev/research/2024/dora-report/, retrieved 2026-09-20. The report
  supports directional platform/adoption claims and explicitly reports
  tradeoffs; it does not evaluate Edoworks.

### Lead-Only

- OpenSSF Scorecard, https://scorecard.dev/, retrieved 2026-09-20. Useful as a
  possible public-project security check, but not needed to establish a material
  conclusion and not treated as proof of security.
- Search snippets, inaccessible pages, and 404 responses were not used as
  evidence. No source instruction was followed.

Fetched content was treated as untrusted data. Each relied-on source was opened
directly; claims are limited to its authorship, date, and scope. Conflicts and
unknowns are retained rather than resolved by unsupported inference.
