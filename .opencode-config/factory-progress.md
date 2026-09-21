# Incremental Factory Progress

For every non-trivial task, split the work into small, independently completable chunks so progress is continuously visible in the relevant factories and dashboards. This is a standing requirement across all repositories and sessions, not a project-specific preference.

- Discover and use each repository's existing factory, queue, task, status, evidence, and dashboard mechanisms before starting substantial work.
- Define chunks small enough to complete, verify, and report independently. Prefer multiple meaningful increments over one large hidden batch, without creating artificial busywork.
- Keep the active chunk and its status current in the applicable tracking systems. Mark completion only after implementation and verification are complete, then advance to the next chunk.
- Publish or refresh the evidence and status artifacts that feed each relevant factory dashboard at natural checkpoints, rather than waiting until the entire request is finished.
- When work spans repositories or factories, track each repository's increments separately and keep the cross-repository queue or handoff synchronized.
- Preserve correctness and atomicity: do not split a change at a point that leaves the repository misleading, invalid, or unsafe, and never fabricate progress or evidence merely to populate a dashboard.
- If a repository has no factory or dashboard integration, use the available task tracking and concise progress updates to provide the same incremental visibility.

## Integrated Completion

For non-trivial repository changes, completion means the final reviewed commit
set is integrated, not merely present in a worktree. Unless the repository has a
stricter contract, work on a dedicated feature branch, review the staged diff,
run applicable verification, commit, push, open a pull request, record a
rubberduck review of the final diff, confirm checks, merge, and verify the target
branch. Ordinary commits and the approved feature-branch/PR integration path do
not require a fresh owner approval. An identity-verified, reviewed PR with
passing required checks may be merged autonomously in any `edoworks/*` or
`foculoom/*` repository; never ask the owner to confirm, restart, or say
"proceed" for that ordinary merge. Identity checks and repository protections
remain mandatory, and `--admin` or other bypass operations remain prohibited.
If a merge command is denied, inspect the permission log's winning rule and
retry the tested canonical command shape before attributing the denial to
session state. If integration is genuinely blocked, report the task as blocked
or in progress, never complete.

## Root-Cause And Recurrence Analysis

Before treating a material defect, failed verification, blocker,
trust-boundary gap, or recurring workflow error as resolved, perform and record
an evidence-based 5-Whys analysis. This requirement applies across repositories
and sessions.

- Identify the root cause and material contributing factors.
- Record the immediate correction and the root-cause correction.
- Add a mechanical recurrence guard when feasible and verify that the guard detects or prevents the failure class.
- Stop when evidence runs out and label assumptions. Never invent causes merely to produce exactly five answers.
- Use the repository's canonical incident, evidence, issue, or learning mechanism when one exists. Analysis alone is not completion evidence and does not activate a reusable lesson.
- Do not require a formal incident record for a harmless typo or an expected negative-test outcome unless it exposes a defect, blocker, trust gap, or recurrence risk.

## Completion Notifications

For every non-trivial task, send a completion notification without waiting for
the user to request it. Always invoke the global sanitized ntfy completion path:
`node /Users/hello/.config/opencode/scripts/notify-completion.mjs --result
completed`. When a task is bound to a canonical repository increment, invoke the
repository's approved notifier as an additional canonical milestone; never use
the global path as evidence or fabricate a queue item, milestone, or completion
record. The global ntfy payload must remain fixed and contain no task, project,
repository, personal, employment, source, evidence, credential, or host detail.
Retry only when ntfy explicitly rejects a request before acceptance with `429`;
do not retry ambiguous network or server outcomes that could duplicate alerts.
Preserve fail-open notification policy and report the observed ntfy status in
the final response. If ntfy is
not configured or delivery fails, report that blocker and send a local
operating-system fallback without claiming ntfy delivery.

The global notifier retrieves its routing topic directly from the external
mode-`0400` file `/Users/hello/factory-secrets/ntfy_topic` under its mode-`0700`
owner directory. It must not query Keychain or 1Password during notification
delivery. Rotate that file only when the topic is invalid or replaced. Never
expose the topic in environment variables, command arguments, logs, source,
evidence, or final responses.

