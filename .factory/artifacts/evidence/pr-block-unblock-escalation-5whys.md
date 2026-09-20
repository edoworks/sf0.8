# PR Block Unblock Escalation: 5-Whys

Date: 2026-09-19
Observation: the PR workflow was blocked by an explicit `gh pr` permission
denial, but the user was told only that work could not continue.

## Analysis

1. **Why did the session stop without an unblock choice?** The final response
   reported the tool restriction but omitted the available authorization paths.
2. **Why were the paths omitted?** The response treated a blocked mutation as a
   terminal status instead of a human-action handoff.
3. **Why was it treated as terminal?** The completion workflow emphasized
   avoiding unauthorized writes but had no required escalation format.
4. **Why was there no escalation format?** Permission boundaries were recorded
   as prohibitions, not as paired `blocked action -> safe user option` records.
5. **Why was that model incomplete?** The recurrence guard covered identity and
   mutation safety, but not operator agency after a safe stop.

## Correction

- Keep the PR mutation blocked; do not bypass the permission policy.
- Offer the user explicit options: enable interactive `gh pr` permissions and
  have the agent create the PR, or create the PR manually with the prepared
  branch and template, then return for review and cleanup.
- Update continuation guidance to require an unblock menu whenever a safe
  external action is blocked.
- Put the catch-all `gh pr *` deny before specific permitted operations because
  OpenCode uses last-match-wins semantics.

## Second Boundary Discovered

The specific OpenCode config rule was corrected and validated, but the tool
execution layer continued to reject `gh pr review`. This is a separate
enforcement plane from `~/.config/opencode/opencode.jsonc`; editing the project
or global config cannot prove that the host-level tool policy has changed.

The safe unblock options are therefore explicit:

1. A human reviewer using `supportfoculoom` approves PR #1 in GitHub's UI; or
2. The host/tool policy is changed to permit `gh pr review` for the validated
   reviewer identity, then OpenCode is restarted and the command is retried.

The agent must not substitute `gh api`, another identity, or a direct merge.

## Recurrence Guard

Any blocked external mutation must report: the exact blocked operation, why it
is blocked, the minimum permission or human action needed, and the next safe
verification step. A blocked operation is not complete until that handoff is
  present or the user explicitly defers it. Permission configurations must place
  specific exceptions after broad deny rules and test exact production command
  shapes after restart.
If the command remains blocked after those checks, report the separate
host/tool-policy boundary and provide the two unblock options above.
