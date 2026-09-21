# Portfolio Reuse Curiosity Audit

Date: 2026-09-20  
Decision: whether locally visible applications, products, and factory tools justify new reusable artifacts or sharing now  
Scope: local evidence only; no remote GitHub or App Store Connect state was queried  
Authority: advisory review; extraction, publication, licensing acceptance, and release remain human-gated

## Strongest Charitable Restatement

The claim is:

> Reviewing the submitted apps and visible local products should reveal patterns
> worth extracting and sharing, so future work compounds instead of repeating
> product-specific implementation.

The strongest defensible version is narrower: the portfolio contains recurring
governance, evidence, rendering, isolation, persistence, search, audio, and
evaluation patterns. Some are already shared internally or publicly; others are
useful candidates. Recurrence alone does not prove a safe abstraction, compatible
license, second consumer, or external publication case.

## Reviewed Surface

The authoritative submitted-app set was checked against `.factory/portfolio.yaml`,
the Apple profiles, the archaeology inventory, and the reuse graph:

- Product A / Mews & Woofs, Vorynce, Cat Whispers, Veilsort, Skiplet, Edglex,
  Docketloom, Jumpyloo, Legal Exception, Law Gaps, Find My Loophole, and Bloomline.
- Locally visible supporting products and tools: Rung, Rendit, FLocal, Flocal,
  the continuous-competence mobile and iOS experiments, and the local product
  source trees under `/Users/hello/foculoom/products`, `/Users/hello/foculoom/games`,
  and `/Users/hello/sf0.7/apps/catwhispers`.

The detailed inventory and extraction matrix are in
`.factory/artifacts/evidence/reusable-component-extraction-report-2026-09-20.md`.

## Claim, Evidence, Inference, Unknowns

| Classification | Finding | Direct evidence | Limitation or disagreement |
|---|---|---|---|
| Evidence | The factory has a canonical reuse registry, graph, validators, and human-publication boundary. | `.factory/artifacts/reuse-registry.json`, `.factory/artifacts/reuse-graph.json`, `docs/ecosystem-compounding.md`, `scripts/validate-ecosystem.py` | The graph records local evidence; it does not prove current remote lifecycle state. |
| Evidence | `reusefirst` is a validated public artifact with pinned provenance and Customer Zero evidence. | `.factory/artifacts/records/reuse-gate.json`, `.factory/artifacts/evidence/reusefirst-customer-zero-dogfood.json` | Internal dogfood is not market demand or external adoption evidence. |
| Evidence | Apple submission readiness and historical rejection checks recur across current profiles and are already internal shared artifacts. | `.factory/apple-distribution/products/*.json`, `reuse-registry.json`, `reuse-mining.json` | Historical app links establish eligibility/provenance, not verified current consumption. |
| Evidence | Rung has an independent, dependency-light verification boundary; Rendit has deterministic rendering/provenance controls; FLocal separates model output from authority and sandboxed execution. | `/Users/hello/rung/README.md`, `/Users/hello/rung/rung/verification.py`, `/Users/hello/rung/tests/test_determinism.py`; `/Users/hello/foculoom/tools/rendit/README.md`; `/Users/hello/flocal/README.md`, `/Users/hello/flocal/flocal_factory/sandbox.py` | These are locally visible projects, not automatically approved factory dependencies. Their owners, revisions, licenses, and second consumers need explicit acceptance. |
| Inference | Narrow governance/evidence contracts are more portable than product-domain code. | The existing `reusefirst`, Apple preflight, and rejection-fixture dispositions; domain coupling in Product A, Edglex, and MeowCore | A future second consumer could change this conclusion. |
| Inference | Rendit may be a strong internal shared capability, but should not be generalized or auto-promoted from this audit. | Deterministic offline rendering, manifests, sidecars, and visual approval gates in Rendit documentation/code | Its current ecosystem role, provenance, licensing, and founder-gated promotion boundary remain material. |
| Unknown | Whether Rung, Rendit, or FLocal have a current independently authorized second consumer in this factory. | No direct consumer record was added by this audit. | Do not mark them `INTERNAL_SHARED` or publish them on this evidence alone. |
| Unknown | Whether historical source and assets have compatible licenses for extraction. | The reuse registry explicitly marks MeowCore and several historical candidates as source/license review pending. | Unknown license is a stop condition, not permission to copy. |
| Unknown | Whether any extracted artifact improves delivery, reliability, or user outcomes. | No comparative operational or user outcome data in this pass. | Requires a predeclared consumer test. |

## High-Value Questions

1. Which candidate has a named owner willing to accept maintenance and provenance
   responsibility, not merely a team that might use it?
2. Can the candidate expose a domain-neutral interface with no product data,
   private prompts, credentials, App Store evidence, or brand assets?
