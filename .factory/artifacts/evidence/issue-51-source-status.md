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

Both branches passed local validators, six regression tests each,
`git diff --check`, independent review, and desktop/mobile rendered review.

## Blocker

GitHub rejects a normal merge of Foculoom PR #184 because the base-branch policy
prohibits it. All visible required checks pass and the independent approval is
recorded, but GitHub still reports an empty computed review decision and a
`BLOCKED` merge state. Normal merge, squash, rebase, and auto-merge paths have
all been tested; auto-merge is disabled. The exact live rule is not exposed by
the permitted read interfaces. The head commit is unsigned, but whether commit
signing is the blocking rule remains an unconfirmed hypothesis. Using `--admin`,
changing repository rules, or rewriting the approved head without explicit
authorization would bypass or invalidate the current review boundary.

Issue #51 remains open until the exact base-branch requirement is identified and
satisfied without bypass, PR #184 merges normally, and the deployed URLs are
fetched and matched to the corrected source.

## Blocker analysis

1. The Foculoom source is not deployed because PR #184 cannot merge normally.
2. GitHub reports that the base-branch policy prohibits the merge.
3. The PR is mergeable, its visible required build check passes, and an eligible
   organization member approved the current head, but GitHub still computes the
   merge state as `BLOCKED`.
4. The permitted PR interfaces expose the outcome but not the exact live branch
   rule; authenticated protection and ruleset API reads are outside the current
   tool policy.
5. Without the exact rule, changing policy, rewriting the approved head, or
   using administrator bypass would substitute speculation for the repository's
   trust-boundary control.

The independent-review correction is complete. The immediate next correction is
an owner inspection of the live `master` branch rule, followed by satisfying the
identified requirement without `--admin`. The recurrence guard is to preflight
and record effective branch requirements before opening future publication PRs.
The exact blocking rule remains `UNKNOWN`; unsigned-commit enforcement is only
a hypothesis supported by the local commit lacking a signature.

## Continuation validation analysis

1. The continuation contract test failed because the refreshed prompt omitted
   required authority and scope-preflight phrases.
2. The prompt had been reduced to the active website blocker and no longer
   carried the repository's durable continuation safeguards.
3. The prompt was updated before its contract test was run.
4. The immediate and root-cause correction is to retain the canonical
   `Continuation Contract` section during status refreshes.
5. The mechanical recurrence guard is
   `tests.test_continuation_contract`, which now verifies the global prompt
   after every refresh.
