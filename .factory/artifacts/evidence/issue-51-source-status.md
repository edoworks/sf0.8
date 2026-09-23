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
  open, mergeable, and has a successful Pages build check.

Both branches passed local validators, six regression tests each,
`git diff --check`, independent review, and desktop/mobile rendered review.

## Blocker

GitHub rejects a normal merge of Foculoom PR #184 because the base-branch policy
prohibits it. All visible checks pass and no review is recorded, so
`supportfoculoom` was requested as the independent reviewer. The current tool
policy does not permit `gh pr review` for this repository; using the owner
identity, API transport, or `--admin` would bypass the review boundary.

Issue #51 remains open until an eligible reviewer approves the current
`00a9458` head, PR #184 merges normally, and the deployed URLs are fetched and
matched to the corrected source.

## Blocker analysis

1. The Foculoom source is not deployed because PR #184 cannot merge normally.
2. GitHub reports that the base-branch policy prohibits the merge.
3. The PR is mergeable and its visible build check passes, but it has no review.
4. Repository governance requires an independently identified reviewer when a
   live branch rule requires approval; owner self-approval is not a substitute.
5. This session permits repository-scoped PR creation, viewing, checks, edits,
   and normal merges, but not review submission under the reviewer identity.

The immediate correction is the pending `supportfoculoom` review request. The
root-cause correction and recurrence guard are already recorded in
`pr-block-unblock-escalation-5whys.md`: explicitly allow and test the exact
review command for the validated reviewer identity, or retain a human web-review
handoff. The exact live rule remains unknown because permitted read interfaces
do not expose it; the missing review is therefore a supported hypothesis, not a
claimed fact.
