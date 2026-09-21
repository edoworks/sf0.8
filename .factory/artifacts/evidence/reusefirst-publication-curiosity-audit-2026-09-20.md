# ReuseFirst Publication Curiosity Audit

Date: 2026-09-20  
Decision owner: Founder  
Decision: Whether to publish `reusefirst` as part of the public `edoworks/artifacts` collection, and how to interpret download activity.  
Status: ADVISORY; human decision required

## Strongest charitable claim

`reusefirst` is a small, dependency-free, licensed, tested artifact with a
portable contract. Publishing it in an isolated `edoworks/artifacts` release
could let people outside Foculoom evaluate or use it, create useful feedback,
and reduce the cost of sharing a capability that already works in several
internal workflows. A download by a non-founder would be meaningful evidence
that the artifact reached an independent person, especially if that person can
show a clean-checkout execution or changed workflow.

That is the strongest version of the claim. It is not the same as claiming
that publication proves demand, product-market fit, safety in arbitrary hosts,
or economic value.

## Evidence, inference, and unknowns

| Category | Current position | Strength and limit |
| --- | --- | --- |
| Observation | The artifact has a versioned public tree/release, Apache-2.0 metadata, tests, provenance, and local-only execution boundaries. | Direct repository evidence; supports technical readiness only. |
| Observation | A bounded dogfood record reports use of the pinned public entrypoint by factory and product workflows. | Evidence of recorded internal use; it is not independent external use. |
| Observation | The local reconciliation record says the canonical `v1.2.1` release and publication approval are now verified. | Current local record; publication authority remains human-only. |
| Observation | A download counter can show that a file or release was fetched. | It does not identify the downloader, prove execution, or distinguish automation, retries, previews, or founder activity. |
| Inference | A non-founder download is stronger than a founder download as an external-reach signal. | Reasonable only if non-founder status and consented attribution are independently established. |
| Inference | A non-founder who executes the artifact in a clean environment and reports a changed workflow is evidence of external use. | Stronger behavioral evidence, but still does not prove repeat use, willingness to pay, or broad demand. |
| Unknown | Whether any downloader is independent, what they intended, whether they executed the artifact, and whether the artifact solved a material problem. | No conclusion should be drawn without a bounded evidence path. |
| Unknown | Whether the public collection can maintain support, security response, licensing, and provenance boundaries as more artifacts are added. | This is a collection-level risk, not answered by `reusefirst` tests. |

## Why not publish the bundle now

1. **The evidence is artifact-specific, not collection-wide.** `reusefirst`
   has a plausible isolated release path. Apple-distribution material,
   product-specific records, historical fixtures, and factory governance are
   not thereby generalized for public use.
2. **Publication creates an obligation, not just visibility.** Public users
   may reasonably expect accurate provenance, issue handling, security contact,
   compatibility guidance, and maintenance. The current evidence does not
   establish capacity or scope for the whole collection.
3. **A download is easy to overread.** Counting downloads as external users
   would convert a reach metric into a usage claim and could cause premature
   roadmap, support, or market conclusions.
4. **The trust boundary is still human-gated.** The factory explicitly keeps
   external publication, legal/IP ownership, privacy classification, and
   release authorization under human control. An automated signal must not
   silently promote an artifact or change repository visibility.
5. **The prior boundary defect is relevant.** An earlier staged public tree
   contained internal references and required a content-level release scan.
   That recurrence risk argues for isolated allowlisting and exact-tree review,
   not a repository-wide or bundle publication.

## High-value questions

1. What exact decision is the download signal meant to inform: reach, actual
   use, repeat use, or willingness to pay?
2. Can an independent person be identified through explicit opt-in evidence,
   without collecting unnecessary identity or private workflow data?
3. What counts as execution: a clean-checkout test, a reported integration, a
   pull request, a bug report, or a repeated workflow?
4. Who owns support and security response for the artifact, and what support
   boundary will be stated publicly?
