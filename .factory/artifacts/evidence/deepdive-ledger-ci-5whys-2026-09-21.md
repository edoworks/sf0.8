# Deep-Dive Ledger CI Failure 5-Whys

Date: 2026-09-21

Failure: PR policy CI blocked `.agents/skills/evidence-research/SKILL.md` as an
unclaimed gated changed path.

1. **Why did CI fail?** The changed reusable skill had no changed issue ledger
   claiming its path.
2. **Why was no ledger included?** Issue #88 was opened after implementation,
   but the implementation was committed before its capability binding and
   ledger were created.
3. **Why did local focused tests not catch it?** They tested command behavior,
   not the repository's complete pull-request changed-path policy.
4. **Why did the workflow reach CI first?** The local preflight omitted
   `validate-ci-change.py` against the actual PR base/head range.
5. **Root cause supported by evidence:** issue-first control-plane binding was
   performed late, and verification did not include the repository's canonical
   changed-path gate before push.

Immediate correction: bind `subject-locked evidence research` to issue #88 and
add a ledger record claiming the skill path with reuse evidence.

Root-cause correction: for future reusable-skill edits, create/reuse the issue,
binding, and ledger before commit, then run the complete changed-path validator
against the intended branch range.

Mechanical recurrence guard: the existing CI validator remains fail-closed; the
same command is run locally before the corrected branch is pushed.
