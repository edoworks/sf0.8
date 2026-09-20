# Reuse Control Incident 5-Whys

Observed chain: substantial work completed -> GitHub mutation blocked -> local implementation successful -> issue state unresolved -> completion was still presented.

1. Why was completion presented? The session treated local verification as the completion boundary.
2. Why could issue reconciliation not run? The loaded OpenCode bash policy had no scoped allow rule for the required GitHub operation.
3. Why did adding the rule not immediately enable the write? OpenCode loads permission configuration at startup and the current session retained the old policy.
4. Why was a restart repeatedly needed? The policy was expanded reactively, one missing operation at a time, with no complete issue-lifecycle contract or startup validation.
5. Why was there no complete contract? The factory modeled issue reconciliation as a completion concern instead of a mandatory control-plane capability with create, comment, and close operations declared before work began.

Immediate correction: record issue 49 as `CONTROL_PLANE_BLOCKED` and `done: false`.
Root-cause correction: `opencode.jsonc` now declares the complete scoped issue lifecycle (`gh issue create`, `gh issue comment`, and `gh issue close`) before a session starts; the portable fixture mirrors that contract; `scripts/complete-work.py` refuses DONE unless required issue reconciliation is true; the idempotency key and resume action preserve deterministic reconciliation.
Recurrence guard: the permission fixture must cover every mandatory issue operation, and the control-plane tests must keep denied-write behavior separate from authenticated/read access. A restart is required only once after this policy correction; future issue work does not require reactive permission edits.

## 2026-09-19 Recurrence

This correction was incomplete: it encoded issue 50 rather than a durable
repository-scoped lifecycle policy. The superseding analysis is
`control-plane/issue-lifecycle-permission-recurrence-5whys.md`.
