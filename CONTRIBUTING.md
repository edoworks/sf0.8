# Contributing

Factory v0.1 is currently private. Contributions open with publication.

Use small, revertible changes on a dedicated `feature/*` branch. Every change
runs `python3 -m unittest discover -s tests -p 'test_*.py'` and any applicable
validators listed in `.github/workflows/checks.yml`; sign-off uses DCO
(`Signed-off-by:` trailers) rather than a CLA.

Routine local staging and ordinary commits do not require interactive approval.
Before committing, review the staged paths, run the applicable verification, and
include the issue reference. Protected-branch pushes, tags, releases, deletion,
visibility changes, and history-rewriting or bypass operations remain gated.

Before opening the pull request, rubberduck the final diff: explain the problem,
the change, its strongest failure mode, and why the verification detects that
failure. Record that review in the pull-request body. Then push the feature
branch, open the pull request, confirm its checks, and merge it. These ordinary
owner-authorized integration steps do not need a new interactive approval;
identity verification and repository protections still apply.

Implementation is complete only after the pull request containing the final
reviewed commit set is merged and the merge is verified on `origin/main`. A
local commit, passing tests, an open pull request, or a blocked integration step
is progress, not completion. After merge, run `./scripts/check-repo-sync.sh`
from this repository and from `product-a/`:

```bash
./scripts/check-repo-sync.sh
./scripts/check-repo-sync.sh product-a
```

Both commands must report a clean worktree whose `HEAD` exactly matches
`origin/main`. If CI-status collection modifies tracked evidence, commit that
evidence through the same branch and pull-request workflow before running the
final synchronization check.

The active agent contract is `AGENTS.md` in each product repo; the governing constitution is `sf0.8/NORTH_STAR.md` + `.factory/governance.yaml`.
