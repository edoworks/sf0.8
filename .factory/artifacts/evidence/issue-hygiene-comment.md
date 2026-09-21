# Issue Hygiene Audit

The active audio chain (#73–#79) was audited against the live issue inventory.

- Classification for all: `enhancement`.
- Intended priorities: #73 P1, #74 P1 complete, #75 P1, #76 P2, #77 P1, #78 P2,
  #79 P2.
- Duplicate review: #73 is the map; #74–#79 are distinct child outcomes; #80
  is adjacent handoff infrastructure, not a duplicate.
- Reprioritization review: #75 remains the active dependency; Product A remains
  shelved; #77 may proceed in parallel only against the shared core.

The detailed record is `.factory/artifacts/evidence/issue-hygiene-active-chain-triage-2026-09-20.md`.

The new issue-intent guard enforces this metadata for future issue creation.
The existing issues predate the guard and have empty remote label sets; applying
remote labels requires the separate owner-authorized GitHub label mutation and
is not claimed here.
