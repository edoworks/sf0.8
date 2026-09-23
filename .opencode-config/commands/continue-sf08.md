---
description: Resume repository metadata and release-claim reconciliation
agent: explore
---

## Current State (2026-09-23)

- Canonical status: `IN_PROGRESS`
- Canonical active map issue: `#48` (`edoworks/factory`)
- Canonical active increment issue: `#52` (`edoworks/factory`)
- Edoworks website PR #70 merged at `ec74a6`; deployed pages and sitemap were
  verified against the corrected source.
- Foculoom website PR #184 merged normally at `f4e0bc9`; post-merge Pages build
  and deployment passed, and live home, policy, sitemap, and Rung destination
  checks match source.
- The permanent branch-policy replacement preserves owner-only mutations without
  requiring explicit merge bypass. `Owner Ref Writers` remains sole-member;
  `supportfoculoom` retains review access but is not a bypass actor.
- Issue #51 completion evidence is in
  `.factory/artifacts/evidence/issue-51-source-status.md`.
- Issue #51 is closed and its closeout guard reported `CLOSED`.

## Next Work

1. Load issue #52, canonical inventory, and current authenticated repository and
   release metadata snapshots.
2. Correct active homepage, lifecycle, license, and release claims without
   unarchiving deprecated repositories or publishing new releases.
3. Verify the metadata snapshot and documented release URLs/assets.
4. Then run issue #53 final cross-surface state review and closeout.

## Authority Boundaries

- Preserve the recorded `supportfoculoom` approval; any head rewrite requires a
  fresh independent review.
- Keep `supportfoculoom` outside `Owner Ref Writers`; reviewer access must not
  grant owner ref-mutation authority.
- Before every owner GitHub write, require
  `gh api user --jq .login == hellofoculoom`.
- Reviewer identities may review or comment only and must be asserted before
  those actions.
- Issue mutations are prohibited in `--auto` mode.
- Never use `--admin`, an API workaround, force-push, or overwrite unrelated
  dirty work.
- Private predecessor completeness remains `UNKNOWN`; issue #16 remains
  effectively blocked.

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
