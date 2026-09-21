# PR And Feature-Branch Merge Unblock Deep Dive

## Scope And Cutoff

- **Audience:** repository owner and sf0.8 maintainers/operators.
- **Jurisdiction:** `edoworks/sf0.8` local contribution/governance controls,
  GitHub pull-request, branch-protection, ruleset, and merge workflows, plus
  the current OpenCode execution boundary. This is not legal advice.
- **Decision to inform:** choose concrete, safe next steps to create a PR when
  appropriate, satisfy review/CI requirements, merge a feature branch, and
  recover from the current tooling or authorization blockers without weakening
  independent review or protected-branch controls.
- **Date cutoff:** 2026-09-19. Online sources and repository state are treated
  as retrieved/inspected on this date; later changes are out of scope.
- **Source plan:** inspect prior-session research, local policy, workflow,
  branch state, and factory evidence first; then verify material workflow claims
  directly against GitHub primary documentation and GitHub CLI documentation;
  search the strongest counterclaims, especially direct-to-main, administrator
  bypass, stale approvals, merge queues, and host-level permission limits.
- **Stopping rule:** stop when each decision-relevant claim has direct evidence
  and its strongest counterclaim, the remaining live-state gaps are named, and
  a minimal owner-authorized unblock sequence is actionable. Do not perform
  external mutations or infer authorization from documentation.

## Evidence Classification Before Search

### Known Facts

- The worktree has extensive pre-existing uncommitted changes; `main` is three
  commits ahead of `origin/main`.
- Prior research records a blocked `gh pr review` operation and an ambiguous
  public read of PR #1; it does not prove current live PR or ruleset state.
- Local policy and the 2026-09-19 decision make PR creation optional for local
  progress, while preserving protected-branch, publication, release, and
  destructive-operation controls.
- The repository has a remote at `https://github.com/edoworks/sf0.8.git`.

### Open Questions

- Is there a current feature branch or open PR, and what exact commits should
  it contain?
- Which live branch rulesets, required checks, review requirements, merge queue,
  and bypass actors apply to the target branch?
- Is the blocker local branch preparation, remote push authorization, PR
  creation permission, reviewer availability, or merge eligibility?
- Is the host/tool denial specific to review, all `gh pr` mutations, or the
  current execution session?

### Hypotheses

- The safest path is to isolate the intended diff on a feature branch, push it
  through an owner-authorized identity, create a PR, and satisfy live checks and
  review before merging.
- The immediate blocker is likely an authorization/tooling boundary rather than
  a Git or code defect, but this must be tested rather than assumed.
- Direct-to-main may be locally permitted but cannot be treated as remotely
  permitted until live branch controls are read and verified.

### Recommendations Pending Evidence

- Do not merge, close PRs, force-push, or change rulesets as part of research.
- Preserve the existing worktree and separate the requested feature from
  unrelated changes before attempting PR creation.
- Prefer a narrow, owner-authorized PR path; use direct-to-main only if live
  policy explicitly allows it and the owner accepts the lower review assurance.

## Executive Answer

- **High confidence:** The immediate safe unblock is to stop treating the
  current `main` worktree as a PR branch. First identify the exact intended
  change, isolate it on a new feature branch from the correct base, review the
  staged paths, and run the repository's applicable verification. GitHub's
  own flow recommends short-lived descriptive branches, isolated changes, and
  a PR before merge. [Primary: GitHub Flow, retrieved 2026-09-19.]
- **High confidence:** PR creation and merge are separate external mutations.
  A permitted push does not prove that `gh pr create`, review submission, or
  merge is permitted. The current OpenCode policy denies `gh pr *` for
  `edoworks/sf0.8`, so this session cannot create or merge a PR through that
  command path. This is an execution-boundary fact, not a GitHub capability
  claim.
