# 5-Whys: Issue-First Tracking Blocker

Date: 2026-09-19

## Observed failure

The required GitHub map issue could not be created from this session. The
identity assertion succeeded (`gh api user --jq .login` returned
`hellofoculoom`), but the command-permission policy denied `gh issue create`.

## Evidence-based analysis

1. **Why** was no issue created? The issue-create command was denied before
   reaching GitHub.
2. **Why** was it denied? The session policy allows issue reads/comments/close
   but does not allow the issue-create command pattern.
3. **Why** does that matter? The repository requires issue-first tracking for
   material work, so local research cannot be honestly marked as issue-bound.
4. **Why** was local artifact tracking used instead? The repository has Git-visible
   evidence artifacts but no local canonical work queue equivalent to a GitHub
   issue.
5. **Why** is this still unresolved? The permission boundary requires an owner
   or session-policy change; the agent cannot authorize that change.

## Correction and recurrence guard

- Immediate correction: recorded the blocker, scope, acceptance criteria and
  all research in Git-visible artifacts; did not claim issue creation or DONE.
- Root-cause correction required: permit the approved owner identity to create
  the map issue, or provide a repository-approved local issue queue.
- Mechanical guard: artifact `issue_first.blocked=true` and verification
  `issue_created=false` make the incomplete control-plane state machine-visible.
  Any completion gate for this increment must reject `DONE` while those values
  remain true.

Assumption: the original denial was session permission policy rather than a
GitHub API failure, based on the tool response. The owner-authorized REST API
retry created map issue #50; the control-plane blocker is resolved.
