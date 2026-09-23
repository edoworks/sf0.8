---
description: Resume NowNest evidence-integrity and release qualification work
agent: explore
---

## Current State (2026-09-22)

NowNest is Reference App 1 (`edoworks/nownest`, local checkout
`/Users/hello/FocusGate`). `edoworks/factory` is the designated successor to
sf0.8, but cutover is not ready.

- Factory PRD evidence-integrity contracts merged in sf0.8 PR #117 at
  `f722b62`.
- NowNest qualification-contract amendments merged in NowNest PR #24 at
  `a055cfc`.
- Factory map #42 owns the NowNest correction program. Child #43 is complete;
  #44-#47 remain open. Cross-surface reconciliation is tracked by map #48.
- Canonical status: `IN_PROGRESS`
- Canonical active map issue: `#48`
- Canonical active increment issue: `#51`
- Existing gate issues remain #10 (Apple acceptance), #11 (30-day
  qualification), #15 (predecessor freeze), and #28/#32 (UX map and owner-only
  treatment selection).
- Qualification ledger remains entry 1/10 and still requires a 30-calendar-day
  observation window, ten consecutive weekday changes, >=95% unattended
  success, and a second operator.

## Material Findings

- Quiet Mode currently permits decorative transition motion that its PRD now
  forbids; the existing UI test does not directly assert Sophie/motion absence.
- The required six-journey x three-variant x two-device matrix is incomplete.
- Prior accessibility evidence includes unsupported PASS claims and must be
  superseded by mode-specific receipts.
- `scripts/activate-testflight.py` can exit successfully without proving beta
  state or group membership and claims tester notification it does not perform.
- Build 3 has no durable tester-feedback record. Record
  `NO_DURABLE_FEEDBACK` unless authenticated sanitized evidence is recovered.
- The App Store Connect encryption screenshot is platform feedback, not tester
  feedback. The local `ITSAppUsesNonExemptEncryption=false` edit in the dirty
  `/Users/hello/FocusGate` main checkout has not been committed or uploaded and
  cannot change build 3.
- Prior long UI runs were described as `COMMAND_TIMEOUT_PROGRESSING`, but no
  compliant durable timeout receipt exists; retain the classification as
  `UNKNOWN` until receipt evidence is recovered.

## Next Work

1. Integrate the prepared Edoworks and Foculoom website branches for issue #51 once PR creation is permitted.
2. Verify the deployed URLs, then close issue #51.
3. Then issue #52: reconcile repository metadata and release claims.
4. Then issue #53: run the final cross-surface rubberduck and closeout.
5. Independently resume issue #44: repair Quiet Mode and complete the 36-cell
   UI matrix.
6. Then issue #45: requalify accessibility with direct evidence.
7. Then issue #46: harden TestFlight activation and implement the typed Apple
   lifecycle/feedback receipt.
8. Do not create or upload a replacement build until #44-#46 prerequisites pass
   and explicit owner authorization is recorded.

## Authority Boundaries

- No credential use, archive, upload, App Review submission, release,
  publication, repository visibility change, or destructive action without
  explicit human authorization.
- Before every owner GitHub write, require
  `gh api user --jq .login == hellofoculoom`.
- Issue mutations are prohibited in `--auto` mode.
- Do not freeze or archive sf0.8 until all cutover contracts pass and issues
  #10, #11, #15, and #16 are verified closed.

## Restart Sequence

1. Read factory map #42 and child #47.
2. Check `git status --short --branch` in `/Users/hello/sf0.8`,
   `/Users/hello/FocusGate`, and `/Users/hello/factory`; preserve existing dirty
   work and use isolated worktrees.
3. Read `docs/PRD-edoworks-factory.md` Evidence Contracts And Cutover Guards.
4. Read NowNest `docs/calm-expressive-ux-prd.md` sections 9-11 and 14.
5. Treat external feedback and release state as build-bound evidence; do not
   infer later states or positive feedback from absence.

## Continuation Contract

- Do not stop merely because one requested step is blocked.
- Continue with independent, authorized local implementation.
- Before ending a turn, check for the next eligible lane.
- Preserve human-authority boundaries for security, privacy, destructive
  actions, external-publication/release, and budget decisions.
- Before using external checkouts, run a read-only scope preflight with
  `git worktree list --porcelain`; record `working_root` and `source_of_truth`
  and identify detached or prunable worktrees. Do not silently discard; do not
  clean, prune, or ignore a dirty or stale path.
