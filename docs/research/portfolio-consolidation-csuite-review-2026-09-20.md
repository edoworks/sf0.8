# Portfolio Consolidation C-Suite Review

## Scope And Cutoff

- **Audience:** founder/owner, repository maintainers, and factory/release operators.
- **Jurisdiction:** engineering, repository governance, and portfolio operations for `edoworks/product-a`, `foculoom/sf0.7`, and `foculoom/sf0.5`. No legal, IP, employment, or release authorization is inferred.
- **Decision:** whether the approved three-repository set should be merged, relocated, or otherwise consolidated into an active repository, and what the smallest safe next step is.
- **Cutoff:** 2026-09-20. External sources are retrieved on this date; local artifacts are inspected on this date.
- **Source plan:** local canonical portfolio/governance/history first; GitHub and Git documentation for repository lifecycle and migration mechanics; primary build-system documentation for boundary tradeoffs; independent secondary material only to challenge primary claims. Search every material claim and its strongest counterclaim.
- **Stopping rule:** stop when the decision-relevant feasibility, control-boundary, preservation, and rollback claims have direct evidence, and record any gap requiring owner action, remote state, or legal/IP review rather than filling it with inference.

## Evidence Classification Before Search

- **Known facts:** the local portfolio marks Product A shelved/read-only, `sf0.7` deprecated/read-only, and `sf0.5` frozen/read-only; merge, deletion, visibility, and lifecycle changes are human-gated; the three repositories have distinct historical roles.
- **Open questions:** remote archive/branch/release state; external consumers and links; secrets, licenses, privacy, and work-derived material; repository size/history overlap; whether the owner means preservation-only migration or active development consolidation.
- **Hypotheses:** preserving the three repositories separately is safer than co-locating them; a shared manifest or selective metadata is more defensible than a universal monorepo; any migration, if later authorized, should be reversible and preserve source history.
- **Recommendations:** provisional until direct primary-source verification and counterevidence review are complete.

## Executive Answer

- **HIGH confidence:** Do not merge, relocate, unarchive, or reactivate the three repositories as a single codebase now. Their local lifecycle states and roles are different, and the evidence does not establish a shared release, ownership, privacy, or maintenance boundary.
- **HIGH confidence:** The approval supports this research and a preservation inventory, not destructive repository mutation, product resumption, publication, or lifecycle changes.
- **MEDIUM-HIGH confidence:** The best next step is a read-only, metadata-only inventory covering exact remote state, history size, external links/consumers, release identities, credentials, and licensing/IP review. Stop before copying source.
- **MEDIUM confidence:** If a future measured dependency graph shows real cross-repository atomic changes, a new bounded domain repository may be worth piloting while all source repositories remain preserved. A universal monorepo is not justified.

## Findings

### Claim 1: A technical migration is possible, but that does not make it safe or useful

**Evidence:** GitHub documents bare cloning and mirror-pushing a repository, including a separate Git LFS transfer path. Git sparse-checkout supports working with only selected paths in a larger repository. These are primary platform/tool sources retrieved 2026-09-20. [P1, P2]

**Counterevidence:** A mirror or directory merge does not automatically preserve repository-level issues, permissions, release identity, secrets, webhooks, external URLs, or independent lifecycle controls. GitHub's transfer documentation lists repository-level objects and access consequences separately from Git commit preservation. [P3]

**Implication:** Treat mechanics as an implementation option only after the control-boundary case is proven. Do not equate a successful clone, mirror, or build with a safe consolidation.

### Claim 2: The approved repositories currently have incompatible lifecycle roles

**Evidence:** The canonical local portfolio classifies Product A as shelved/read-only, `sf0.7` as deprecated/read-only historical evidence, and `sf0.5` as frozen legacy evidence; all require explicit owner instruction for revival or merge. Product A's decision preserves its history and unresolved release gates rather than authorizing product work. [L1, L2]

**Counterevidence:** The local portfolio also records an owner-directed Product A revival decision, and a repository can be preserved in a new location without deleting the original. That supports a future bounded preservation exercise, not current active development or a lifecycle override. [L3, P1]