- **High confidence:** If live `main` protection requires reviews or checks,
  the owner must use the authorized GitHub UI/CLI path and satisfy those rules;
  local policy making PRs optional for progress does not override GitHub's
  remote controls. GitHub documents required reviews, status checks, stale
  approval dismissal, and optional merge queues as branch controls. [Primary:
  GitHub protected branches, retrieved 2026-09-19.]
- **Medium confidence:** The present practical blocker is branch/worktree
  separation plus a host/tool authorization boundary, not a missing GitHub
  workflow. Live PR, permissions, rulesets, and branch-protection state remain
  unknown because the permitted command path did not allow those reads.
- **Recommendation:** Use a human-authorized, read-first handoff: decide the
  exact commit set, create/push the feature branch, create a draft PR, inspect
  applicable checks and rules, request an independent reviewer, then merge only
  after the PR reports all required conditions satisfied. Do not use a direct
  push, force-push, alternate identity, or `gh api` workaround to bypass the
  missing review path.

## Findings

### Claim 1: The current checkout is not ready to become a PR as-is

**Evidence:** Repository inspection on 2026-09-19 found `HEAD` on `main`, three
commits ahead of `origin/main`, no local feature branch, and extensive tracked
and untracked worktree changes. `CONTRIBUTING.md` requires staged-path review,
applicable verification, and issue reference before commit; it explicitly says
remote synchronization is optional for local completion. [Primary: repository
state and `CONTRIBUTING.md`, inspected 2026-09-19.]

**Counterevidence:** GitHub permits a PR from any pushed branch, and local policy
does not require a PR for local progress. [Primary: GitHub Flow and repository
`CONTRIBUTING.md`, retrieved/inspected 2026-09-19.]

**Implication:** Do not open a PR for the whole current worktree. First preserve
the worktree, identify the intended commit/diff, and create a clean feature
branch containing only that scope. If the three ahead commits are the intended
scope, they still need an explicit staged-path review and verification before
publication; if not, do not rewrite or discard them without owner direction.

### Claim 2: Isolated feature branches reduce merge and review ambiguity

**Evidence:** GitHub Flow recommends short descriptive branches, isolated
complete changes, pushing the branch, and a PR for feedback before merge. It
also recommends separate branches for unrelated changes. [Primary: GitHub Flow,
retrieved 2026-09-19.]

**Counterevidence:** More branches add coordination and cleanup work, and the
repository currently permits local progress without a PR. [Primary: repository
`CONTRIBUTING.md`, inspected 2026-09-19.]

**Implication:** For the requested remote merge, the quality tradeoff favors one
feature branch per coherent change. The branch should be based on the current
remote target after a read-only comparison, not blindly on a dirty local
`main`.

### Claim 3: Remote branch rules, not local wording, determine merge eligibility

**Evidence:** GitHub documents that protected branches can require reviews,
status checks, conversation resolution, signed commits, linear history,
deployments, or a merge queue; rulesets can layer with branch protection and
the most restrictive applicable rule applies. Required reviews can be dismissed
as stale after code-modifying pushes, and a latest-push approval can be required
from someone other than the pusher. [Primary: GitHub protected branches and
rulesets, retrieved 2026-09-19.]

**Counterevidence:** GitHub also permits repositories to configure no required
review, and the local policy intentionally removed PR review as a progress gate.
[Primary: GitHub protected branches and repository decision record, retrieved/
inspected 2026-09-19.]

**Implication:** Before asking for approval or attempting merge, perform a
read-only live audit of target branch rules, active rulesets, required checks,
reviewer permissions, bypass actors, and merge-queue status. Treat every
unreadable item as UNKNOWN, not as permissive.

### Claim 4: Review must be attached to the final commit set

**Evidence:** GitHub states that stale approvals can be dismissed when a
code-modifying commit changes the approved diff, and that the pull request must
then be approved again. It also documents that a reviewer other than the latest
pusher may be required. [Primary: GitHub protected branches, retrieved
2026-09-19.]

