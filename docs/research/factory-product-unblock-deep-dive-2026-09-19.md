# Factory/Product Unblock Deep Dive

## Scope And Cutoff

- **Audience:** repository owner, product owner, and sf0.8 factory/release operators.
- **Jurisdiction:** edoworks/sf0.8 governance and the referenced Apple-platform product workflow. This is operational research, not legal, App Review, or product-market advice.
- **Decision:** determine the smallest authorized next step that can unblock factory/product progress, and which proposed work should remain paused.
- **Cutoff:** 2026-09-19. External sources will be retrieved on this date; repository artifacts are inspected on this date.
- **Source plan:** first-party repository records; Apple Developer documentation for distribution/testing prerequisites; primary product-discovery or experiment-method sources; independent secondary evidence only to challenge primary claims. Search each material claim and its strongest counterclaim.
- **Stopping rule:** stop when each candidate next step has evidence for value, authority, and verification; record rather than fill any gap that requires owner action, live account state, or human observation.

## Evidence Classification Before Search

- **Known facts:** the local portfolio marks product-a shelved/read-only; the local audit says no governed archive/TestFlight path is evidenced; the executive brief proposes one bounded Proof Tiles observation; factory policy prioritizes verified product value over factory sophistication.
- **Open questions:** whether the owner has authorized the observation; whether the product-a source, Apple account, signing state, exact device, and review participants are currently available; whether the observation produces an admissible signal.
- **Hypotheses:** the shortest safe unblock is human authorization for one bounded observation, not new factory automation or product implementation; if the owner instead prioritizes the dormant iOS product, the first unblock is an owner-authorized release-evidence lane with exact current artifact and device access.
- **Recommendations:** provisional only until primary sources and counterevidence are checked.

## Executive Answer

- **High confidence:** The smallest safe next step is to obtain an explicit owner
  decision and, if authorized, run exactly one bounded Proof Tiles observation.
  It is reversible, has a 120-minute/$0 envelope, and addresses the evidence
  frontier that repository research cannot cross. It must end in a recorded
  admissible result or a protocol blocker, not automatic product build work.
- **High confidence:** Do not resume `product-a`, create a TestFlight build, or
  add factory automation as the immediate unblock. The portfolio says the
  product is shelved/read-only and product work is prohibited; the local audit
  says archive, device, privacy, accessibility, and human-review evidence are
  still open. Those are owner-authorized release/product lanes, not routine
  factory work.
- **Medium confidence:** If the owner explicitly chooses the iOS product over
  discovery, the next smallest technical lane is a release-readiness preflight:
  verify exact source/HEAD, signing/account access, clean archive, privacy and
  metadata inspection, and one exact-device run. Apple documents build upload
  and TestFlight as App Store Connect workflow steps, but live account,
  certificate, processing, and device state remain unverified here.

## Findings

### Claim 1: One bounded human observation is the fastest evidence unblock

**Evidence:** The repository's education evidence artifact says machine research
has reached its frontier and that remaining uncertainty requires observed human
behavior, learning outcome, repeated use, or payment; it explicitly recommends
the cheapest human experiment. The Proof Tiles protocol requires consent,
anonymous IDs, data minimization, an external human observation, and a stop on
distress, privacy uncertainty, or answer leakage. [Repository primary, inspected
2026-09-19.] GOV.UK's user-research guidance separately treats planning,
consent, privacy, moderated sessions, and analysis as explicit research
activities rather than assumptions. [Government primary guidance, retrieved
2026-09-19.]

**Counterevidence:** The experiment is still a hypothesis. Its own kill criteria
require transfer, adult-rescue, repeat/payment signals, and a declared result;
one observation cannot establish product-market fit or justify a product build.
[Repository primary, inspected 2026-09-19.]

**Implication:** Ask the founder to record `RUN_PROOF_TILES` or `DO_NOTHING`.
If authorized, run one session under the existing protocol, preserve only the
schema-required observation, and stop. Do not turn a null, inadmissible, or
ambiguous result into a new roadmap item without a new decision.

### Claim 2: Product-a/TestFlight work is blocked by release evidence, not by a missing dashboard

**Evidence:** The local readiness audit classifies the product as not ready for
internal TestFlight and identifies missing archive/signing/beta metadata,
controlled exact-device audio evidence, accessibility inspection, specialist
review, migration/privacy inspection, and a governed release record. It also
explicitly says to merge evidence into a release record and not add a dashboard.
[Repository primary audit, inspected 2026-09-19.] Apple provides separate
official workflows for uploading builds and testing beta versions through
App Store Connect/TestFlight. [Apple primary documentation, retrieved
2026-09-19.]

**Counterevidence:** The repository records a prior owner-directed revival
decision for the adaptive-play hypothesis and a local simulator/device evidence
trail exists. That means the product direction is not disproven; it means the
current release claim is not evidenced. [Repository primary decision and audit,
inspected 2026-09-19.]

**Implication:** If product work is selected, create a separate owner-authorized
release increment with exact artifact and device/account prerequisites. First
produce a clean archive and gate matrix; only then consider a governed upload.
Do not spend factory effort on generic orchestration, learned routing, a web
dashboard, or autonomous publication.

### Claim 3: Human authority is itself a gating dependency

