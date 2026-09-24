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

## 2026-09-24 Offline Runner Recurrence

Storage-governance PR 146 remained queued with zero steps because the scoped
runner was configured but offline. The runner had been started manually and was
not installed as a launchd service. Its diagnostics establish that it used
manual startup and stopped producing activity at 08:04Z; they do not establish
why that process exited.

1. Integration stalled because the required policy job never started.
2. The job remained queued because no online runner matched
   `[self-hosted, macOS, ARM64, sf08]`.
3. The configured runner was offline because no `Runner.Listener` process was
   active.
4. It was not restarted because the runner was not installed as a service and
   depended on a manually launched process.
5. The outage consumed repeated watch intervals because completion procedure
   checked terminal CI state but had no runner-readiness preflight for a
   zero-step queued job.

Immediate correction: install and start the existing repository-scoped runner
as a launchd service. Root-cause correction: `scripts/ci-status.sh` invokes
`scripts/runner-readiness.sh` before waiting on a queued sf0.8 run. The guard
fails promptly when the service command, launchd state, or listener process is
absent. Automated tests cover each state. The runner remains limited to the
private, same-repository trust boundary; public or fork-originated workflows
must not execute on this host.

The first local readiness invocation found a test-double gap: the vendor
`svc.sh` resolves its template relative to the current directory even for
`status`, while the guard initially invoked it by absolute path from the source
repository. The immediate cause was the wrong working directory; the
contributing cause was a fake service command that did not enforce the vendor
script's directory contract. The guard now executes `svc.sh` from the runner
root, and the positive test fails unless that working directory is used.

The first updated PR run then failed the changed-path ecosystem gate because the
two new scripts were not claimed by a current capability ledger. The issue
existed, but its binding and ledger had not been added before push; local unit
tests validate record semantics, not the complete GitHub pull-request range.
The policy therefore failed correctly. The correction binds issue 147 to the
self-hosted runner readiness capability and claims exactly the two gated paths
in `.factory/artifacts/ledger/issue-147.json`. The complete PR-range CI check is
the recurrence guard; local green tests cannot replace it.