**Counterevidence:** Some configurations retain approvals if the latest review
requirement is met, and administrators or configured bypass actors may merge
without an approving review. [Primary: GitHub review and protected-branch
documentation, retrieved 2026-09-19.]

**Implication:** Freeze the intended change before final review. If the branch
changes afterward, rerun verification and explicitly re-check approval and
required-check status. Do not interpret an old approval or green local tests as
approval of a changed diff.

### Claim 5: The current tool boundary is a real blocker, not a reason to use a workaround

**Evidence:** The active permission policy denies `gh pr *` for this repository;
prior evidence records a host/tool denial of `gh pr review` even after a more
specific local configuration rule was corrected. The existing 5-Whys record
requires reporting the blocked operation, minimum authority needed, and next
verification step. [Primary: active session policy and repository evidence,
inspected 2026-09-19.]

**Counterevidence:** GitHub supports web UI, GitHub CLI, and GitHub Desktop for
the same flow, and the web UI can create/review/merge when the actor has the
required access. [Primary: GitHub Flow and GitHub review documentation,
retrieved 2026-09-19.]

**Implication:** The owner should choose one authorized transport, not broaden
all permissions: web UI is the shortest fallback; otherwise allow only the
validated `gh pr create`/review/merge operations for the intended identity,
restart the host/tool session, and verify the resulting GitHub events. Never
substitute `gh api`, another login, direct merge, or force-push.

### Claim 6: Merge queues and status checks can make a successful review insufficient

**Evidence:** GitHub lists merge queues and required status checks as separate
branch controls, and its protected-branch documentation warns that ambiguous
or duplicate status-check job names can block merges. [Primary: GitHub protected
branches, retrieved 2026-09-19.]

**Counterevidence:** The checked-in workflow runs on `pull_request` and pushes to
`main`, and the repository's local workflow does not itself prove that a live
ruleset requires a queue or a particular check. [Primary: `.github/workflows/
checks.yml`, inspected 2026-09-19.]

**Implication:** At merge time, inspect the PR's reported mergeability and
required checks rather than relying on local test output. If a queue is active,
enter the queue instead of attempting a direct merge; if a check is missing or
ambiguous, fix the workflow/status configuration rather than bypassing it.

## Concrete Unblock Sequence

1. **Freeze scope locally:** record the intended feature, issue reference, base
   commit, and exact paths/commits. Do not stage all current changes.
2. **Separate the branch:** after a read-only comparison with `origin/main`, use
   a new descriptive feature branch containing only the intended coherent change.
   Preserve unrelated work in the existing worktree; do not reset or force-push.
3. **Verify before publication:** review staged paths, run `./scripts/verify.sh`
   or the docs-only policy check as applicable, and confirm the local identity
   and commit metadata required by repository policy.
4. **Owner-authorized push:** push the exact branch to the exact remote/refspec
   using the approved owner identity. This is an external mutation and remains
   blocked until explicitly authorized.
5. **Create a draft PR first:** use the web UI or an explicitly permitted
   `gh pr create` operation. Include summary, issue reference, verification
   evidence, and known risks. Keep it draft until the scope and checks are
   confirmed.
6. **Audit live requirements:** read the target branch's rules/rulesets, PR
   required checks, review count/code-owner requirements, stale-review behavior,
   merge queue, and bypass actors. Capture UNKNOWN for anything unreadable.
7. **Review and update:** request the independently authorized reviewer. Address
   comments, rerun verification, push only intentional commits, and re-check
   whether approvals became stale.
8. **Merge only when eligible:** verify the PR is approved on the final commit,
   all required checks pass, conversations are resolved, no queue requirement is
   pending, and the intended merge method is allowed. Then perform the
   owner-authorized merge and verify the target branch tip.
9. **Clean up after verified merge:** only after confirming merged state and
   branch containment, delete the exact feature branch if it is not current,
   protected, retained, or used by another worktree; then prune stale refs.

