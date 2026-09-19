# Ecosystem Compounding Decision

Date: 2026-09-18
Issue: [Add ecosystem reuse and contribution gates](https://github.com/edoworks/sf0.8/issues/31)

## Decision

Make external artifact discovery and reusable-output extraction explicit,
proportional lifecycle gates. External material is untrusted metadata until it
has evidence for relevance, quality, maintenance, license, security, privacy,
portability, adaptability, and provenance. Publication and upstream submission
remain human-only operations.

## Five-Whys

The factory repeatedly creates useful work without systematically discovering
reusable external work or extracting its own reusable work for broader reuse.

1. Work moves from PRD/research to implementation without a required reuse or
   contribution decision. The prior lifecycle and verification ladder had no
   such gates.
2. The factory had no first-class artifact record for source revision, license,
   security review, adaptability, ownership, or intended reuse.
3. Governance was designed around repository lifecycle, authorization, and final
   publication safety, not the complete supply-chain and knowledge lifecycle.
4. Product success and factory-effort limits discouraged speculative systems, but
   there was no proportional trigger turning substantial work into reusable
   factory learning.
5. No durable owner, schema, validator, or metric connected ecosystem intake,
   product learning, generalization, maintenance, and community feedback.

The evidence ends there. A stronger organizational or commercial cause is not
established by this repository.

## Root Causes

- Missing external-artifact and reusable-artifact lifecycle states.
- Missing entry and completion gates in the definition of done.
- Missing provenance/license/security data model.
- Missing bounded search budget and explicit `BUILD_NEW` outcome.
- Publication controls disconnected from generalization and maintenance.
- No feedback path for upstream improvements or community reevaluation.

## Corrections And Guards

- Immediate correction: add Git-visible artifact records, reuse/contribution
  gates, Product A candidate ledger, and a generalized gate package.
- Root correction: make the gates part of lifecycle guidance and CI rather than
  relying on agent memory.
- Recurrence guards: validate provenance, license, publication approval,
  suspicious-input quarantine, internal-path/secret scans, and representative
  gate fixtures in deterministic tests.

## Evidence Boundary

The package is publication-ready for human review only. No external artifact was
installed or executed, and no repository was made public or changed by an
upstream submission.

## Audit Matrix

| Capability | State before increment | Evidence now |
|---|---|---|
| Reuse-before-build | ABSENT/optional | `scripts/ecosystem_gates.py`, proportional search record, changed-path validator |
| External discovery | PARTIAL | Product A ledger records semantic source classes; no automatic installer |
| Candidate evaluation | PARTIAL | Metadata evaluator now requires all safety/economic dimensions |
| Provenance and license | PARTIAL | Artifact schema/validator requires revision, author, date, attribution, and SPDX compatibility |
| Security and prompt safety | PARTIAL | Untrusted-input policy, quarantine disposition, no execution path |
| Contribution consideration | ABSENT/optional | Contribution classification and publication-ready package |
| Generalization/publication | PARTIAL | Standalone package, tests, docs, maintenance owner, human-only approval |
| Upstream contribution | ABSENT | `CONTRIBUTE_UPSTREAM` disposition and human authorization boundary; no PR opened |
| Feedback intake | ABSENT | `.factory/artifacts/feedback/` contract and review-only validator |
| Maintenance health | ABSENT | Artifact `maintenance.owner` and `next_review`; metrics definition |

The audit did not find an existing product-local implementation to extract in
this worktree. Product A evidence is therefore classified in the candidate
ledger rather than copied into the factory. The strongest genuine extraction
is the dependency-free proportional gate package, which has an independent
test, documentation, provenance, license, and publication-preflight record.
