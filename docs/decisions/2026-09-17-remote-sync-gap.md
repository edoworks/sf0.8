# Remote Synchronization Gap

## Evidence

After the local completion pass, `sf0.8` was one commit ahead of
`origin/main`, and `product-a` was sixteen commits ahead. Both worktrees were
otherwise clean. Running `scripts/ci-status.sh` also updated the tracked CI
evidence timestamp after validation.

## 5-Whys

1. Why were commits not synchronized with the remote? The commits were created
   locally but no push was performed.
2. Why was no push performed? The workflow treated local commit plus clean
   worktree as completion, while remote writes are separately authorized.
3. Why did that omission survive completion? Completion checked cleanliness but
   did not compare `HEAD` with `origin/main`.
4. Why was the comparison absent? The clean-worktree invariant was defined
   without a remote-state invariant, and CI-status collection could mutate
   tracked evidence after the final check.
5. Evidence limit: no deeper cause is established beyond this workflow gap and
   the explicit external-write boundary.

## Correction and Guard

- Immediate correction: push the reviewed commits using the owner-bound GitHub
  credentials and verify exact equality with `origin/main`.
- Root-cause correction: completion now requires a clean worktree and exact
  local/remote equality, documented in `CONTRIBUTING.md`.
- Mechanical guard: `scripts/check-repo-sync.sh` fails on dirty state, missing
  remote tracking, or unequal local and remote heads. It accepts a repository
  path so the active factory can check both itself and `product-a`.
- Evidence guard: tracked CI-status evidence must be committed before the final
  synchronization check.

The guard does not block ordinary local commits or require a push during
unrelated development. It is a completion gate after the authorized push.