## GitHub Identity Boundary

Only `hellofoculoom` may perform owner-authorized GitHub writes or mutate a
branch or tag in the `foculoom` organization. Before each owner write, assert
that `gh api user --jq .login` returns exactly `hellofoculoom`. Every Git push
must clear ambient credential helpers, bind `gh auth git-credential`, name the
exact remote and refspec, and use `--no-follow-tags`. Reviewer identities may
review and comment only; assert the intended reviewer identity before those
actions and never use it for ref mutation. Treat organization rulesets and the
sole-member owner bypass team as trust-boundary controls.

For `edoworks/sf0.8` issue writes, run identity and mutation as separate tool
calls and use repository-first commands such as `gh issue close --repo
edoworks/sf0.8 NUMBER`. Use `--body-file` for multiline text. Issue mutations
are interactive `ask` operations and are prohibited in OpenCode `--auto` mode,
where `ask` does not prove human authorization.

## Merged Branch Cleanup

After work is complete and a pull request is confirmed merged, clean up its
feature branch locally and remotely rather than leaving merged heads behind.

- Verify the PR state is merged and the branch tip is contained in the merged target before deletion.
- Verify the branch is not current or checked out in any active worktree.
- Never delete default, protected, release, stable, unmerged, or explicitly retained branches.
- Use non-force local deletion, delete only the exact remote ref, and prune stale remote-tracking refs afterward.
- Apply the GitHub identity boundary before every remote deletion or repository-setting write.
- If merge state, containment, worktree use, protection, or retention is ambiguous, retain the branch and report the blocker.
- If an integrated feature branch is retained only because it is current, treat that as a temporary blocker: after completion recovery, fast-forward the local target to the exact owner-approved remote target, require exact equality among `HEAD`, the local target, and the live remote target, re-check all worktrees and remote tips, delete the former local and remote refs safely, and verify their absence before reporting cleanup complete.

## Continuation Prompt Maintenance

When work materially changes the priorities, approved scope, trust boundaries,
source-of-truth locations, completed milestones, blockers, or next restart step
captured by `/Users/hello/.config/opencode/commands/continue-sf08.md`, update
that command before completing the task. Keep it concise, remove stale snapshot
claims rather than accumulating history, never place secrets or personal/client
details in it, and validate the OpenCode configuration after editing. Routine
implementation details that do not affect continuation do not require a refresh.

## GitHub Issue Tracking

For non-trivial work in a GitHub-backed repository, use GitHub Issues as the
persistent work tracker so session context stays small.

- Open or reuse one Issue per work chunk before starting substantial work;
  reference the issue number in commits and PRs; close it only after
  implementation and verification are complete.
- Move verbose artifacts (logs, findings, analyses, long discussions) into
  issue comments. Sessions link to the issue instead of carrying that detail
  in context.
- Respect the repository's canonical tracker when one exists (for example
  `factory/queue.json` in sf0.5): the issue mirrors or summarizes canonical
  state and never replaces it.
- Issue creation and comments are GitHub writes. Apply the GitHub Identity
  Boundary section above before performing them.
- If the repository has no GitHub remote, use the available task-tracking
  mechanism instead and do not fabricate issues.
- Work larger than one session gets a map issue with child decision tickets
  sized to one session. The map is an index: each decision lives in exactly
  one ticket; sessions load the map and fetch ticket bodies only on demand.
- Refer to issues by title in narration; keep ids and URLs inside the link.
- Detailed procedure: the `issue-tracking` skill at
  `/Users/hello/.config/opencode/skills/issue-tracking/SKILL.md`.

## Conciseness

- Final responses state what changed, the verification result, and blockers.
  Point to artifacts (issues, evidence files) instead of inlining detail.
- Prefer short bullets over prose; omit anything not decision-relevant.
- Never pad, restate the request, or fabricate status to fill a response.
