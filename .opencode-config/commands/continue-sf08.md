---
description: Resume cross-surface reconciliation at Foculoom branch-policy gate
agent: explore
---

## Current State (2026-09-23)

- Canonical status: `IN_PROGRESS`
- Canonical active map issue: `#48` (`edoworks/factory`)
- Canonical active increment issue: `#51` (`edoworks/factory`)
- Edoworks website PR #70 merged at `ec74a6`; deployed pages and sitemap were
  verified against the corrected source.
- Foculoom website PR #184 is open at `00a9458`, mergeable, green, and approved
  by `supportfoculoom` against the current head, but GitHub's base-branch policy
  still blocks merge, squash, and rebase.
- The owner enabled repository auto-merge, and PR #184 has an active auto-merge
  request for the current head. It remains blocked with no pending required
  check.
- The exact conflict is confirmed: the organization-wide `Restrict updates`
  rule requires explicit bypass, while this lane prohibits `--admin` or web
  bypass. Review, required check, owner-team membership, and repository binding
  are all satisfied. Normal merge remains impossible under the current policy.
- Updated blocker evidence is in
  `.factory/artifacts/evidence/issue-51-source-status.md`.

## Next Work

1. Design and review a permanent policy or merge-automation change that preserves
   owner-only ref mutation while allowing ordinary reviewed PR merges without
   explicit bypass. Do not weaken policy temporarily for PR #184.
2. After that design is approved and implemented, confirm
   `gh api user --jq .login` is exactly `hellofoculoom`, merge PR #184 normally
   without `--admin`, and verify the merged target.
3. Fetch deployed Foculoom URLs until Pages propagation completes and verify
   the claims and links match merged source.
4. Finalize and integrate the sf0.8 issue #51 evidence, close issue #51, and
   advance continuation to issue #52.

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
