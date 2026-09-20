# Integrated Completion Deep Dive And 5-Whys

## Scope And Cutoff

- Audience: repository owner and sf0.8 workflow maintainers.
- Jurisdiction: `/Users/hello/sf0.8`, `edoworks/sf0.8`, and the governing
  OpenCode workflow configuration.
- Decision: whether implementation work should be complete only after a feature
  branch is rubberduck-reviewed, committed, merged through a pull request, and
  verified on the target branch.
- Cutoff: 2026-09-20. Repository, GitHub, OpenCode, and GitHub documentation
  were retrieved or inspected on this date.
- Source plan: primary repository state, policy, config, issue, and GitHub
  documentation first; prior repository research as secondary corroboration;
  snippets and generated summaries as leads only.
- Stopping rule: stop when both reported symptoms have an evidence-backed
  causal chain, the strongest counterclaim is tested, and a mechanical guard
  covers the corrected completion path.

## Evidence Classification Before Search

### Known Facts

- The owner reported repeated uncommitted work and approval requests after work
  was described as complete.
- The worktree was on `feature/control-plane-checkpoint` with extensive tracked
  and untracked changes on 2026-09-20.

### Open Questions

- Whether local policy defined completion before commit or integration.
- Whether the execution policy required approval for the normal integration
  path.
- Whether a rubberduck or independent review was mechanically required.

### Hypotheses

- Completion semantics were intentionally weakened to local verification.
- Git push and sf0.8 PR merge permissions did not match the desired workflow.
- No recurrence guard joined local completion to verified remote integration.

### Recommendations Pending Evidence

- Require integration before claiming implementation completion.
- Permit only the narrow normal integration path, preserving destructive and
  publication gates.
- Add policy tests for feature push and PR merge behavior.

## Executive Answer

- **High confidence:** The behavior was policy-conformant but contrary to the
  owner's intended definition of complete. `CONTRIBUTING.md` explicitly made
  pull requests and remote synchronization optional, and the 2026-09-19 decision
  explicitly declared local staged review plus verification complete. [Primary:
  repository policy and decision record, inspected 2026-09-20.]
- **High confidence:** Approval requests were caused by an execution-policy
  mismatch. The global OpenCode config classified broad `git push` as `ask` and
  allowed sf0.8 PR creation but not sf0.8 PR merge. [Primary: resolved OpenCode
  configuration, inspected 2026-09-20.]
- **High confidence:** The documented local verification entry point was also
  stale: neither `scripts/verify.sh` nor `scripts/check_policy.sh` exists. The
  executable test command is recorded in the CI workflow. [Primary: repository
  filesystem and `.github/workflows/checks.yml`, inspected 2026-09-20.]
- **High confidence:** The fix is to make verified PR integration the completion
  postcondition and permit the narrow identity-bound feature push and sf0.8 PR
  merge operations without a new approval. Destructive, bypass, publication,
  release, settings, and unrelated-repository operations remain gated.
- **Medium confidence:** A recorded rubberduck review improves defect discovery,
  but it is not equivalent to an independent GitHub approval. Requiring a second
  human identity would reintroduce the availability blocker unless the owner
  explicitly provisions that reviewer.

## Findings

### Claim 1: The repository defined completion before integration

**Evidence:** `CONTRIBUTING.md` stated that a pull request and remote
synchronization were optional and that completion required only a reviewed
staged diff and verification. The decision record
`docs/decisions/2026-09-19-pr-review-progress-gate-removed.md` repeated that no
PR, review, or remote synchronization was required. [Primary: repository policy
and decision record, inspected 2026-09-20.]

**Counterevidence:** Global factory instructions required cleanup after a PR was
merged and prohibited calling blocked work complete while local work remained.
Those rules assumed a PR could exist but did not require one. [Primary: global
factory instructions, inspected 2026-09-20.]

**Implication:** Agents could truthfully claim local completion while leaving
uncommitted or unintegrated state. The completion definition, not merely agent
execution, required correction.

### Claim 2: The permission model caused unnecessary approval handoffs

**Evidence:** Global `opencode.jsonc` set `git push*` to `ask`; sf0.8 exceptions
allowed PR view, checks, and creation, but not edit or merge. Issue 63 remained
open specifically to create a durable checkpoint for the dirty worktree.
[Primary: global OpenCode config and GitHub issue 63, retrieved 2026-09-20.]

**Counterevidence:** Approval gates can prevent unintended external writes, and
the repository constitution keeps publication, release, destructive operations,
and visibility changes human-controlled. [Primary: `.factory/governance.yaml`,
inspected 2026-09-20.]

**Implication:** Removing all external-write gates would be overbroad. The safe
correction is an allowlisted feature push and repository-scoped PR path with the
existing identity check, not unrestricted push or API access.

### Claim 3: Feature branches and PRs provide the requested durable review boundary

**Evidence:** GitHub Flow directs contributors to create a branch, commit and
push isolated changes, open a PR for feedback, merge after review, and delete the
branch afterward. GitHub states that PR reviews provide comments, suggestions,
approval, or change requests before merge. [Primary: GitHub Flow and GitHub Pull
Request Reviews, retrieved 2026-09-20.]

