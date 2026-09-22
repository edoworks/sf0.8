---
description: Resume NowNest release qualification and sf0.8 evidence work
agent: explore
---

## Current State (2026-09-22)

**NowNest** is Reference App 1. The old FocusGate identity is deprecated.

- Repository: `edoworks/nownest`; local checkout: `/Users/hello/FocusGate`
- Branch/revision: `main` at `5895c37`, clean and pushed
- Bundle ID: `com.foculoom.nownest`; Team ID: `H8MJMBTFVP`
- Universal iPhone/iPad app, Swift 6, local SwiftData, no network/accounts/
  analytics/notifications/background work
- Factory release ladder G1-G7 passed; Apple processed the uploaded TestFlight
  build as `VALID` (delivery UUID `ede273f5-a56b-4513-aa21-389b012066e8`)

## Calm Expressive UX Redesign

The durable PRD is merged to `edoworks/nownest` `main` (commit `7f8ec23`,
PR #1). It lives at `docs/calm-expressive-ux-prd.md` and is available to a
fresh `git clone`. The permission config allows `edoworks/nownest` PR
operations (merged in sf0.8 PR #98).

Factory tracking issues in `edoworks/factory`:

- #28: redesign map (parent)
- #29: Chunk A — prototype visual system
- #30: Chunk B — Home, Capture, success, and Quiet Mode treatments
- #33: Chunk C — Review and accessibility qualification (no archive)
- #32: Chunk D — human comparison and treatment selection (owner-only)
- #31: superseded and closed

Two reusable skills created and merged in sf0.8 PR #99:

- `neuroinclusive-ux`: cognitive-accessibility hypotheses, comparison
  protocols, accessibility checklists, and participant/consent rules.
- `product-art-direction`: visual-language briefs, semantic token rules,
  mascot contracts, and anti-generic design reviews.

## Current Validation

- Current revision passed 6 UI and 6 unit tests on iPhone 17 Pro simulator,
  iPad Pro 11-inch simulator, physical iPhone 16 Pro Max, and physical iPad Air.
- G8 human visual review and TestFlight validation passed for revision
  `8d6f3b5`; evidence is `/Users/hello/sf0.8/.factory/artifacts/evidence/nownest-g8-visual-testflight-2026-09-21.json`.
- G9 recovery remains authorization-gated.

## Remaining Gates

1. Run G9 recovery only after explicit authorization for destructive simulator
   behavior.
2. Review the integrated App Store metadata draft without submitting to App Review.
3. Chunk D human comparison and physical accessibility checks remain owner-gated.
4. G10 App Store submission and G11 Apple acceptance remain human/Apple gated.

## Immediate Next Steps

1. Preserve the G8 evidence and do not upload a new build without explicit authority.
2. Use the issue closeout guard for every tracked chunk before reporting completion.
3. Continue only in the next authorized G9, metadata, or Chunk D lane.

## Repository State

- `/Users/hello/FocusGate`: clean `main` at `5895c37` with metadata draft evidence.
- `/Users/hello/sf0.8`: `main` at `96c11a1` with the closeout guard and skill
  update merged; unrelated pre-existing factory artifacts remain dirty.
- `/Users/hello/factory`: `main` at `fa90f1f` with the queue audit and closeout
  5-Whys merged; existing issue cleanup remains maintainer-reviewed.
- `/Users/hello/sf0.8/product-a`: pre-existing dirty checkout; do not modify.
- Stash `stash@{0}` on `feature/control-plane-checkpoint` remains parked.

## Governance Boundaries

- Owner write gate: `gh api user --jq .login == hellofoculoom`
- Permission policy: `~/.config/opencode/opencode.jsonc`
- Portable fixture: `tests/permission_policy_fixture.json`
- No App Store submission, publication, archive, or visibility change without
  explicit human authorization
- Issue mutations are interactive `ask` operations; prohibited in `--auto` mode
- Issue closeout guard: `node ~/.config/opencode/scripts/issue-closeout.mjs
  verify --repo REPO --issues NUMBER[,NUMBER...]`; require `CLOSED`.
- Trivial tasks must use `explore` (local granite), not `general` (OpenAI Luna)

## Continuation Contract

- Do not stop merely because one requested step is blocked. Continue with independent, authorized local implementation.
- Before ending a turn, check for the next eligible lane.
- Preserve human-authority boundaries for security, privacy, destructive actions,
  external-publication/release, and budget decisions.
- Run a read-only scope preflight before using external checkouts:
  `git worktree list --porcelain`; record `working_root` and `source_of_truth`;
  identify detached or prunable worktrees. Do not silently discard, clean, prune, or
  ignore a dirty or stale path.

## Restart Sequence

1. Check `git status --short --branch` in `/Users/hello/FocusGate`,
   `/Users/hello/sf0.8`, and `/Users/hello/factory`.
2. Confirm `/Users/hello/FocusGate` is on `main` at `5895c37` or later.
3. Read `docs/calm-expressive-ux-prd.md` in `/Users/hello/FocusGate` for the
   full implementation handoff.
4. Check factory issues #28-#36 and #10-#18; completed candidates require
   maintainer review, not inferred closure.
5. Run the closeout guard for every new tracked chunk before declaring it done.
6. G9, Chunk D, and G10/G11 remain human-gated.
