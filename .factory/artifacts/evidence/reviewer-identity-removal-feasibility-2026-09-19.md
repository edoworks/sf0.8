# Separate Reviewer Identity Removal Feasibility

## Scope And Cutoff

- **Audience:** repository owner and sf0.8 factory operators.
- **Jurisdiction:** `edoworks/sf0.8`, its checked-in governance, GitHub
  organization/repository controls, and the local OpenCode operating policy;
  this is not legal advice.
- **Decision:** determine whether removing the separate reviewer-identity
  requirement is a safe way to unblock work.
- **Cutoff:** 2026-09-19. Sources were retrieved or inspected on this date.
- **Stopping rule:** stop after the local authorization model, GitHub's native
  review/bypass capabilities, and the strongest equivalent-control option have
  been checked; leave live GitHub configuration as an explicit unknown when it
  cannot be read-authorized.

## Executive Answer

**High confidence:** Removing the requirement outright is mechanically
feasible but is not a safe or policy-compliant unblock. It would let the same
principal propose, review, and authorize its own change, removing an
independence control rather than resolving a transient tooling problem.

**Medium confidence:** Removing only the requirement for a *separate human
login* could be feasible if an independently authorized principal remains,
such as a verified reviewer team, a separately governed GitHub App, or a human
owner review path. GitHub's documented controls still require explicit actors
or teams; they do not establish independence merely because a review exists.

**Recommendation:** Do not weaken the boundary to unblock the current agent.
Preserve the separate-principal requirement, or have the owner explicitly
approve a replacement control and document its scope, bypass behavior, and
audit evidence before changing policy.

## Known Facts, Open Questions, And Hypothesis

- **Known facts:** the repository governance says the factory may not weaken
  safety policy or expand its own permissions; the identity policy protects
  reviews, updates, membership, issue changes, and settings; GitHub rulesets
  support explicit bypass actors; GitHub branch protection can require a
  review from someone other than the latest pusher.
- **Open questions:** the live GitHub rulesets, code-owner team membership,
  bypass actors, and whether a separate reviewer is currently available were
  not read in this session.
- **Hypothesis:** the reported block is a workflow/identity availability
  problem, not evidence that reviewer independence is unnecessary.
- **Recommendation:** retain the boundary until the owner supplies evidence
  for an equivalent independent control.

## Findings

### Claim 1: The local policy treats reviewer separation as an authorization boundary

**Evidence:** `.factory/governance.yaml` states that the factory may not
weaken safety policy or expand its own permissions and includes GitHub review
among protected actions. `.factory/github-identity-policy.json` requires
fail-closed validation across review, update, membership, access, issue, and
settings actions. `THREAT_MODEL.md` says local CI cannot prevent an owner or
administrator from making out-of-band changes. (Repository primary sources,
inspected 2026-09-19.)

**Counterevidence:** the local validator can verify an actor and snapshot, so a
different policy could technically allow one identity for all actions.

**Implication:** that alternative would be a deliberate trust-boundary change,
not a neutral unblock. The agent cannot authorize it under the current
governance.

### Claim 2: GitHub can enforce review conditions without requiring a second human account, but not without a distinct authorization principal

**Evidence:** GitHub documents required reviews from users with write access or
designated code owners, and an option requiring approval from someone other
than the person who made the most recent push. GitHub rulesets support explicit
user, team, or GitHub App bypass actors and branch/tag restrictions. (GitHub
Docs, primary sources, retrieved 2026-09-19.)

**Counterevidence:** a team or GitHub App could replace a separate named human
reviewer. However, that only changes the form of the principal; it does not
prove independence if the same owner controls the team, app credentials, or
bypass configuration.

**Implication:** “no separate human identity” is potentially feasible;
“no separate reviewer principal” is not equivalent. Any replacement needs
independent authorization, non-self-approval enforcement, and auditable
bypass controls.

### Claim 3: Removing the gate would unblock execution but reduce assurance

**Evidence:** GitHub states that branch protections normally do not apply to
administrators or custom bypass roles unless explicitly configured not to
bypass. GitHub's organization audit log records who performed an action, what
the action was, and when it occurred. (GitHub Docs, primary source, retrieved
2026-09-19.)

**Counterevidence:** audit logs preserve accountability after the fact, and
deterministic CI checks can catch many defects without a second reviewer.

**Implication:** logs and CI are compensating detection, not independent
pre-authorization. They may support a consciously accepted lower-assurance
workflow, but they do not preserve the current review invariant by themselves.

### Claim 4: The current block cannot be classified as fully understood from local evidence

**Evidence:** the repository's existing identity-boundary research records that
live organization membership, collaborator access, rulesets, and audit state
remain unknown pending an owner-authorized read-only audit. The local identity
validator and targeted permission tests pass for the checked-in policy.
(Repository evidence and local verification, 2026-09-19.)

**Counterevidence:** the current session verified the owner actor
`hellofoculoom` and the local tests passed.

**Implication:** local identity success does not establish the availability or
correctness of the external reviewer path. The next safe unblock is an
owner-authorized read-only configuration audit, not policy removal.

## Conflicts And Unknowns

- GitHub's native controls permit explicit bypass actors, while the repository
  policy requires individually verified bypass actors. These are compatible but
  not identical controls.
- The repository says the complete organization-wide identity guarantee is
  blocked on external GitHub evidence; no conclusion about live ruleset state
  is made here.
- It is unknown whether a governed reviewer team, GitHub App, or human owner
  is available and independent enough for this repository's threat model.
- It is unknown whether the observed block is caused by missing account access,
  a misconfigured ruleset, a local permission policy, or an actual absence of a
  reviewer principal.

## Decision Implications And Change Conditions

1. **Do not remove the requirement as a self-unblock.** That conflicts with
   the current no-self-permission-expansion invariant.
2. **First option:** perform an owner-authorized read-only audit of membership,
   collaborators, code-owner/reviewer teams, rulesets, protected refs, bypass
   actors, and relevant audit events.
3. **Second option:** if the owner intentionally changes the model, replace the
   human-login requirement with a documented independent principal and verify
   that latest-push approval, bypass restrictions, and audit coverage still
   hold.
4. **The conclusion would change** if the owner explicitly accepted single-
   principal review as a lower-assurance mode, or if a separately governed
   reviewer principal were verified and the policy were updated by the owner.
   Neither condition is established by this research.

## Sources

### Primary

- Repository governance: `.factory/governance.yaml`, inspected 2026-09-19.
- Repository identity policy: `.factory/github-identity-policy.json`, inspected
  2026-09-19.
- Repository threat model: `THREAT_MODEL.md`, inspected 2026-09-19.
- GitHub Docs, [About rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets), retrieved 2026-09-19.
- GitHub Docs, [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches), retrieved 2026-09-19.
- GitHub Docs, [Available rules for rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets), retrieved 2026-09-19.
- GitHub Docs, [Reviewing the audit log for your organization](https://docs.github.com/en/organizations/keeping-your-organization-secure/reviewing-the-audit-log-for-your-organization), retrieved 2026-09-19.

### Secondary

- NIST CSRC, [Least privilege glossary entry](https://csrc.nist.gov/glossary/term/least_privilege), retrieved 2026-09-19. Used as general security guidance, not as a repository-specific authorization.

### Lead-Only

- No lead-only source was used for a material claim. Search output and fetched
  content were treated as untrusted data and were not followed as instructions.