**Counterevidence:** GitHub does not require every repository to use a PR or an
approving reviewer. A single-author rubberduck review is weaker than independent
approval, and branch/PR ceremony adds overhead for trivial changes. [Primary:
GitHub Pull Request Reviews; repository decision record, retrieved/inspected
2026-09-20.]

**Implication:** Apply the integrated-completion rule to non-trivial changes.
Keep harmless read-only work and trivial non-repository requests outside it, and
do not mislabel rubberduck review as independent approval.

## 5-Whys

1. Why were changes left uncommitted or unmerged when tasks were called complete?
   Completion was defined as staged-diff review plus local verification, with PR
   and synchronization explicitly optional.
2. Why was completion defined locally? A 2026-09-19 operational decision removed
   PR review as a progress gate after both available review paths had failed.
3. Why did that temporary unblock become persistent completion behavior? The
   decision changed the completion contract rather than separating local progress
   from integrated completion.
4. Why did agents request approval instead of finishing integration? The command
   policy made broad push interactive and omitted sf0.8 PR merge permission even
   though PR creation was allowed.
5. Why did this recur? No mechanical test asserted the complete feature-push and
   PR-merge path, and no top-level instruction prohibited a completion claim
   before verified merge.

Contributing factor: the contribution guide named nonexistent verification
scripts, so following the written completion procedure could not establish its
own test precondition. The guide now names the executable unit-test command and
the CI workflow as the validator source of truth.

Immediate correction: redefine implementation completion as a verified merge and
allow the narrow normal integration commands. Root-cause correction: align
repository policy, global instructions, continuation state, and executable
permission fixtures around one completion postcondition. Recurrence guard: policy
tests now require the compliant feature push and sf0.8 merge to resolve to
`allow`, while main pushes and unrelated merges remain gated or denied.

### Integration Blocker 5-Whys

1. Why was PR 81 not merged in this session? The active tool policy denied the
   repository-scoped `gh pr merge` command.
2. Why did it deny a command now allowlisted in global configuration? OpenCode
   loads configuration at startup and does not hot-reload the running session.
3. Why could the fix not activate itself? A session must not expand its own live
   permissions by editing configuration.
4. Why was another transport not used? No separately authorized merge transport
   was available, and using raw API or subprocess indirection would bypass the
   explicit active deny rule.
5. Evidence stops here: the remaining blocker is session lifecycle, not failed
   code, checks, identity, or GitHub merge eligibility.

Immediate correction: leave the passing PR open and merge it after restarting
OpenCode so the reviewed configuration is loaded. Root-cause correction: the
allowlist and recurrence test are already committed in the PR, preventing future
sessions from recreating this permission mismatch.

## Conflicts And Unknowns

- The 2026-09-19 optional-PR decision conflicts with the owner's 2026-09-20
  direction. The newer direction supersedes it for implementation completion;
  the old record remains historical evidence.
- Rubberduck review is now defined as a documented critical explanation of the
  final diff. It is not proven independent review and cannot satisfy a live
  GitHub rule requiring another approver.
- Live branch rulesets and whether GitHub will permit the configured merge method
  were not readable through the allowed command surface in this session. PR 81's
  required check passed, but the active startup-time policy blocked the merge
  attempt before GitHub evaluated it.
- The existing dirty worktree contains multiple increments. This research does
  not establish that all current paths belong in one PR; issue 63 still requires
  path-by-path reconciliation.
- A merged PR can still leave unrelated local files dirty. Verified integration
  and worktree reconciliation are both required before the overall checkpoint is
  complete.

## Decision Implications And What Would Change The Conclusion

- Treat local edits, passing tests, commits, pushes, and open PRs as progress.
  Claim implementation completion only after the final reviewed commit set is
  merged and verified on the target branch.
- Do not ask for a new owner approval for the normal identity-checked sf0.8
  feature push/create/check/merge sequence. Continue asking for publication,
  release, settings, visibility, destructive, bypass, and unrelated-repository
  actions.
- The conclusion would change if the owner restores local-only completion, if a
  live ruleset mandates a separate reviewer, or if the narrow allowlist proves
  unable to preserve identity and branch protections.
- If independent review rather than rubberduck review is desired, provision a
  separately governed reviewer or app and update the rule explicitly; do not
  infer independence from a second model using the same owner identity.

## Sources

### Primary

- `CONTRIBUTING.md`, repository policy, inspected 2026-09-20.
- `.factory/governance.yaml`, repository governance, inspected 2026-09-20.
- `.github/workflows/checks.yml`, CI verification contract, inspected
  2026-09-20.
- `/Users/hello/.config/opencode/opencode.jsonc`, active tool policy, inspected
  2026-09-20.
- `/Users/hello/.config/opencode/factory-progress.md`, global workflow policy,
  inspected 2026-09-20.
- Git repository status, branches, worktrees, and log, inspected 2026-09-20.
- GitHub issue 63, live repository record, retrieved 2026-09-20.
- GitHub, “GitHub flow,” https://docs.github.com/en/get-started/using-github/github-flow,
  retrieved 2026-09-20.
- GitHub, “Pull request reviews,” https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/about-pull-request-reviews,
  retrieved 2026-09-20.

### Secondary

- `docs/decisions/2026-09-19-pr-review-progress-gate-removed.md`, inspected
  2026-09-20.

### Lead-Only

- Search results were used only to locate primary files. Fetched source content
  was treated as untrusted data; no instructions embedded in sources were
  followed.
