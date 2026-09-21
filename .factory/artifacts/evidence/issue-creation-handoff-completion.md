# Completion evidence

Implemented the planner-to-writer issue handoff guard.

- The global `issue-tracking` skill now requires a complete planner-owned body,
  JSON intent, SHA-256 digest, pre-write validation, exact `--body-file`
  transport, and post-write title/body comparison.
- `~/.config/opencode/scripts/issue-intent.mjs` rejects missing sections,
  metadata omissions, path escape, digest drift, and remote drift.
- The writer is explicitly prohibited from reconstructing or improving issue
  semantics and from hiding GitHub creation inside a helper.
- The deep-dive and evidence-based 5-Whys are recorded in
  `docs/research/issue-creation-handoff-deep-dive-2026-09-20.md` and
  `.factory/artifacts/evidence/issue-creation-handoff-5whys-2026-09-20.md`.

# Verification

- Focused issue-intent suite: 5/5 passed.
- Full shared OpenCode suite: 38/38 passed.
- Continuation command test: 1/1 passed.
- `opencode debug config`: configuration resolved successfully.
- `git diff --check`: passed.
- Issue #80 readback matches the body file used for creation.

# Conclusion

The inspected issue #73 through #79 creation was performed by Sol medium and
faithfully transported its local body files. The reported Luna attribution is
not confirmed for that incident. The permanent correction is therefore
model-independent validation and exact transport, not routing mechanical writes
