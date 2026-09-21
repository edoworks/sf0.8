# 5-Whys: Physical Device Signing Blocker

Date: 2026-09-20
Scope: local installation attempt on the available paired device Ethan.

## Observed failure

CoreDevice and Xcode recognized Ethan as available, but the device build failed:

`No Account for Team "YM5MWC8YJF"` and `No profiles for
ai.foculoom.competence-check-experiment were found.` Automatic provisioning was
therefore unable to proceed.

## Evidence-based chain

1. **Why** did the physical build fail? Xcode had no authenticated Apple
   Developer account for the selected team and no iOS App Development
   provisioning profile matched the experiment bundle identifier.
2. **Why** were those unavailable? The native spike has no configured
   development team/profile path, and this machine's Xcode account state does
   not authorize automatic provisioning for the team.
3. **Why** was signing omitted? The spike was intentionally created as an
   unsigned simulator/local experiment to avoid making Apple account or release
   changes before evidence justified them.
4. **Why** did that become a blocker now? The experiment moved from simulator
   feasibility to physical Customer Zero testing, which requires a different
   signing boundary.
5. **Why** was this not detected before the device attempt? The native preflight
   checked device availability but did not check signing readiness for the
   chosen bundle identifier.

## Correction and recurrence guard

- Immediate correction: use `devicectl` and `xcodebuild -showdestinations` for
  device availability; do not use `xctrace` as the device gate.
- Root-cause correction required: add a human-approved development team and
  provisioning profile for this experiment, or explicitly keep physical testing
  deferred.
- Mechanical guard: a future Apple experiment preflight should check both the
  CoreDevice target and the bundle's provisioning readiness before attempting a
  device install.

## Human gate

Automatic provisioning (`-allowProvisioningUpdates`), Apple Developer account
changes, signing-profile creation, TestFlight, and release remain human-
authorized. No such action was attempted.
