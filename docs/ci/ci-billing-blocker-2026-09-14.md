# CI Billing Blocker — 2026-09-14

Run: `34897768895`
Commit: `2be816f`
Result: job not started; GitHub reported failed recent payments or an exceeded spending limit.

## 5-Whys

1. Why did the post-push verification fail? The `policy` job was marked failed.
2. Why was the job marked failed? GitHub Actions refused to start it.
3. Why did GitHub Actions refuse to start it? The account billing gate reported failed payments or a spending-limit condition.
4. Why did sf0.8 depend on that blocked service? Its workflow still selected hosted `macos-26`, while the available self-hosted runner was registered only to Product A.
5. Why did the workflow and runner scope disagree? The sf0.8 workflow was not migrated when Product A was moved to the free self-hosted CI path. The precise account sub-cause remains unverified: GitHub reported failed payments or a spending-limit condition.

## Correction and guard

- Immediate correction: register a separate sf0.8-scoped runner and migrate the workflow to its `sf08` label; no spending-limit change is required.
- Root-cause correction: keep repository workflows aligned with their explicitly scoped self-hosted runners, rather than depending on hosted macOS capacity.
- Recurrence guard: `scripts/ci-status.sh` records the run conclusion and blocks any green CI claim when the required workflow does not complete successfully.

The exact billing sub-cause remains an explicit assumption pending owner inspection of GitHub Billing & plans; it is no longer on the sf0.8 critical path.
