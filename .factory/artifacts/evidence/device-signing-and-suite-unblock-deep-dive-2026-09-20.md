# Device Signing And Verification Blocker Deep Dive

## Scope And Cutoff

- Audience: founder/customer-zero decision maker and factory operator.
- Jurisdiction: Apple-platform development on macOS/Xcode for locally paired
  iPhone/iPad devices; engineering and authorization analysis only.
- Decision: determine which blocker can be safely unblocked now and whether
  physical-device validation can proceed without owner authorization.
- Cutoff: 2026-09-20 inclusive. Local sources and command results were verified
  on 2026-09-20.
- Stopping rule: stop after the verification blocker is either mechanically
  corrected or shown to require policy review, and after the physical-device
  action is classified as local or human-authorized.

## Executive Answer

- **High confidence: verification blocker unblocked.** The full-suite failure
  was fixture drift, not an audio defect. The repository fixture omitted four
  existing `edoworks/factory` PR rules from the resolved OpenCode policy. Adding
  those exact rules restored the equality guard; all 248 tests pass.
- **High confidence: physical-device blocker remains.** Paired devices are
  discoverable, but the experiment lacks an authenticated account/profile for
  its selected development team. No local fixture or policy change can create
  that authorization safely.
- **High confidence: work can proceed in parallel.** Audio unit tests, host
  replay, simulator work, and signing-readiness preflight can proceed. They
  cannot be represented as physical microphone, permission, route, playback,
  or interruption evidence.

## Findings

### Claim 1: The full-suite failure was policy-fixture drift

**Evidence:** The failing test compares the resolved OpenCode `bash` rules with
`tests/permission_policy_fixture.json`, filtering GitHub issue/API/PR rules
(repository primary source: `tests/test_permission_policy.py:82-92`, retrieved
2026-09-20). The resolved configuration contains four
`gh pr {view,checks,create,edit} --repo edoworks/factory` rules, while the
fixture did not (local configuration primary source:
`/Users/hello/.config/opencode/opencode.jsonc:106-109`, retrieved 2026-09-20).

**Counterevidence:** The fixture is a security boundary and could be stale for
a deliberate reason. The repository record warns that policy reconciliation
must not weaken controls (`.factory/artifacts/evidence/host-audio-validation-
full-suite-blocker-2026-09-20.md:19-40`). No evidence shows those four rules
were intentionally excluded; their actions and patterns exactly match the
existing live policy's repository-scoped rules.

**Implication:** Updating the fixture with the four exact existing rules is a
reconciliation, not a permission expansion. The mechanical guard is restored.

### Claim 2: The verification blocker is resolved

**Evidence:** After the fixture-only change:

- `python3 -m unittest tests.test_permission_policy`: 6 passed.
- `python3 -m unittest discover -s tests -p 'test_*.py'`: 248 passed.
- `git diff --check` on the changed evidence/fixture paths: passed.

These are local primary command results, retrieved 2026-09-20.

**Counterevidence:** The historical blocker record says 256 tests were
attempted. The current run discovers 248, so the old count is stale; it is not
evidence that the current suite covered fewer intended tests without further
comparison.

**Implication:** The active increment may report a green repository suite, but
must not rewrite the historical blocker record. This report supersedes its
status for current verification while preserving the original observation.

### Claim 3: Physical-device validation remains blocked by signing

**Evidence:** The local device attempt reported `No Account for Team
"YM5MWC8YJF"` and no matching provisioning profile; CoreDevice still
recognized paired devices (`docs/research/continuous-competence-device-
signing-5whys-2026-09-20.md:6-13`, retrieved 2026-09-20). The meow-capture
contract explicitly assigns permission, routes, microphone, playback, and
interruption recovery to physical iPhone/iPad evidence and says host replay is
not device proof (`docs/decisions/2026-09-20-meow-capture-product-contract.md:
63-72`, retrieved 2026-09-20).

**Counterevidence:** Simulator and Mac replay can validate deterministic UI,
mapping, thresholds, buffering, deletion logic, and approved-file processing.
They cannot validate physical audio routes or OS-mediated permission behavior
under this contract.

**Implication:** Do not bypass signing, use a fake classifier result, or claim
physical acceptance. The remaining action is an explicit owner-authorized
development-account/team/profile setup, followed by device evidence.

## Conflicts And Unknowns

- The suite count changed from 256 in the earlier blocker record to 248 now;
  the cause is not established by this increment.
- Apple documentation pages were identified but the fetched device-running page
  required JavaScript and the attempted account-role URLs were unavailable or
  redirected. They are retained as lead-only sources, not used to establish
  Apple policy claims.
- It is unknown whether the owner prefers the existing team, a Personal Team,
  or another authorized development team. That choice may affect entitlements,
  profile duration, and repeatability.
- No account login, provisioning update, device install, TestFlight upload, or
  release was attempted.

## Decision Implications

1. Continue issue #75 with the green local suite, focused audio tests, host
   replay, and simulator/preflight work.
2. Add or retain a signing-readiness check before any future physical-device
   build; fail closed when account/team/profile readiness is absent.
3. Request owner authorization only for the Apple account/team/profile action
   and the subsequent bounded device session.
4. Keep physical-device acceptance open until separate iPhone and iPad evidence
   exists.

The conclusion changes if an authorized development team/profile becomes
available and the exact-revision device install and required evidence pass. It
also changes if the owner explicitly narrows the acceptance contract to omit
physical-device claims.

## Sources

### Primary

- `tests/test_permission_policy.py`, repository test contract, retrieved
  2026-09-20.
- `/Users/hello/.config/opencode/opencode.jsonc`, resolved policy source,
  retrieved 2026-09-20.
- `tests/permission_policy_fixture.json`, checked-in policy fixture, retrieved
  2026-09-20.
- `docs/research/continuous-competence-device-signing-5whys-2026-09-20.md`,
  local Xcode/CoreDevice observation, retrieved 2026-09-20.
- `docs/decisions/2026-09-20-meow-capture-product-contract.md`, owner-bound
  acceptance contract, retrieved 2026-09-20.
- Verification command results listed under Claim 2, retrieved 2026-09-20.

### Secondary

- None used for material claims.

### Lead-only

- Apple Developer Documentation, “Running your app on simulated or physical
  devices,” https://developer.apple.com/documentation/xcode/running-your-app-on-simulated-or-physical-devices
  (retrieved 2026-09-20; fetched page required JavaScript, so not relied on).
- Apple Developer Account Help, “Create a development provisioning profile,”
  https://developer.apple.com/help/account/provisioning-profiles/create-a-development-provisioning-profile/
  (retrieved 2026-09-20; page content was not independently sufficient for a
  material claim in this run).
