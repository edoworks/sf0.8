# Issue #51 source status

Date: 2026-09-23
Status: `BLOCKED`

## Integration status

- `edoworks/edoworks.github.io` branch `feature/website-state-51`, commit
  `dd583a6`: NowNest lifecycle, privacy, terms, support, portfolio, sitemap,
  manifest, navigation, monitoring, CI guard, and regression tests. PR #70
  merged as `ec74a6`; the deployed pages and sitemap match the corrected source.
- `foculoom/foculoom.github.io` branch `feature/public-state-51`, commit
  `00a9458`: verified Rung destination, explicit commercial status, privacy
  contact scope, complete sitemap, Pages guard, and regression tests. PR #184 is
  open and mergeable, has a successful Pages build check, and was independently
  approved by `supportfoculoom` against the current head.
- The sf0.8 evidence and continuation checkpoint merged in PR #124 at
  `96c3f31` after its policy check and independent rubberduck review passed.

Both branches passed local validators, six regression tests each,
`git diff --check`, independent review, and desktop/mobile rendered review.

## Blocker

GitHub rejects a normal merge of Foculoom PR #184 because the base-branch policy
prohibits it. All visible required checks pass and the independent approval is
recorded. GitHub computes the review decision as `APPROVED` but the merge state
as `BLOCKED`. Normal merge, squash, and rebase paths have all been tested. The
owner enabled repository auto-merge on 2026-09-23, and PR #184 has an active
auto-merge request for the current head, but it remains blocked with no pending
required check.

Owner inspection established the effective policy conflict:

- Repository protection requires the `build` check and disallows bypass; the
  check passes and the head is current.
- GitHub requires an approving reviewer with repository Write access.
  `supportfoculoom` was granted Write access, and GitHub now computes the current
  head's review decision as `APPROVED`.
- The organization ruleset `hellofoculoom-only branch mutations` targets every
  repository and branch and enables `Restrict updates`.
- Its sole bypass actor is the `Owner Ref Writers` team. The team again contains
  only `hellofoculoom`, now has explicit Write access to this repository, and
  retains its original `Always allow` mode.
- After membership, repository binding, review eligibility, checks, and
  auto-merge were all satisfied, GitHub still required an explicit bypass
  operation to update `master`. Both `Always allow` and a bounded test of `For
  pull requests only` produced the same blocked normal-merge result.

The PR cannot merge through the required normal path while `Restrict updates`
is active. `--admin`, a web bypass, and temporary policy weakening remain
prohibited.

Issue #51 remains open pending an approved permanent policy design that supports
owner-only ref mutation and ordinary reviewed PR merging without explicit
bypass, followed by PR #184 merge and deployed-URL verification.

## Blocker analysis

1. The Foculoom source is not deployed because PR #184 cannot merge normally.
2. GitHub reports `Cannot update this protected ref` because the organization
   ruleset restricts updates to bypass actors.
3. The owner is the sole configured bypass actor, but GitHub's normal and
   auto-merge paths do not invoke the explicit bypass required by that rule.
4. Explicit bypass is prohibited because it can skip the review and check
   boundary, even though this PR independently satisfies both.
5. The conflicting policies were not detected before publication because the
   preflight checked identities, permissions, review, and checks separately but
   did not exercise a representative protected normal merge.

The immediate correction is to leave PR #184 queued and the public source
undeployed. The root-cause correction requires a reviewed permanent policy or
merge-automation design, not a one-off bypass. A disposable protected-PR
preflight that proves normal mergeability before a publication increment depends
on it is proposed but not yet implemented or verified.

## Reviewer-team authority incident

1. `supportfoculoom` was briefly added to the owner bypass team during diagnosis.
2. The reviewer needed repository Write access for its approval to count, and
   reviewer eligibility was mistakenly conflated with ref-writer eligibility.
3. The bypass-team settings page was open during diagnosis, and the proposed
   correction was not checked against the reviewer-only authority rule before
   the membership change.
4. No continuation test required that the reviewer remain outside the owner
   bypass team, so the unsafe proposal was not mechanically rejected.
5. Evidence does not establish a deeper cause; further inference stops here.

The immediate correction removed `supportfoculoom`; `Owner Ref Writers` is again
sole-member. The root-cause correction separates repository review access from
owner bypass membership. The mechanical recurrence guard is an explicit
continuation-contract assertion that `supportfoculoom` remains outside `Owner Ref
Writers`; the assertion is covered by `tests.test_continuation_contract`.

## Continuation validation analysis

1. The continuation contract test failed because the refreshed prompt omitted
   required authority and scope-preflight phrases.
2. Those phrases were omitted because the prompt was replaced with a narrow
   blocker snapshot instead of preserving its durable contract section.
3. The replacement was not caught before editing because validation ran only
   after the prompt refresh.
4. Evidence does not establish why the earlier refresh process skipped that
   checkpoint, so deeper causes remain `UNKNOWN`.

The immediate correction restores the canonical `Continuation Contract`
section. The root-cause correction is to preserve that section during status
refreshes and run `tests.test_continuation_contract` at the same checkpoint.
That test is the mechanical recurrence guard and now passes against the global
prompt.
