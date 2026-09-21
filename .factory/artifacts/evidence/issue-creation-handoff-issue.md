# Outcome

Make planner-to-writer GitHub issue handoffs complete, deterministic, and
model-independent so a lower-cost writer cannot silently omit planned scope.

# Scope

- Define a machine-validated issue-intent artifact for repository, title, body,
  acceptance criteria, verification, dependencies, authority constraints, and
  source provenance.
- Require the planner to freeze and validate that artifact before delegation.
- Restrict the writer to validation and exact transport via `--body-file`;
  prohibit reconstruction or summarization from conversational context.
- Require a read-back comparison before reporting issue creation complete.
- Add regression fixtures for missing fields and body drift.
- Record the evidence-based 5-Whys and deep-dive conclusion.

# Out of scope

- Changing the approved model routes solely because of this incident.
- Editing existing issue #73 through #79 content without a separate decision.
- Granting issue-write authority to auto-mode sessions.

# Acceptance criteria

- An incomplete intent fails before any GitHub mutation.
- A complete intent produces a body file without model-authored changes.
- Post-write verification detects title or body drift.
- The issue-tracking skill explicitly separates planner and writer duties.
- Tests demonstrate the guard against omission and drift.
- Research distinguishes directly observed model attribution from hypotheses.

# Verification

- Run the issue-intent validator test suite.
- Validate the shared OpenCode configuration and updated skill.
- Run repository checks for changed sf0.8 evidence files.
- Read back the created tracking issue and compare it with this body.

# Authority and privacy

- GitHub identity must be checked separately before every mutation.
- Issue writes remain interactive `ask` operations and are prohibited in
  OpenCode `--auto` mode.
- No secrets, private audio, personal data, or hidden model reasoning may enter
  the artifact or GitHub issue.

# Source provenance

- User report dated 2026-09-20.
- OpenCode session/message/tool records for the issue #73 through #79 creation
  sequence.
- GitHub issue bodies and local body-file artifacts retrieved 2026-09-20.
- Shared issue-tracking skill and model-routing benchmark records retrieved
  2026-09-20.
