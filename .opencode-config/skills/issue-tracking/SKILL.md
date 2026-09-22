---
name: issue-tracking
description: Track work as GitHub Issues to keep session context small. Use when starting non-trivial work, planning work larger than one session, moving verbose findings out of a transcript, or closing out a completed chunk. Issues mirror the repository's canonical tracker (e.g. factory/queue.json); they never replace it.
---

# GitHub Issue Tracking

Track work chunks as GitHub Issues so sessions stay small: detail lives in
issues, sessions hold pointers.

## When To Use

- Starting any non-trivial work chunk in a GitHub-backed repository.
- Planning work larger than one agent session.
- A transcript is accumulating verbose logs, findings, or analysis.
- Closing out a chunk whose verification passed.

## Procedure

### Single-chunk work

1. Before substantial work, open (or reuse) one issue. For a new issue, use the
   planner/writer handoff below; never reconstruct an issue from conversation.
2. Reference the issue number in commits and PRs.
3. Post verbose artifacts (logs, findings, 5-Whys detail) as issue comments.
   Narrate in-session by issue title; keep ids/URLs inside links.
4. Close the issue only after implementation and verification are complete.

### Closeout gate

An evidence file, merged pull request, or passing test suite does not close a
tracking issue. Before reporting a chunk complete:

1. Resolve the canonical tracking issue number from the evidence and confirm
   that the implementation and its stated verification passed.
2. In an interactive, human-authorized session, run the separate identity
   check and then close the exact issue with repository-first syntax:
   `gh issue close --repo REPO NUMBER`.
3. Run the read-only closeout guard:
   `node ~/.config/opencode/scripts/issue-closeout.mjs verify --repo REPO --issues NUMBER[,NUMBER...]`.
4. Require the guard to print `CLOSED` for every issue. An `OPEN` result,
   mutation denial, missing issue, or unknown state keeps the work in progress
   and must be reported as a blocker or follow-up; do not claim completion from
   code or evidence state alone.
5. In auto mode, do not mutate issues. Record the verified work and leave an
   explicit issue-closure follow-up rather than silently carrying an open issue
   into the next session.

For a parent/child map, close only the verified child issue in the current
chunk. Keep the parent open until its own acceptance criteria pass. Do not
retroactively close old issues from inferred evidence without maintainer review.

### Planner/writer handoff

Planning and writing are separate roles. The planning model owns completeness;
the writing model is deterministic transport and must not summarize, improve,
or infer omitted content.

1. The planner writes an issue body with non-empty `# Outcome`, `# Scope`,
   `# Out of scope`, `# Acceptance criteria`, `# Verification`,
    `# Dependencies`, `# Authority and privacy`, `# Source provenance`,
    `# Classification`, `# Priority`, and `# Triage review` sections. The
    triage section must record duplicate and reprioritization review.
2. Next to the body, the planner writes a JSON intent with `schema_version: 1`,
    `repo`, `title`, relative `body_file`, the exact file's `body_sha256`,
    non-empty `labels`, matching `classification`, `priority` (`P0` through
    `P3`), and non-empty `dependencies`, `authority_constraints`,
    `source_provenance`, `duplicate_review`, and `reprioritization_review`
    arrays. `None` is valid when there is genuinely no dependency.

   ```json
   {
     "schema_version": 1,
     "repo": "owner/repository",
     "title": "Bounded outcome",
      "body_file": "issue-body.md",
      "body_sha256": "64 lowercase hexadecimal characters",
      "labels": ["enhancement"],
      "classification": "enhancement",
      "priority": "P2",
      "dependencies": ["None"],
      "authority_constraints": ["Interactive owner-approved write"],
      "source_provenance": ["Decision record path or URL"],
      "duplicate_review": ["Reviewed existing issues; no duplicate."],
      "reprioritization_review": ["Reviewed related issues; no change."]
   }
   ```

3. Before delegation, run
   `node ~/.config/opencode/scripts/issue-intent.mjs validate INTENT.json`.
   Validation failure blocks delegation and GitHub mutation.
4. The writer re-runs the same validation, performs the required separate
   identity check, and invokes only
    `gh issue create --repo REPO --title TITLE --label LABEL ... --body-file BODY_FILE`. The writer
   must use the frozen values verbatim and must not edit either artifact.
5. After creation, run
   `node ~/.config/opencode/scripts/issue-intent.mjs verify-remote INTENT.json NUMBER`.
    Do not report creation complete unless it prints `MATCH` and all frozen labels
    are present remotely.
6. If intent content is wrong, return it to planning. Do not ask the writer to
   repair semantics during transport. Run issue bookkeeping on a routine route;
   model escalation is not a substitute for validation.

### GitHub write sequence

1. Never combine identity and mutation in one shell command. Run
   `gh api user --jq .login`, verify the exact required owner, and only then run
   exactly one mutation as a separate tool call.
2. Put `--repo edoworks/sf0.8` immediately after `create`, `comment`, or `close`.
   This repository-first grammar is the only mutation form admitted by policy.
3. Use `--body-file` for multiline or structured text. Inline bodies containing
   newlines or shell separators intentionally match deny rules.
4. Issue mutations are repo-scoped `ask` operations. Never treat approval from
   an OpenCode `--auto` session as human authorization; do not mutate issues in
   auto mode.
5. Validation and readback do not grant mutation authority. Do not wrap `gh`
   creation inside a helper, because that would bypass the visible permission
   boundary around the exact GitHub command.

### Multi-session work (map pattern)

1. Create one map issue. Body sections: Destination (1-2 lines), Notes,
   Decisions so far (one gist line per closed ticket, linking it), Out of
   scope.
2. Create child decision tickets, each sized to one session; wire blocking
   references in a second pass (issues need ids before they can cross-link).
3. The map is an index, not a store: each decision lives in exactly one
   ticket; the map gists and links, never restates.
4. Per session: load only the map, claim one ticket, resolve it, post the
   resolution as a comment, close it, append one gist line to Decisions so
   far. Resolve at most one decision ticket per session.

## Constraints

- Issues mirror the repository's canonical tracker (e.g. `factory/queue.json`);
  they never replace it.
- Issue creation and comments are GitHub writes: apply the GitHub identity
  boundary (`gh api user --jq .login` returns exactly `hellofoculoom` for
  foculoom repositories) before performing them.
- If the repository has no GitHub remote, use its available task-tracking
  mechanism; never fabricate issues.
- Never close an issue before its stated verification passes.
- Never report a tracked chunk complete until the closeout guard confirms the
  canonical issue is `CLOSED`.
- Never add issue-number literals to global permission rules. Canonical issue
  identity belongs in the repository binding, not the shell policy.