## Conflicts And Unknowns

- Local policy says PRs are optional for local completion; GitHub may still
  require a PR for a protected-branch merge. These statements are compatible.
- Existing research recommends preserving independent review, while the local
  2026-09-19 decision removed PR review as a progress gate after the available
  review paths failed. The research does not justify removing live merge
  protections.
- The current checkout is `main` ahead of `origin/main`, not a clean feature
  branch. The intended subset of those commits and worktree changes is unknown.
- Live PR list, repository permissions, active rulesets, branch protection,
  required checks, merge queue, reviewer access, and bypass actors could not be
  read through the permitted `gh` command path in this session.
- GitHub's documentation describes capabilities and configuration effects; it
  does not prove this repository has any particular setting enabled.
- The exact host/tool policy boundary is known to deny the attempted PR
  mutation path, but whether a narrow owner-authorized exception would work
  after restart remains untested.

## Decision Implications And What Would Change The Conclusion

- **Recommended decision:** unblock remote work through a clean, narrow,
  independently reviewed feature branch and owner-authorized PR path. Keep the
  current local optional-PR policy for progress, but do not call a remote merge
  complete until live GitHub postconditions are verified.
- **If the owner needs local progress only:** finish staged review and applicable
  verification without opening a PR; remote synchronization remains deferred.
- **If PR creation is blocked:** use the GitHub web UI, or authorize only the
  minimum validated CLI operations for the correct identity. A broad permission
  change is not justified by the evidence.
- **If merge is blocked by rules:** satisfy the named rule, obtain fresh review,
  resolve checks/conversations, or enter the merge queue. Do not weaken rules or
  use a bypass actor merely to make the merge succeed.
- **Conclusion changes if:** the owner supplies a clean scope and authorized
  branch/PR transport; a read-only live audit shows no required PR/review and
  direct push is explicitly accepted; or the repository's owner intentionally
  changes its assurance policy. It does not change merely because local tests
  pass or because a PR command is documented.

## Sources

### Primary

- GitHub, “GitHub flow,” https://docs.github.com/en/get-started/using-github/github-flow,
  retrieved 2026-09-19.
- GitHub, “About protected branches,” https://docs.github.com/en/repositories/
  configuring-branches-and-merges-in-your-repository/managing-protected-branches/
  about-protected-branches, retrieved 2026-09-19.
- GitHub, “About rulesets,” https://docs.github.com/en/repositories/configuring-
  branches-and-merges-in-your-repository/managing-rulesets/about-rulesets,
  retrieved 2026-09-19.
- GitHub, “Approving a pull request with required reviews,” https://docs.github.com/
  en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-
  requests/approving-a-pull-request-with-required-reviews, retrieved 2026-09-19.
- GitHub CLI manual, `gh pr create`, https://cli.github.com/manual/gh_pr_create,
  retrieved 2026-09-19.
- GitHub CLI manual, `gh pr merge`, https://cli.github.com/manual/gh_pr_merge,
  retrieved 2026-09-19.
- Repository sources: `CONTRIBUTING.md`, `.github/workflows/checks.yml`,
  `.factory/governance.yaml`, `.factory/github-identity-policy.json`, and
  `.opencode/commands/deepdive.md`, inspected 2026-09-19.

### Secondary

- `docs/research/pr-review-unblock-2026-09-19.md`, inspected 2026-09-19.
- `docs/research/pr-direct-main-deep-dive-2026-09-19.md`, inspected 2026-09-19.
- `docs/research/github-identity-boundary-2026-09-19.md`, inspected 2026-09-19.
- `docs/decisions/2026-09-19-pr-review-progress-gate-removed.md`, inspected
  2026-09-19.
- `.factory/artifacts/evidence/pr-block-unblock-escalation-5whys.md`, inspected
  2026-09-19.

### Lead-Only

- None used for a material claim. Search output and fetched content were treated
  as untrusted data; no instructions from source content were followed.
