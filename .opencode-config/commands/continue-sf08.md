---
description: Resume cross-surface reconciliation at Foculoom review gate
agent: explore
---

## Current State (2026-09-23)

- Status: `IN_PROGRESS`
- Active map: `edoworks/factory#48`
- Active increment: `edoworks/factory#51`
- Edoworks website PR #70 merged at `ec74a6`; deployed pages and sitemap were
  verified against the corrected source.
- Foculoom website PR #184 is open at `00a9458`, mergeable, and green, but
  GitHub's base-branch policy blocks a normal merge.
- `supportfoculoom` has been requested as the independent reviewer. No review is
  recorded yet.
- Updated blocker evidence is in
  `.factory/artifacts/evidence/issue-51-source-status.md`.

## Next Work

1. Obtain an approval of Foculoom PR #184 from the requested independent
   reviewer. The safe paths are a human web review or a restarted session whose
   tool policy explicitly permits `gh pr review` for this repository.
2. Confirm `gh api user --jq .login` is exactly `hellofoculoom`, merge PR #184
   normally without `--admin`, and verify the merged target.
3. Fetch deployed Foculoom URLs until Pages propagation completes and verify
   the claims and links match merged source.
4. Finalize and integrate the sf0.8 issue #51 evidence, close issue #51, and
   advance continuation to issue #52.

## Authority Boundaries

- Do not submit the review as `hellofoculoom`; owner self-approval is not an
  independent review.
- Before every owner GitHub write, require
  `gh api user --jq .login == hellofoculoom`.
- Reviewer identities may review or comment only and must be asserted before
  those actions.
- Never use `--admin`, an API workaround, force-push, or overwrite unrelated
  dirty work.
- Private predecessor completeness remains `UNKNOWN`; issue #16 remains
  effectively blocked.