5. Which exact files are allowlisted for release, and what blocks publication
   if private context, unsupported provenance, or rights ambiguity appears?
6. What result would justify publishing a second artifact rather than merely
   maintaining this one?

## C-suite rubber duck

- **CEO / CCO:** Publish only the smallest reversible surface. Do not use a
  public artifact collection to imply a public factory or a mature portfolio.
- **CFO:** Treat downloads as zero-dollar funnel evidence. No pricing, revenue,
  TAM, or spend decision follows without observed external value exchange.
- **CPO:** Ask whether an independent user completed a job and changed
  behavior. A download is a lead; a successful external workflow is evidence.
- **CTO:** Release an immutable, isolated tree with exact content scanning and
  a narrow support contract. Do not expose internal control-plane artifacts or
  add telemetry merely to manufacture certainty.
- **COO:** Keep the approval and evidence ledger human-gated. Record the
  artifact revision, source of the signal, consent status, and verification
  result before changing classification.
- **Legal / Trust:** Confirm ownership, license notices, trademark use,
  privacy expectations, and security-reporting obligations before publication.

## Disconfirming test

For one immutable release, define a 30-day test before expanding the
collection:

1. Record downloads as **reach only**, with timestamp, release asset, and
   known limitations. Do not label them users.
2. Offer one explicit opt-in path for an independent downloader to report
   whether they executed the artifact in a clean checkout, what job it served,
   and whether they would use it again. Do not infer identity from IP address
   or attempt covert attribution.
3. Count external use only when a non-founder provides a reproducible result,
   issue/patch, or consented workflow report tied to the immutable revision.
4. Treat repeated use or a concrete time/cost tradeoff as a separate, stronger
   signal from first execution.
5. Stop and keep the collection closed if all observed activity is founder,
   automated, unverified, one-off curiosity, or unrelated to the artifact's
   stated job.

**Falsifiable prediction:** If the artifact has genuine independent utility,
at least one consented non-founder should be able to execute the immutable
release in a clean environment and report a concrete workflow outcome during
the test window. If downloads occur but no such evidence appears, the claim
that downloads demonstrate external use is falsified for this decision.

## Recommendation

**Confidence: medium.** Do not publish the broader `edoworks/artifacts`
collection or use raw download counts as evidence of external use. Keep
publication isolated to `reusefirst` only if the founder confirms the current
release authorization, ownership/IP review, exact-tree scan, support boundary,
and canonical metadata. Treat a verified non-founder clean-checkout execution
as meaningful external-use evidence, but not as proof of demand or economics.

The recommendation changes toward broader publication if the 30-day test
produces independent, consented, revision-linked use plus an explicit owner
and support commitment. It changes toward deferral or withdrawal if rights or
privacy concerns arise, the release tree leaks private context, the artifact
cannot be executed outside the factory, or observed downloads remain
unverified and non-repeating.

## Conclusion revision

The earlier position of “prepare, but do not publish” should be narrowed, not
reversed: the current records support a human-approved isolated release of
`reusefirst`, but they do not support publishing the collection as a whole or
calling downloads external use. The revision is based on the reconciled
`v1.2.1` release record; it does not remove the independent-use and support
unknowns.

## Human escalation

Founder approval is required for publication or any visibility change. Legal
or qualified privacy review is required for rights, trademark, attribution,
or downloader-data questions. This audit authorizes no publication, telemetry,
outreach, external execution, or irreversible action.

## Referenced evidence

- `.factory/artifacts/evidence/shareable-artifacts-publication-feasibility-2026-09-19.md`
- `.factory/artifacts/evidence/shareable-artifacts-publication-5whys.md`
- `.factory/artifacts/evidence/reusefirst-customer-zero-dogfood.json`
- `.factory/artifacts/evidence/reusefirst-customer-zero-5whys-2026-09-20.md`
- `.factory/artifacts/publication-state-reconciliation.json`
- `.factory/governance.yaml`
