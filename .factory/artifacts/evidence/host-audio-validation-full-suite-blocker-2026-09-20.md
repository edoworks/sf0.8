# Full-Suite Verification Blocker

Date: 2026-09-20
Scope: issue #75 validator-hardening increment

## Observed Failure

`python3 -m unittest discover -s tests -p 'test_*.py'` executed 256 tests and
failed one unrelated test:

`test_permission_policy.PermissionPolicyFixtureTests.test_resolved_opencode_github_rules_match_fixture`

The resolved OpenCode GitHub permission rule list differs from
`tests/permission_policy_fixture.json`. The failure is outside the two audio
files changed in this increment and no policy files were modified to mask it.

## 5-Whys

1. Why did the full suite fail? The effective OpenCode permission rules did not
   equal the checked-in expected rule sequence.
2. Why did the expected sequence differ? The live/global configuration and the
   repository fixture are out of sync.
3. Why is that not corrected here? This increment is scoped to audio evidence
   validation, and changing trust-boundary policy without an explicit policy
   review could weaken or misrepresent the security control.
4. Why is the mismatch material? The test is a fail-closed drift guard for
   GitHub mutation permissions.
5. Why must the audio increment not claim a green suite? A repository-wide
   verification failure remains unresolved even though focused audio checks
   pass.

Root cause: pre-existing effective-config/fixture drift in the permission
policy control plane.

Immediate correction: preserve the failure, isolate the audio verification,
and do not modify the policy fixture or effective configuration as part of
issue #75.

Recurrence guard: the existing resolved-config equality test continues to fail
closed until an authorized policy reconciliation is reviewed and verified.

## Audio Verification Status

- `python3 -m unittest tests.test_validate_audio_replay` — 7 passed.
- `swift test --package-path experiments/audio-validation-macos` — 9 passed.
- Scoped `git diff --check` — passed.

This blocker does not establish or invalidate physical-device, microphone,
real-cat, or release evidence. Issue #75 remains open.
