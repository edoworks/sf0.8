# Monorepo Consolidation Feasibility

Date: 2026-09-20
Evidence cutoff: 2026-09-20
Audience: repository owner and maintainers
Jurisdiction: engineering and repository governance; no legal/IP clearance is inferred

## Scope And Source Plan

Decision: whether to aggressively consolidate the portfolio into a monorepo,
especially repositories or folders marked read-only or inactive for at least a
month.

Source plan: local canonical portfolio and governance records; first-party
GitHub, Git, Bazel, Google Research, and Turborepo documentation; independent
commentary was sought but not relied on where direct retrieval failed.

Stopping rule: stop when feasibility drivers, strongest counterclaims, and
portfolio-specific unknowns are evidenced. A migration is not authorized by
this research.

Known facts: the portfolio explicitly distinguishes active, shelved/read-only,
deprecated, frozen, public, and internal surfaces. Destructive repository
operations and visibility changes require human approval. The portfolio says
that absence from local observation is not proof of deletion or safe removal.

Open questions: complete remote inventory, repository sizes and histories,
secrets/IP/privacy review, external links and consumers, release identities,
permissions, CI cost, and whether any inactive item has preservation or
revival obligations.

Hypotheses: active, related products may benefit from a bounded monorepo;
historical/read-only material is more likely to need archival preservation than
active integration; inactivity alone is not a sufficient merge criterion.

## Executive Answer

**Overall feasibility: technically feasible, operationally conditional
(HIGH confidence).** GitHub supports repository mirroring/transfers, Git
supports sparse checkouts, and modern build systems support package/workspace
boundaries. These establish mechanics, not that one portfolio repository is
the right control boundary.

**Aggressive portfolio-wide consolidation: not recommended (HIGH confidence).**
The local design review already rejects a giant portfolio monorepo because it
mixes personal, commercial, work-adjacent, and public material and expands
security/context blast radius. This directly applies to the proposed
read-only/stale sweep.

**Read-only or stale items: preserve by default; merge only after a separate
provenance and authorization review (HIGH confidence).** GitHub archival makes
all repository content, history, issues, permissions, and releases read-only;
moving such material into an active monorepo changes its access and mutation
boundary even if files are not edited.

**Best fit: federated or domain monorepos, not one universal monorepo (MEDIUM-
HIGH confidence).** Consolidate only active, same-governance, same-visibility,
same-release-boundary code that benefits from atomic changes. Keep historical
evidence, public distribution surfaces, products with distinct credentials,
and uncertain ownership separate.

## Findings

### Claim 1: The migration is mechanically possible

**Evidence:** GitHub documents bare cloning and mirror-pushing repositories,
including Git LFS handling (primary platform documentation, retrieved
2026-09-20): <https://docs.github.com/en/repositories/creating-and-managing-repositories/duplicating-a-repository>.
GitHub documents that repository transfers preserve commits and can transfer
issues, pull requests, releases, hooks, secrets, deploy keys, and LFS objects,
with caveats (primary platform documentation, retrieved 2026-09-20):
<https://docs.github.com/en/repositories/creating-and-managing-repositories/transferring-a-repository>.
Git sparse checkout supports working on only selected paths in a larger
repository (primary Git documentation, retrieved 2026-09-20):
<https://git-scm.com/docs/git-sparse-checkout>.

**Counterevidence:** These mechanisms do not automatically migrate issue
semantics, CI identities, package publishing, external URLs, ownership, or
secrets safely. A merge is a history and control-boundary migration, not a
directory copy.

**Implication:** A pilot can be run without deleting source repositories, but
it needs a reversible mirror, a manifest, and parity checks before cutover.

### Claim 2: Monorepos can improve coordination when boundaries are real

**Evidence:** Bazel models a workspace containing repositories, packages,
targets, dependencies, and visibility controls (primary build-system
documentation, retrieved 2026-09-20): <https://bazel.build/concepts/build-ref>.
Turborepo documents a multi-package workspace with explicit apps/packages
structure and shared tooling conventions (primary tooling documentation,
retrieved 2026-09-20): <https://turborepo.com/docs/crafting-your-repository/structuring-a-repository>.
Google describes a single-repository model at very large scale and the tooling
needed to make it workable (primary research publication page, retrieved
2026-09-20): <https://research.google/pubs/why-google-stores-billions-of-lines-of-code-in-a-single-repository/>.

**Counterevidence:** Those examples depend on substantial build graph,
ownership, testing, and developer tooling. Without equivalent selective CI and
dependency boundaries, a monorepo turns unrelated changes into shared cost.

**Implication:** Consolidation should follow demonstrated coupling and shared
release needs, not precede them.

### Claim 3: A universal monorepo increases security and governance risk here

**Evidence:** The local design review says mixing personal, commercial,
work-derived, and public code increases privacy/IP blast radius and context
bloat, and recommends separate repositories with selective centralization
(primary local design review, retrieved 2026-09-20):
`docs/factory-v0.1-design-review.md:120,336-354`.
The local governance contract requires human approval for destructive
repository operations and visibility changes (primary local governance,
retrieved 2026-09-20): `.factory/governance.yaml:17-27`.
GitHub notes that visibility changes affect forks, Pages, logs, security
features, and access (primary platform documentation, retrieved 2026-09-20):
<https://docs.github.com/en/repositories/creating-and-managing-repositories/setting-repository-visibility>.

