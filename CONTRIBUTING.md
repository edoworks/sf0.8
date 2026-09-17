# Contributing

Factory v0.1 is currently private. Contributions open with publication.

When we open: small, revertible PRs; every change runs `./scripts/verify.sh` (or `scripts/check_policy.sh` for docs-only); sign-off via DCO (`Signed-off-by:` trailers) rather than a CLA.

Routine local staging and ordinary commits do not require interactive approval.
Before committing, review the staged paths, run the applicable verification, and
include the issue reference. Protected-branch pushes, tags, releases, deletion,
visibility changes, and history-rewriting or bypass operations remain gated.

Completion requires more than a local commit. After the approved push, run
`./scripts/check-repo-sync.sh` from this repository and from `product-a/`:

```bash
./scripts/check-repo-sync.sh
./scripts/check-repo-sync.sh product-a
```

Both commands must report a clean worktree whose `HEAD` exactly matches
`origin/main`. If CI-status collection modifies tracked evidence, commit that
evidence before running the final synchronization check.

The active agent contract is `AGENTS.md` in each product repo; the governing constitution is `sf0.8/NORTH_STAR.md` + `.factory/governance.yaml`.
