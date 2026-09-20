# Complete-Event Changed-Path Validation 5-Whys

Date: 2026-09-19

## Defect

The changed-path CI gate compared only `HEAD^..HEAD`. A pull request with more
than one commit could therefore omit substantial paths changed before the last
commit and pass without a capability-bound issue ledger for those paths.

## Analysis

1. Why could an earlier pull-request change escape validation? CI supplied only
   the paths from the last commit.
2. Why did CI use the last commit? The workflow invoked `git diff --name-only
   HEAD^ HEAD` without using the GitHub event's base, head, or before objects.
3. Why did the existing recurrence test not detect this? It asserted that the
   dynamic ledger flag was present and the fixed historical ledger was absent,
   but did not test the revision range.
4. Why was the path-selection layer not independently testable? Range selection
   lived in workflow shell rather than a deterministic fail-closed validator.
5. Evidence ends here. The records do not establish why the original fix was
   scoped to one commit.

## Correction

- Immediate correction: select pull-request paths from `base...head` and push
  paths from `before..head`, with full history available to CI.
- Root-cause correction: move event range validation and NUL-delimited path
  extraction into `scripts/validate-ci-change.py` and reject missing, null, or
  unsupported event metadata.
- Mechanical recurrence guard: focused tests prove that an earlier-commit path
  is included, push ranges use before/after identities, bad metadata fails
  closed, Git failures fail closed, and the workflow cannot regress to
  `HEAD^ HEAD`.

## Initial Verification Failures

The first focused test run exposed two integration defects: the dynamic test
loader could not resolve the sibling `ecosystem_gates` module, and the prior CI
contract test still required the superseded `--changed-ledgers` command. The
loader now adds the repository scripts directory explicitly, while the contract
test asserts the new validator, full-history checkout, and absence of the
single-commit range. The repeated focused run passed 50 tests.
