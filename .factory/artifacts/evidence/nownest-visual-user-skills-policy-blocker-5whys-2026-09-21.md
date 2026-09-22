# NowNest Visual-User Skills Policy Blocker 5-Whys

Date: 2026-09-21
Subject: NowNest visual-user support and skills research, issue #105
Status: CORRECTION IN PROGRESS

## Evidence

- The pull request policy check blocked `.agents/skills/neuroinclusive-ux/SKILL.md`
  as an `unclaimed gated changed path`.
- `scripts/validate-ci-change.py` derives gated paths from the changed-path
  ledger and requires the issue number to exist in `.factory/control-plane-bindings.json`.
- Issue #105 existed and was verified remotely, but the binding still ended at
  the earlier skill work on issue #100.
- The local contract, skill-sharing, ecosystem, and diff checks passed before
  the pull request policy check.

## Analysis

1. **Why did the pull request policy check fail?** The changed
   `neuroinclusive-ux` skill path had no bound issue in the control-plane
   ledger used by the CI changed-path gate.
2. **Why had it no bound issue?** Issue #105 was created after the prior
   skill-creation binding for issue #100 and no new binding/ledger record had
   been added before opening the pull request.
3. **Why was the missing binding not caught before the PR?** Local verification
   ran skill and ecosystem validators, but not the exact pull-request event
   range with the new issue binding.
4. **Why was that validation step absent?** The issue-tracking workflow and the
   repository changed-path guard are separate operations; issue creation does
   not mechanically create a control-plane binding.
5. **Root cause supported by evidence:** the material-work workflow lacks a
   pre-PR synchronization step that binds a newly created issue to every gated
   changed path before the CI range check.

## Corrections

- Immediate correction: add issue #105 to `.factory/control-plane-bindings.json`
  and record its changed paths in `.factory/artifacts/ledger/issue-105.json`.
- Root-cause correction: make the exact `validate-ci-change.py` pull-request
  event-range invocation a required pre-PR verification for future gated skill
  changes.
- Recurrence guard: the CI changed-path gate itself must continue to fail closed
  on unbound gated paths; this incident demonstrates that it detects the class
  of omission.

## Verification

Run the exact base/head range after the binding correction and require the
decision to be `PASS`, then rerun the full repository checks before merging.
