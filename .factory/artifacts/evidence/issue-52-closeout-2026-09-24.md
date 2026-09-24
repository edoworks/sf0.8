# Issue 52 Closeout Evidence

- Captured: `2026-09-24T06:33:27Z`
- Working root: clean detached worktree created from `origin/main@2d148d6`
- Source of truth: `/Users/hello/sf0.8` (left dirty and unmodified)
- Owner identity: `hellofoculoom`, asserted separately before every write

## Integrated Effects

- `edoworks/rung` homepage is `https://edoworks.com/rung/`.
- `edoworks/asc-client` description uses the canonical deprecated wording.
- `edoworks/factory-constitution` description uses the canonical deprecated wording.
- `edoworks/asc-client` PR 1 merged reviewed head `c49e8a2` as `b1127bc`.
- `edoworks/factory-constitution` PR 1 merged reviewed head `1412836` as `a21a523`.
- Both feature refs are absent after normal ancestry-preserving merges.

## Verification

- Independent final diff review found no findings and `git diff --check` passed
  for both source PRs.
- Both repositories define no CI checks; review covered exact heads, lifecycle
  wording, historical MIT license text, release links, and tagged content.
- `python3 scripts/public-surface-preflight.py --github-contract
  .factory/repository-metadata-target.json` passed all six repositories and all
  four release records without `--allow-declared-blockers`.
- Private predecessor completeness remains `UNKNOWN`; this was outside issue 52.

## Continuation Projection Failure

1. The first closeout validation failed because canonical continuation advanced
   to issue 53 while the checked-in continuation prompt still named issue 52.
2. The closeout edit updated the machine-readable state and evidence but treated
   the human-readable prompt as a later issue-53 concern.
3. Both files are projections of the same active-increment fact and must change
   atomically.

Root cause: the initial closeout patch split one canonical state transition
across verification phases. Immediate correction: update the checked-in prompt
in the same branch. Root-cause correction and recurrence guard: retain the
existing evidence-integrity comparison, which detected the mismatch before
commit; rerun it after every continuation-state change.

## Complete-Contract CI Failure

1. PR 143's policy job returned exit 1 after all ten live contract checks passed.
2. CI always invokes the contract with `--allow-declared-blockers` so an exact
   declared blocker set can keep an `IN_PROGRESS` contract verifiable.
3. That mode returned success only when `completion_status` was `IN_PROGRESS`.
4. No regression test exercised the transition from a matching in-progress
   blocker set to a blocker-free complete contract under the CI command shape.

Root cause: declared-blocker mode encoded only the intermediate state, while CI
used it for the contract's full lifecycle. Immediate correction: complete mode
now succeeds only when declared and actual blockers are both empty and all
non-repository checks pass. Root-cause correction: regression tests execute the
CI command path for both blocker-free success and live-drift rejection.

## Changed-Path Binding Failure

1. The second PR 143 run passed the authenticated contract but the ecosystem
   gate rejected three ledger paths that were unchanged in the PR range.
2. The ledger retained gated paths from issue 52's earlier merged implementation
   and added the regression-test path.
3. The gate binds a ledger to the current PR's gated diff, not cumulative issue
   history; the test path is not gated and the earlier paths are already merged.

Root cause: the follow-up edit treated `changed_paths` as cumulative issue
history instead of an exact current-range capability binding. Immediate
correction: bind only `scripts/public-surface-preflight.py`. Root-cause
correction and recurrence guard: run `validate-ci-change.py` with the PR base and
head range before pushing any follow-up that changes a capability ledger.