**Counterevidence:** A private monorepo can still use CODEOWNERS and path-based
workflow filters. GitHub documents both path filters and path-based code
ownership (primary platform documentation, retrieved 2026-09-20):
<https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions>
and <https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners>.

**Implication:** These controls reduce review and CI noise but do not recreate
separate repository visibility, fork, audit, credential, or archival
boundaries. They are necessary controls, not proof of equivalence.

### Claim 4: Read-only and stale status are not positive merge signals

**Evidence:** GitHub defines archival as read-only for code, history, issues,
pull requests, releases, tags, branches, comments, and permissions and
recommends closing and documenting work first (primary platform documentation,
retrieved 2026-09-20):
<https://docs.github.com/en/repositories/archiving-a-github-repository/archiving-repositories>.
The local Product A decision explicitly preserves the repository, history,
PRD, handoff, evidence, and unresolved release gates; revival requires owner
instruction (primary local decision, retrieved 2026-09-20):
`docs/decisions/2026-09-17-product-a-shelved.md:4-12,51-55`.
The local portfolio marks `sf0.7` and `sf0.5` as read-only historical evidence
and requires explicit authorization for merge or revival (primary local
portfolio, retrieved 2026-09-20): `.factory/portfolio.yaml:59-85`.

**Counterevidence:** Truly dead, non-sensitive, single-owner code with no
external consumers can be cheaper to preserve in a clearly labelled archive
directory than as a separate active repository.

**Implication:** “No commit in 30 days” should trigger classification, not
automatic migration. A stale item may be dormant, intentionally frozen,
externally governed, legally sensitive, or merely unobserved.

### Claim 5: The current portfolio favors selective consolidation

**Evidence:** The canonical portfolio has one active factory, a shelved
read-only product, a deprecated read-only predecessor, a frozen legacy
factory, active products, public distribution surfaces, and internal tools
(primary local portfolio, retrieved 2026-09-20): `.factory/portfolio.yaml:4-14,22-145`.
The repository’s reuse analysis preserves provenance and declines extraction
when a second consumer or licensing-safe boundary is not evidenced (primary
local evidence, retrieved 2026-09-20):
`.factory/artifacts/evidence/reusable-component-extraction-report-2026-09-20.md:132-142`.

**Counterevidence:** Some historical products have already been consolidated
within a domain, showing that bounded consolidation can work when provenance
and the target boundary are known.

**Implication:** The likely high-value move is a portfolio manifest plus a few
domain monorepos, not a single repository containing every artifact.

## Conflicts And Unknowns

- Product A is marked shelved/read-only at repository level while an Apple
  product subsection says active; the local evidence resolves this by treating
  the higher-level repository lifecycle as the work-permission authority.
- The local reconciliation records some repositories as not locally observed;
  that is explicitly not equivalent to deleted, archived, or safe to remove.
- The evidence does not establish all remote repositories, forks, consumers,
  package registries, deployment hooks, branch protections, or secret history.
- Repository size, object count, LFS usage, and history overlap are not yet
  measured. GitHub recommends repositories remain under 1 GB where possible and
  strongly recommends under 5 GB; this is a practical constraint, not a hard
  monorepo prohibition (primary platform documentation, retrieved 2026-09-20):
  <https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github>.
- No legal/IP determination has been made for work-derived, personal, Apple,
  or public material.

## Decision Implications

1. Do not perform a portfolio-wide merge based on read-only or 30-day inactivity
   labels.
2. Keep `edoworks/product-a`, `foculoom/sf0.7`, and `foculoom/sf0.5` separate
   unless the owner explicitly authorizes a preservation-preserving migration.
3. Inventory and classify candidates into active shared domain, historical
   evidence, public distribution, internal tool, and unknown/blocked.
4. Pilot one active same-governance domain in a new monorepo while retaining
   source repositories read-only until parity, provenance, CI, release, and
   rollback checks pass.
5. Prefer shared metadata, templates, and dependency/reuse registries over
   forced source co-location.

The conclusion would change toward broader consolidation if a measured graph
shows frequent cross-repository atomic changes, identical visibility and
ownership requirements, no unresolved IP/privacy boundary, acceptable clone
and CI cost, and a tested rollback/archive plan. It would change against even
domain consolidation if external consumers, release credentials, sensitive
history, or preservation obligations cannot be isolated.

## Sources

### Primary

- Local portfolio, governance, design review, decisions, and evidence cited
  inline; retrieved 2026-09-20.
- GitHub repository duplication, transfer, visibility, archive, CODEOWNERS,
  Actions workflow, and large-file documentation cited inline; retrieved
  2026-09-20.
- Git sparse-checkout documentation; retrieved 2026-09-20.
- Bazel build reference; retrieved 2026-09-20.
- Google Research publication page on its single-repository model; retrieved
  2026-09-20.
- Turborepo repository-structuring guide; retrieved 2026-09-20.

### Secondary

- None relied upon for a material claim. Independent commentary was attempted,
  but direct retrieval was unavailable or non-authoritative in this run.

### Lead-only

- Search snippets and inaccessible monorepo commentary were not used as
  evidence and are intentionally omitted from the decision basis.
