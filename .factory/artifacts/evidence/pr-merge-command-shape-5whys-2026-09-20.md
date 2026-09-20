# Organization-Wide PR Merge Permission 5-Whys

## Observation

An owner-authorized, reviewed, mergeable PR with passing checks repeatedly
required owner follow-up because the merge command was denied before reaching
GitHub.

## 5-Whys

1. The owner became a progress bottleneck because agents stopped after routine
   merge denials and requested another confirmation or restart.
2. The denials occurred because repository-first production commands matched
   the broad `gh pr *` deny instead of the number-first scoped allow.
3. The command forms diverged because `gh` accepts both orders while OpenCode
   permission globs compare literal command strings.
4. Tests did not detect the divergence because they covered two repositories
   and only the number-first happy path.
5. The same defect recurred after PR creation because its exact-command lesson
   was repaired locally rather than promoted to an organization-wide merge
   invariant.

## Root Cause And Corrections

- Root cause: policy intent, permission globs, tests, and emitted commands did
  not share one production-command matrix.
- Immediate correction: use the tested number-first merge form already admitted
  by the active policy.
- Root-cause correction: allow and test both valid merge argument orders for
  `edoworks/*` and `foculoom/*`.
- Mechanical guard: matrix tests cover both organizations, both orders,
  `--delete-branch`, foreign and lookalike organizations, and explicit denial of
  `--admin`.
- Operating correction: eligible ordinary merges proceed without requesting a
  fresh owner confirmation. After any denial, inspect the logged winning rule
  before attributing the result to session state.

## Safety Boundary

The correction does not authorize admin bypass, failed-check overrides,
protected-branch pushes, force pushes, releases, tags, publication, settings,
visibility changes, repository deletion, or foreign-organization mutations.
GitHub rulesets and required reviews remain authoritative.