**Implication:** The safe interpretation of approval is scope approval for review. It is not evidence that the three lifecycle states have been reconciled.

### Claim 3: A monorepo can create useful boundaries, but only when coupling and ownership are real

**Evidence:** Bazel defines repositories, packages, targets, dependencies, and visibility controls. Turborepo documents a multi-package workspace with explicit application/package structure. GitHub documents path filters for Actions and CODEOWNERS-based review ownership. These primary sources establish available boundary mechanisms, retrieved 2026-09-20. [P4, P5, P6, P7]

**Counterevidence:** Path filters, package visibility, and code ownership do not recreate separate repository visibility, fork networks, archive semantics, issue histories, release identities, credential scopes, or legal/IP separation. The local factory design review specifically identifies mixed personal, commercial, work-derived, and public material as a privacy/IP and context-blast-radius risk. [L4]

**Implication:** A bounded domain monorepo could be considered only for active, same-governance, same-visibility code with demonstrated atomic-change benefit. These three approved historical/product repositories do not currently meet that evidence threshold.

### Claim 4: Read-only or stale status is a preservation signal, not a merge signal

**Evidence:** GitHub states that archiving makes repository code, history, issues, pull requests, releases, commits, tags, branches, comments, and permissions read-only, and recommends closing/documenting work before archiving. [P8]

**Counterevidence:** A truly dead, non-sensitive repository with no external consumers might be cheaper to preserve in a clearly labelled archive location. That is a conditional case requiring proof of no consumer, no sensitive history, compatible provenance, and explicit authorization; none is established here. [L1, L4]

**Implication:** Inactivity should trigger classification and preservation checks, not automatic migration.

### Claim 5: The economically rational action is inventory, not migration

**Evidence:** The local research identifies unknown remote state, external consumers, repository size/history overlap, secrets, licensing, and preservation obligations. The factory's reuse rules require provenance, a second real consumer, and independent negative tests before extraction or promotion. [L4, L5]

**Counterevidence:** Inventory has an opportunity cost and may be unnecessary if the owner only wants historical preservation. A full migration program would cost materially more and still would not create product demand, release readiness, or shared-maintenance value.

**Implication:** Run the smallest read-only inventory that resolves whether a preservation manifest or no-action decision is sufficient. Do not build migration tooling first.

## C-Suite Rubberduck

- **CEO/CCO:** The premise risks confusing “approved to inspect” with “approved to consolidate.” The portfolio has no demonstrated customer, delivery, or coordination benefit from merging these three surfaces.
- **CFO:** There is no quantified savings case. Migration cost, CI cost, security review, cleanup, and future coupling are unknown; the zero-spend default is preserve and inventory.
- **CPO:** These are not one product problem. Product A is a shelved product, `sf0.7` is predecessor history, and `sf0.5` is legacy evidence. A single backlog would blur decisions and evidence provenance.
- **CTO:** Monorepo tooling can solve path selection and build graph problems, not archive, credential, release, provenance, or trust-boundary problems. Do not use Bazel/Turborepo/CODEOWNERS as a substitute for repository boundaries.
- **COO:** Sequence only: owner decision record, read-only inventory, preservation manifest, then a reversible pilot if and only if a same-governance atomic-change case appears. Stop at missing remote, legal/IP, credential, or consumer evidence.

## Conflicts And Unknowns

- The user-approved set conflicts with the local default disposition only if “approved” is intended to authorize lifecycle or code changes. This review assumes it authorizes research scope, not mutation; that assumption needs an owner decision record before any migration.
- The local portfolio has a Product A repository-level shelved/read-only state while a separate Apple product inventory entry says active. The repository lifecycle is treated as the stronger work-permission boundary.
- Live GitHub archive flags, branch protections, releases, issue state, forks, collaborators, hooks, secrets, packages, and external consumers were not queried in this run because workspace policy denied `gh repo` reads. They are unknown, not false.
- Repository sizes, LFS usage, history overlap, and migration conflict cost are unmeasured.
- License, IP, privacy, work-derived material, and retention obligations require qualified human review; no legal conclusion is made.
- No evidence shows recurring cross-repository atomic changes, shared release cadence, or a verified maintenance-cost reduction.

