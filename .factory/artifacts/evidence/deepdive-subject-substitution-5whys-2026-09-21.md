# Deep-Dive Subject Substitution 5-Whys

Date: 2026-09-21

Incident: a request to identify an alternate name for the blocked FocusGate
release was answered with a researched name for the separate meow-capture
product. Related prior deep-dive attempts also stopped when a short request did
not carry enough subject context into the delegated task.

## Evidence

- The deep-dive command required audience, jurisdiction, decision, cutoff,
  sources, and stopping rules, but did not require an immutable subject lock.
- The incorrect report explicitly scoped itself to `meow-capture` even though
  the active blocker was FocusGate's occupied App Store name.
- The repository contains prominent meow-capture identity requirements, making
  it a plausible but incorrect context-derived substitute.
- A prior 5-Whys covered omitted research topics, but its guard did not test for
  subject substitution after a report had selected a topic.

## Analysis

1. **Why was the wrong product researched?** The delegated researcher selected
   meow-capture as the subject instead of preserving FocusGate from the active
   request.
2. **Why could it select a different subject?** The command required a scope but
   did not require the scope to quote and lock the user's exact named subject.
3. **Why did the normal evidence checks not catch this?** They validated source
   quality and report structure, not consistency between the request subject and
   every finding or recommendation.
4. **Why was nearby repository context able to override the request?** The fresh
   subagent had a generic research instruction and a repository containing
   several product identities, with no explicit rule that adjacent products are
   out of scope unless the user names them.
5. **Root cause supported by evidence:** the deep-dive handoff contract lacked a
   mechanical subject-lock and final subject-consistency assertion. The prior
   recurrence guard covered missing fields, not a wrong-but-complete scope.

## Corrections

- Immediate correction: reject `WhiskerEcho` for FocusGate and screen candidates
  against the FocusGate product promise; record `NowNest` only as a provisional,
  uncleared candidate.
- Root-cause correction: require every deep-dive to quote the authoritative
  subject before searching and forbid substitution from nearby repository or
  conversation context.
- Recurrence guard: contract tests require the command to contain a subject lock,
  adjacent-subject exclusion, ambiguity stop, and final subject-consistency
  check.

## Verification

The reusable command/skill contract test must pass after the guard is added. A
contract-level negative assertion confirms that the command explicitly rejects
an answer about an adjacent product when another subject is locked.
