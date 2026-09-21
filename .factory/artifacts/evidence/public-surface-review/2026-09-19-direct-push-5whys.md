# 5-Whys: Public-Surface Direct-Push Block

Date: 2026-09-19
Scope: `foculoom/foculoom.github.io` public homepage correction
Outcome: direct push blocked by the repository pre-push hook; no bypass used

## Evidence

- Owner identity check returned `hellofoculoom`.
- Commit `1fb9f2c` contains only the canonical Rung-link correction.
- Push to `origin HEAD:master` was rejected with: `direct push to 'master' is prohibited`.
- The same commit was pushed to `feature/public-rung-link` using the configured GitHub credential path.

## Why Chain

1. Why did the push fail? The repository pre-push hook rejects direct pushes to `master`.
2. Why does the hook reject that push? Public website changes must enter through a feature branch and review path.
3. Why is review required? The public homepage is an external publication surface and its changes need an auditable review boundary.
4. Why was a direct push attempted first? The execution step checked owner identity but did not preflight the target repository's branch policy.
5. Root cause reached: the local execution checklist treated owner authorization as sufficient for mutation and omitted repository-specific branch-policy discovery.

## Correction

- Immediate correction: preserve the commit, create `feature/public-rung-link`, and push only that exact branch without bypassing hooks.
- Root-cause correction: perform branch-policy and repository-hook discovery before every external push; use a pull request for protected or review-gated targets.
- Recurrence guard: this record is attached to the public-surface evidence bundle; the successful branch push and subsequent PR state must be verified before publication is claimed.

## Boundary

The live `rung.edoworks.com` HTTP 530 remains unresolved. Merging the branch and deploying the homepage require the repository's approved review and publication path.
