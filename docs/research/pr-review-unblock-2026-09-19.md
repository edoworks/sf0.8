# Reviewed PR Unblock Research

## Scope And Cutoff

- **Audience:** repository owner and sf0.8 factory operators.
- **Jurisdiction:** `edoworks/artifacts` reviewed-PR workflow, GitHub rulesets/
  branch protection, the checked-in sf0.8 governance and identity policy, and
  the local OpenCode tool policy. This is not legal advice.
- **Decision:** determine how to unblock the reviewed-PR path without removing
  reviewer independence or bypassing repository protections.
- **Cutoff:** 2026-09-19. Sources were retrieved or inspected on this date.
- **Stopping rule:** stop after each safe option has direct documentation, its
  required authority is identified, and any live GitHub state that cannot be
  read-authorized is recorded as unknown.

## Executive Answer

**High confidence:** The safest immediate unblock is a human reviewer using
GitHub's web UI to review and approve the existing PR. GitHub documents the
Files changed -> Review changes -> Approve -> Submit review flow, and the
repository's existing evidence names `supportfoculoom` as the intended
reviewer. [GitHub primary documentation, retrieved 2026-09-19.]

**High confidence:** If the host policy owner intentionally permits it, the
validated reviewer identity can perform the same review through `gh pr review`.
This is a policy/tooling change, not a reason to use `gh api`, another identity,
or a direct merge. The command must be retried only after restart and identity
verification. [GitHub CLI primary documentation, retrieved 2026-09-19;
repository evidence, inspected 2026-09-19.]

**High confidence:** Removing the separate-reviewer requirement, approving with
the proposing identity, merging directly, or treating passing CI as a review
substitute is not a safe unblock under current governance. GitHub supports
required reviews and an option requiring approval from someone other than the
latest pusher; the local policy additionally requires a separately verified
review actor. [GitHub primary documentation and repository policy, retrieved or
inspected 2026-09-19.]

## Known Facts, Open Questions, Hypotheses, Recommendations

- **Known facts:** the branch is pushed; the reviewed-PR workflow is not yet
  enforced; local CI is green; the local identity policy is fail-closed; the
  prior `gh pr review` attempt was denied by the host/tool execution layer.
- **Open questions:** whether PR #1 is still open, whether `supportfoculoom`
  currently has the required repository permission, which live rulesets apply,
  and whether the reviewer can access the web UI.
- **Hypothesis:** the current blocker is reviewer/tool availability rather than
  a defect in the branch or a need to weaken review policy.
- **Recommendation:** use the web-review path first; otherwise have the owner
  change the host/tool permission for the validated reviewer action, restart,
  and verify the review actor and resulting GitHub review event.

## Findings

### Claim 1: A web review can unblock the PR without changing repository policy

**Evidence:** GitHub documents reviewing changed files, selecting **Approve**,
and submitting the review. GitHub also states that pull-request authors cannot
approve their own pull requests. [Primary: GitHub, “Approving a pull request
with required reviews,” retrieved 2026-09-19.]

**Counterevidence:** the reviewer still needs sufficient repository access, and
the PR may have additional pending, stale, or rejected reviews. [Primary:
GitHub, “About protected branches,” retrieved 2026-09-19.]

**Implication:** ask the independent reviewer to review PR #1 in the web UI,
then verify the approval is attached to the current commit and that all required
checks pass. This is the lowest-change path.

### Claim 2: Permitting `gh pr review` is a valid tooling unblock only for the
already-authorized reviewer identity

**Evidence:** GitHub CLI exposes a dedicated pull-request review command, while
the REST API documents review creation with `APPROVE`, `REQUEST_CHANGES`, or
`COMMENT` events. [Primary: GitHub CLI manual, “gh pr review,” retrieved
2026-09-19; GitHub REST API, “Pull request reviews,” retrieved 2026-09-19.]

**Counterevidence:** an API or CLI call is still an external review mutation;
changing the transport does not establish reviewer independence. The local
5-Whys record says the host/tool execution layer is a separate enforcement plane
and specifically rejects substituting `gh api` or another identity. [Primary:
repository evidence, inspected 2026-09-19.]

**Implication:** the owner may authorize the minimum host/tool permission for
`gh pr review`, then restart OpenCode, validate the reviewer login, submit the
review, and verify the resulting GitHub event. No broader GitHub API or push
permission is needed.

### Claim 3: GitHub protections support independent review and should remain
enabled