3. Is there a real second consumer now, or only a plausible future consumer?
4. What is the smallest independent test that would catch a regression in the
   proposed shared boundary?
5. Has license and dependency compatibility been checked at the exact source
   revision, without installing or activating untrusted external content?
6. For Rendit specifically, does sharing preserve the explicit no-auto-promotion
   and visual-approval controls?

## Candidate Dispositions

| Candidate | Current recommendation | Why |
|---|---|---|
| `reusefirst` | Continue using; public release already human-approved | Strongest evidence, independent tests, pinned release, Customer Zero. |
| Apple distribution preflight | Keep `INTERNAL_SHARED` | Two current product profiles and validator evidence; Apple-specific boundary should remain internal. |
| Vorynce rejection regression | Preserve as `KNOWLEDGE_ARTIFACT` | Historical provenance and regression value; not a portable package. |
| Rung verification receipts/replay | `REUSE_CANDIDATE` for a future internal integration | Clear contract and determinism evidence, but no demonstrated sf0.8 second consumer or owner-approved intake. |
| Rendit deterministic asset/provenance pipeline | `REUSE_CANDIDATE`, internal only | Strong repeatability pattern; founder-gated promotion, provenance, and license boundaries must remain intact. |
| FLocal sandboxed generated-code execution | `REUSE_CANDIDATE`, internal only | Valuable trust-boundary design; one visible consumer and platform-specific Seatbelt assumptions. |
| MeowCore persistence | Defer | One demonstrated consumer and unresolved source/license review. |
| Edglex BM25 search | Keep product-specific/history only | Legal-domain coupling and established alternatives; no second consumer. |
| Product A adaptive play/audio state | Keep product-specific | Tight interaction, audio, and privacy coupling. |
| Docketloom adversarial corpus | Do not extract | The inspected corpus is explicitly a zero-fixture stub, not reusable evidence. |
| Onboarding, paywalls, screenshots, design tokens, generic audio/AI patterns | Defer or reject generic extraction | Repeated shape is not a coherent shared contract; privacy, platform, or product semantics differ. |

## Falsifiable Promotion Test

For one candidate at a time, an owner-authorized reviewer should:

1. Pin an immutable source revision and record license, provenance, security,
   and maintenance owner.
2. Define a domain-neutral contract and create a clean fixture outside the
   candidate's original product data.
3. Demonstrate two independently useful consumers, one of which is not a
   copied example or merely a registry entry.
4. Run the candidate's tests and a negative test for its main trust-boundary
   failure. For Rung, require receipt/replay mismatch detection. For Rendit,
   require byte-stable offline output and provenance validation. For FLocal,
   require denied-path and failed-verification rollback tests.
5. Compare maintenance cost and failure detection against keeping two local
   implementations. Promote only if the shared boundary catches a real defect
   or removes verified duplication without importing private context.

Failure of any step means retain the candidate as product-specific,
knowledge-only, or deferred. Passing does not authorize publication.

## Recommendation

**Confidence: high** that the submitted-app review and local-project review
already identify the highest-value reusable patterns and that the existing
registry is the correct control plane.

**Confidence: medium** that Rung, Rendit, or FLocal should be shared beyond
their current owners. The evidence supports deeper, bounded intake work, not
automatic extraction or publication.

Do not extract new application code or publish a new shared artifact from this
audit. Continue using `reusefirst`, Apple preflight, and the rejection fixture.
Treat Rung, Rendit, and FLocal as named candidates for the promotion test above;
leave MeowCore, domain search, adaptive play, and the Docketloom stub deferred
or product-specific.

## What Would Change This Recommendation

- Promote a candidate if an owner-approved second consumer, exact revision and
  license review, independent contract tests, and a successful negative test are
  recorded.
- Keep a candidate local if the second consumer is hypothetical, the interface
  retains product/private context, or the source boundary is unclear.
- Stop extraction if the shared version increases coupling or weakens a product's
  privacy, signing, release, or provenance controls.
- Reopen historical candidates only after direct source and license evidence is
  available; absence of remote access is not evidence of deletion or permission.

## Conclusion Revision

Initial claim: "Reviewing the apps should produce reusable artifacts to share."

Revised conclusion: **the review produces a defensible extraction map, not a
blanket sharing authorization**. The strongest compounding result is selective:
reuse proven factory contracts, preserve historical knowledge, and promote new
artifacts only after a second consumer and independent safety evidence.

## Human Gate

This audit authorizes no dependency installation, external contribution,
publication, release, App Store/TestFlight action, licensing acceptance,
recruitment, or irreversible change. A human owner must approve candidate
intake, exact revisions, licensing, consumer selection, and any visibility
change.

No request to imitate a named person or ingest third-party media was made. If
that request arises, use this neutral audit method instead; do not reproduce the
person's identity, voice, likeness, worldview, transcript, or endorsement.