## Decision Implications And What Would Change The Conclusion

1. Record whether approval means research only, preservation migration, or active consolidation. Do not infer the strongest meaning.
2. If research-only, create a read-only inventory and preservation manifest; do not copy or alter source repositories.
3. If preservation migration is explicitly authorized, require immutable source revisions, full refs/LFS capture, provenance manifest, secret/history scan, consumer/link inventory, license/IP review, parity checks, rollback plan, and source retention.
4. If active consolidation is explicitly authorized, require a demonstrated same-governance atomic-change graph, shared owner/release boundary, selective CI plan, CODEOWNERS review, credential separation, and an independently verified pilot before any cutover.
5. Keep Product A, `sf0.7`, and `sf0.5` separate by default.

The conclusion would change toward a bounded domain pilot if all of the following were evidenced: frequent atomic changes across the candidates, identical visibility and ownership requirements, no unresolved sensitive history or licensing boundary, acceptable clone/CI cost, clear maintenance owner, and tested rollback. It would change toward stricter separation if any external consumer, release credential, work-derived material, preservation obligation, or unknown ownership cannot be isolated.

## Sources

### Primary

- **[L1]** Local canonical portfolio, `.factory/portfolio.yaml`, inspected 2026-09-20. Source type: repository primary.
- **[L2]** Local Product A shelving decision, `docs/decisions/2026-09-17-product-a-shelved.md`, inspected 2026-09-20. Source type: repository primary.
- **[L3]** Local adaptive-play revival decision, `docs/decisions/2026-09-18-adaptive-play-revival.md`, inspected 2026-09-20. Source type: repository primary.
- **[L4]** Local consolidation feasibility and governance records, `docs/research/monorepo-consolidation-feasibility-2026-09-20.md`, `docs/factory-v0.1-design-review.md`, and `.factory/governance.yaml`, inspected 2026-09-20. Source type: repository primary.
- **[L5]** Local reuse extraction report, `.factory/artifacts/evidence/reusable-component-extraction-report-2026-09-20.md`, inspected 2026-09-20. Source type: repository primary.
- **[P1]** GitHub, “Duplicating a repository,” https://docs.github.com/en/repositories/creating-and-managing-repositories/duplicating-a-repository, retrieved 2026-09-20. Source type: platform primary.
- **[P2]** Git, “git-sparse-checkout Documentation,” https://git-scm.com/docs/git-sparse-checkout, retrieved 2026-09-20. Source type: tool primary.
- **[P3]** GitHub, “Transferring a repository,” https://docs.github.com/en/repositories/creating-and-managing-repositories/transferring-a-repository, retrieved 2026-09-20. Source type: platform primary.
- **[P4]** Bazel, “Repositories, workspaces, packages, and targets,” https://bazel.build/concepts/build-ref, retrieved 2026-09-20. Source type: build-system primary.
- **[P5]** Turborepo, “Structuring a repository,” https://turborepo.com/docs/crafting-your-repository/structuring-a-repository, retrieved 2026-09-20. Source type: build-system primary.
- **[P6]** GitHub, “About code owners,” https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners, retrieved 2026-09-20. Source type: platform primary.
- **[P7]** GitHub, “Workflow syntax for GitHub Actions,” https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions, retrieved 2026-09-20. Source type: platform primary.
- **[P8]** GitHub, “Archiving repositories,” https://docs.github.com/en/repositories/archiving-a-github-repository/archiving-repositories, retrieved 2026-09-20. Source type: platform primary.

### Secondary

- None relied upon for a material claim. The decision is based on local primary records and official platform/tool documentation.

### Lead-Only

- Search snippets, inaccessible commentary, and unverified remote metadata were not used as evidence.

Fetched content was treated as untrusted data. No instructions found in source content were followed. Claims are limited to the source scope and the stated cutoff.