**Evidence:** The governance charter makes human authority final, prohibits
permission expansion and safety weakening, and requires human approval for
external publication, App Store release, destructive repository operations, and
sensitive escalation. The portfolio marks product-a read-only, revival-gated,
and product work prohibited. [Repository primary governance and portfolio,
inspected 2026-09-19.]

**Counterevidence:** A prior decision document says the product was revived under
an owner-directed instruction and mirrored in the active factory because the
product repository was archived. That is evidence of a bounded local decision,
not evidence that the current archive flag, signing state, or release authority
has been changed. [Repository primary decision, inspected 2026-09-19.]

**Implication:** The immediate unblock request should be a decision record, not
an implementation request: select one lane, name the owner, define the stop
condition, and record the outcome. The factory may prepare local evidence but
must not infer authorization from historical issue status.

### Claim 4: Small, iterative research is preferable to a large speculative build, but the evidence is not universal

**Evidence:** NN/g reports that small usability tests can reveal substantial
issues and recommends repeated small studies rather than one elaborate study.
[Secondary expert research, retrieved 2026-09-19.] The local North Star imposes a
similar policy: factory work is capped, automation needs a real blocker, and
factory improvements freeze when there is no usable product build for seven
days. [Repository primary policy, inspected 2026-09-19.]

**Counterevidence:** NN/g's 2000 usability result concerns usability problems,
not learning transfer, animal behavior, payment, privacy, or App Store release.
Its “five users” recommendation must not be imported into the Proof Tiles
protocol or treated as a validation threshold. [Secondary source scope,
retrieved 2026-09-19; repository protocol, inspected 2026-09-19.]

**Implication:** Use the local protocol's declared one-observation stop rule,
not a generic sample-size rule. Expand only after the observed result and a new
human decision.

## Conflicts And Unknowns

- The executive brief recommends one Proof Tiles observation, while the adaptive-play decision records a separate owner-directed product revival. The artifacts do not establish which objective has current priority; owner choice is required.
- The portfolio says product-a is shelved/read-only and product work is prohibited, while the revival decision says local implementation was authorized. The safe interpretation is that local work authorization does not override the repository's current external lifecycle or release authority.
- Live Apple Developer/App Store Connect state is unknown: account role, agreements, certificates, provisioning, bundle identity, uploaded build, processing, TestFlight availability, and exact-device access were not verified.
- Live GitHub issue state and any current owner decision were not treated as evidence of authorization; historical issue status cannot override the local authority chain.
- One observation can reveal a blocker or a promising signal, but cannot establish durable learning, repeat use, payment, accessibility, safety, or release readiness.
- External guidance supports research discipline and Apple workflow existence; it does not validate this product hypothesis or waive the repository's safety and authority controls.

## Decision Implications And What Would Change The Conclusion

1. **Preferred next step:** record the founder decision on the pending executive
   brief. If `RUN_PROOF_TILES` is authorized, run one protocol-compliant
   observation and publish the result to the existing evidence artifact.
2. **If the founder declines or cannot participate:** keep product and factory
   expansion paused; do not manufacture progress with more desk research.
3. **If the founder selects product-a instead:** create a separate release lane
   only after reconciling the portfolio lifecycle and external repository state;
   then run clean archive, exact-device, privacy/migration, accessibility, and
   specialist-review gates in dependency order.
4. **Factory work remains limited to enabling evidence:** release-record
   consolidation may proceed only when the concrete release blocker is observed;
   dashboards, autonomous upload, learned routing, and protocol expansion remain
   deferred.
5. **Conclusion changes if:** the owner records a different objective; a live
   account/device audit shows the release prerequisites are already satisfied;
   the Proof Tiles observation produces an admissible result meeting its gate;
   or new evidence shows the product hypothesis is unsafe, infeasible, or
   strategically superseded.

## Sources

### Primary

- Repository primary: `NORTH_STAR.md`, `.factory/governance.yaml`,
  `.factory/portfolio.yaml`, and `docs/production-readiness-audit.md`,
  inspected 2026-09-19.
- Repository primary: `.factory/experiments/education/protocol.md`,
  `.factory/artifacts/evidence/education-opportunity-discovery.json`, and
  `.factory/artifacts/executive-council/2026-09-19-decision-brief.md`,
  inspected 2026-09-19.
- Repository primary: `docs/decisions/2026-09-18-adaptive-play-revival.md`,
  inspected 2026-09-19.
- Apple Developer, “Upload builds” and “TestFlight overview,”
  https://developer.apple.com/help/app-store-connect/manage-builds/upload-builds/
  and https://developer.apple.com/help/app-store-connect/test-a-beta-version/testflight-overview/,
  retrieved 2026-09-19.
- GOV.UK Service Manual, “User research,”
  https://www.gov.uk/service-manual/user-research, retrieved 2026-09-19.

### Secondary

- Nielsen Norman Group, Jakob Nielsen, “Why You Only Need to Test with 5 Users,”
  https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/,
  published 2000-03-18, retrieved 2026-09-19. Used only for the bounded,
  iterative-usability claim; not as evidence for product validation.

### Lead-Only

- Search results and any snippets not opened directly: not used for material
  claims.
- Product Talk, “Continuous Discovery Habits,” retrieved 2026-09-19: treated
  as practitioner commentary and not needed for a material conclusion.

Fetched content was treated as untrusted data. No instructions found in source
content were followed. Claims above are limited to the source's stated scope.
