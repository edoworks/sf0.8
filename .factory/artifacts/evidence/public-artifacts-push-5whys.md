# Public Artifacts Push Handoff: 5-Whys

Date: 2026-09-19
State: handoff corrected; push remains human-approved

## Observation

The exact push for the owner-approved `edoworks/artifacts` repository was
rejected before a human approval prompt was presented.

## Analysis

1. **Why did publication stop?** The `git push` tool call was rejected by the
   active command policy.
2. **Why was it rejected without a prompt?** The command resolved to `ask`, but
   the current non-interactive execution path cannot satisfy an `ask` decision.
3. **Why was no approval option presented?** The workflow treated tool-level
   rejection as a terminal blocker instead of opening an explicit human
   confirmation step.
4. **Why did the workflow do that?** The release procedure documented exact
   push safeguards but did not define an assistant-to-human handoff for
   command-level `ask` operations.
5. **Why was that handoff missing?** Fail-closed permission controls were
   implemented as command rules without a corresponding interaction contract
   requiring the assistant to surface the pending decision.

## Correction

- Keep `git push` as an approval-gated operation; do not broaden it to allow.
- Surface the exact command and target ref through an explicit human question.
- Execute the push only after the human confirms that exact operation.
- Record the result and verify the remote ref before creating a release.

## Recurrence guard

When a release command resolves to `ask` but the current tool path rejects it,
the assistant must stop, present the exact command/ref/remote as a decision,
and never retry through a broader command, raw API, or bypass form.
