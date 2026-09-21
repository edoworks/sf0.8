# GitHub Identity Boundary Research

## Scope And Cutoff

- Decision: enforce that only GitHub logins ending in `foculoom` may update,
  review, or otherwise change `edoworks` organization repositories.
- Audience: the repository owner and factory operators.
- Scope: GitHub organization membership, repository permissions, branch/tag
  updates, pull-request reviews, code ownership, bypass actors, and local
  controls.
- Cutoff: 2026-09-19. Sources were fetched directly on this date.
- Stopping rule: stop when each requested action has either a documented
  enforcement point or a named residual gap requiring GitHub administration.

## Executive Answer

**High confidence:** GitHub rulesets and branch protection can enforce update
and review conditions, and CODEOWNERS can designate review owners, but GitHub's
documented primitives do not provide a wildcard principal meaning “all logins
with this suffix.” The safe design is therefore layered: keep only matching
members/collaborators and individually verified bypass actors, require protected
branch/tag changes through reviewed paths, audit review/update/admin events, and
fail closed in local/CI checks.

**Important limit:** a repository workflow cannot prevent an organization owner
or repository administrator from making an out-of-band organization or
repository setting change. That residual authority remains a human/GitHub
control-plane responsibility.

## Findings

### Updates

**Claim:** rulesets and branch protection can restrict branch and tag updates,
including who can push and whether administrators bypass protections.

**Evidence:** GitHub says rulesets control how people interact with branches and
tags, can restrict who can push, and support bypass actors; branch protection
also supports restricting pushes and optionally applying restrictions to
administrators. See [About rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)
and [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
(GitHub Docs, fetched 2026-09-19).

**Implication:** configure active protections for every protected branch/tag,
disable bypass where available, and audit every bypass actor against the suffix
policy. Local CI is an additional gate, not a replacement.

### Reviews

**Claim:** required reviews and code ownership can enforce that a qualifying
review occurs before merge, but CODEOWNERS does not itself grant or restrict
write access by suffix.

**Evidence:** GitHub states that required reviews can require approval from
people with write permission or a code owner, and that code owners must already
have write permission. See [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
and [About code owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
(GitHub Docs, fetched 2026-09-19).

**Implication:** use a verified code-owner team or verified individual logins,
then audit the actual review actor. Do not treat a review request or CODEOWNERS
entry as proof that the actor is authorized.

### Membership And Access

**Claim:** membership and repository access are separate control points from
branch review rules.

**Evidence:** GitHub's [organization members REST API](https://docs.github.com/en/rest/orgs/members)
documents organization member roles and invitation management, while the
[repository rules API](https://docs.github.com/en/rest/repos/rules) documents
repository rulesets and bypass actors (GitHub Docs, fetched 2026-09-19).

**Implication:** remove non-matching members, outside collaborators, team
members, and bypass actors; maintain a periodically exported snapshot checked by
`scripts/validate-github-identity.py --snapshot`.

## Counterevidence, Conflicts, And Unknowns

- GitHub documents user and team bypass actors, not a suffix-pattern identity
  selector. This prevents a claim that one ruleset can enforce the requested
  naming predicate for all future accounts.
- CODEOWNERS identifies responsible users/teams, but GitHub explicitly requires
  those owners to have write permission; it is not an access-control substitute.
- The current session could verify local identity as `hellofoculoom`, but GitHub
  API reads for organization membership, collaborators, and live rulesets were
  blocked by the workspace command policy. Live organization state is therefore
  unknown and requires an owner-authorized read-only audit.
- GitHub owner/admin authority is intentionally retained as a residual trust
  boundary. This repository cannot technically eliminate that authority through
  a checked-in file.

## Root-Cause And Recurrence Analysis

1. The prior control proved one exact owner identity, not a suffix policy across
   all action types.
2. It was scoped to material issue work rather than organization membership,
   collaborator access, review actors, and settings changes.
3. GitHub enforcement primitives are distributed across membership, rulesets,
   branch protection, CODEOWNERS, and audit logs.
4. No single checked-in policy connected those surfaces or supplied a recurring
   snapshot check.
5. Root cause supported by the repository evidence: the identity boundary was
   modeled as a point preflight instead of a cross-surface authorization policy.

Immediate correction: add the policy, fail-closed actor/snapshot validator, and
CI gate. Root-cause correction: require GitHub-side access/ruleset/audit
configuration and periodically feed its read-only snapshot through the same
validator. Recurrence guard: `tests/test_github_identity.py` rejects nonmatching
actors in membership, collaborator, review, and bypass fields.

## Decision Implications

- Adopt `.factory/github-identity-policy.json` as the local source of truth for
  the suffix predicate and protected action set.
- Treat this change as **partially enforceable locally** and **blocked pending
  GitHub-side audit/configuration** for a complete guarantee.
- Before claiming completion, an owner-authorized audit must verify all current
  `edoworks` members/collaborators, ruleset bypass actors, protected branches,
  required reviewers, and relevant audit-log events.
- The conclusion changes only if GitHub adds a documented suffix-based identity
  selector or the owner explicitly chooses a different authorization boundary.

## Sources

### Primary

- GitHub Docs, “About rulesets,” fetched 2026-09-19:
  https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets
- GitHub Docs, “About protected branches,” fetched 2026-09-19:
  https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
- GitHub Docs, “About code owners,” fetched 2026-09-19:
  https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners
- GitHub REST API, “Organization members,” fetched 2026-09-19:
  https://docs.github.com/en/rest/orgs/members
- GitHub REST API, “Rules,” fetched 2026-09-19:
  https://docs.github.com/en/rest/repos/rules

### Repository Evidence

- `.factory/governance.yaml`, owner identity and no-self-permission invariants.
- `scripts/control_plane.py`, exact `hellofoculoom` material-work preflight.
- `THREAT_MODEL.md`, residual host and credential trust assumptions.