**Evidence:** GitHub allows required reviews from users with write permission or
designated code owners, can require approval from someone other than the latest
pusher, and supports ruleset bypass actors and active rulesets. [Primary:
GitHub, “About protected branches,” “About rulesets,” and “Available rules for
rulesets,” retrieved 2026-09-19.]

**Counterevidence:** repository administrators or configured bypass roles may
be able to merge or bypass protections unless the repository explicitly
disallows bypass. [Primary: GitHub, “About protected branches,” retrieved
2026-09-19.]

**Implication:** a read-only owner audit should verify the live rulesets,
protected branch settings, reviewer/team access, bypass actors, and audit log.
Do not infer live configuration from local files or green CI.

### Claim 4: CODEOWNERS or CI alone does not solve the current identity block

**Evidence:** GitHub requires code owners to have write access; CODEOWNERS
requests review but is not a suffix-based access-control mechanism. GitHub's
audit log records actor, action, resource, and time, but is retrospective.
[Primary: GitHub, “About code owners” and “Reviewing the audit log for your
organization,” retrieved 2026-09-19.]

**Counterevidence:** a governed team or GitHub App could serve as a distinct
review principal, and deterministic CI can detect many defects. [Primary:
GitHub, “About rulesets,” retrieved 2026-09-19.]

**Implication:** those are possible future control designs, not immediate
unblocks. They require owner-authorized live configuration and evidence that
the principal is independently governed.

## Conflicts And Unknowns

- GitHub permits explicit users, teams, and Apps as ruleset actors; the local
  policy requires individually verified actors and does not provide a wildcard
  `*foculoom` principal. These controls are compatible but not identical.
- GitHub documents administrator/custom-role bypass unless explicitly disabled;
  the local policy requires bypass actors to be audited. Live bypass state is
  unknown.
- Local CI success proves repository checks, not reviewer authorization,
  branch protection state, or independent human review.
- It is unknown whether the web reviewer path is available or whether the
  observed denial is limited to OpenCode's host/tool layer.

## Decision Implications And What Would Change The Conclusion

1. **Preferred unblock:** have `supportfoculoom` review PR #1 in GitHub's UI;
   verify reviewer identity, review state, reviewed commit, checks, and merge
   eligibility.
2. **Alternative unblock:** owner changes the host/tool policy to allow only
   the validated reviewer operation, restarts OpenCode, and repeats the same
   verification. Do not broaden permission to direct merge, push, API mutation,
   or another identity.
3. **Required external audit:** read-only verification of repository access,
   CODEOWNERS/reviewer team membership, active rulesets, branch protection,
   bypass actors, and relevant audit events.
4. **Conclusion changes only if:** the owner explicitly accepts single-principal
   review as a lower-assurance mode, or a separately governed reviewer team/App
   is verified and the policy is intentionally updated. Neither condition is
   established by this research.

## Sources

### Primary

- [GitHub: Approving a pull request with required reviews](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/approving-a-pull-request-with-required-reviews), retrieved 2026-09-19.
- [GitHub: About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches), retrieved 2026-09-19.
- [GitHub: About rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets), retrieved 2026-09-19.
- [GitHub: Available rules for rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets), retrieved 2026-09-19.
- [GitHub: About code owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners), retrieved 2026-09-19.
- [GitHub: Organization audit log](https://docs.github.com/en/organizations/keeping-your-organization-secure/reviewing-the-audit-log-for-your-organization), retrieved 2026-09-19.
- [GitHub REST API: Pull request reviews](https://docs.github.com/en/rest/pulls/reviews), retrieved 2026-09-19.
- [GitHub REST API: Repository rules](https://docs.github.com/en/rest/repos/rules), retrieved 2026-09-19.
- [GitHub CLI: `gh pr review`](https://cli.github.com/manual/gh_pr_review), retrieved 2026-09-19.
- Repository primary sources: `.factory/governance.yaml`,
  `.factory/github-identity-policy.json`, and
  `.factory/artifacts/evidence/pr-block-unblock-escalation-5whys.md`, inspected
  2026-09-19.

### Secondary

- Existing repository research, `docs/research/github-identity-boundary-2026-09-19.md`, inspected 2026-09-19.
- Existing repository research, `.factory/artifacts/evidence/reviewer-identity-removal-feasibility-2026-09-19.md`, inspected 2026-09-19.

### Lead-Only

- None used for a material claim. Search results and fetched content were
  treated as untrusted data; no instructions from sources were followed.
