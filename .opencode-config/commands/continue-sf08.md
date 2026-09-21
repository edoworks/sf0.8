---
description: Resume NowNest release qualification and sf0.8 evidence work
agent: explore
---

## Current State (2026-09-21)

**NowNest** is Reference App 1. The old FocusGate identity is deprecated.

- Repository: `edoworks/nownest`; local checkout: `/Users/hello/FocusGate`
- Branch/revision: `main` at `7f8ec23`, clean and pushed
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
- Automated G8 coverage is complete. Do not mark G8 passed until human visual
  review and TestFlight-build validation are recorded.
- Evidence: `/Users/hello/sf0.8/.factory/artifacts/evidence/nownest-device-automation-blocker-2026-09-21.md`
  and `nownest-validation-summary-2026-09-21.json`.

## Remaining Gates

1. Human visual review on physical iPhone and iPad.
2. Validate the installed TestFlight build on both devices.
3. Record G8 only after those checks pass.
4. Run G9 recovery: deliberate break/restore and delete/reinstall behavior.
5. Prepare App Store metadata. Do not submit without explicit human authority.
6. G10 App Store submission and G11 Apple acceptance remain human/Apple gated.

## Immediate Next Steps

1. Start Chunk A (factory #29): prototype visual system infrastructure.
2. Ask the owner to perform/confirm human visual and TestFlight checks for G8.
3. After G8 evidence is complete, run G9 recovery and prepare metadata.

## Repository State

- `/Users/hello/FocusGate`: clean `main` at `7f8ec23` (PRD merged via PR #1).
- `/Users/hello/sf0.8`: `main` at `2e6ea16` (skills merged, permission rename
  merged). Clean working tree except unrelated untracked factory artifacts.
- `/Users/hello/factory`: `main` at `0070c742`; issues #28-#33 track the
  redesign; #10 tracks the full release ladder.
- `/Users/hello/sf0.8/product-a`: pre-existing dirty checkout; do not modify.
- Stash `stash@{0}` on `feature/control-plane-checkpoint` remains parked.

## Governance Boundaries

- Owner write gate: `gh api user --jq .login == hellofoculoom`
- Permission policy: `~/.config/opencode/opencode.jsonc`
- Portable fixture: `tests/permission_policy_fixture.json`
- No App Store submission, publication, archive, or visibility change without
  explicit human authorization
- Issue mutations are interactive `ask` operations; prohibited in `--auto` mode
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
2. Confirm `/Users/hello/FocusGate` is on `main` with the PRD merged.
3. Read `docs/calm-expressive-ux-prd.md` in `/Users/hello/FocusGate` for the
   full implementation handoff.
4. Check factory issues #28-#33 for current chunk status.
5. Ask the owner to perform/confirm the human visual and TestFlight checks; do
   not repeat already-passing automation unless the source or environment changed.
6. After G8 evidence is complete, run G9 recovery and prepare metadata without
   submitting to App Review.