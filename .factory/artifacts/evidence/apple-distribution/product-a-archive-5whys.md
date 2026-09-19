# Product A Archive Signing 5-Whys

## Problem

The first real Product A archive succeeded, but it is development-signed and
cannot be treated as a TestFlight distribution archive.

## Evidence

- Archive: `/var/folders/m6/j69tcnk52059qvy0_6hnxk5r0000gq/T/opencode/ProductA-ef94f24.xcarchive`
- Source commit: `ef94f2492d3e73d98fb883320bad2902c64f3e15`
- Toolchain: Xcode 26.6, build 17F113, iPhoneOS SDK 26.5
- `codesign` identity: Apple Development
- Entitlement: `get-task-allow=true`
- Distribution retry failed because automatic development signing conflicts with
  the manually requested `Apple Distribution` identity.

## Analysis

1. Why is the archive not distribution-ready? The archive has a development
   signing identity and development entitlement.
2. Why did Xcode select development signing? The project uses automatic signing
   and the available managed provisioning profile is a development profile.
3. Why did an explicit distribution identity not fix it? The project has no
   distribution signing configuration; Xcode rejected the conflicting override.
4. Why is that configuration absent? The factory has only modeled signing as a
   preflight fact and has not resolved the owner-managed distribution profile
   boundary.
5. Why was that treated as sufficient? The prior workflow counted archive plans
   and tests without requiring an archive's signing entitlements to prove
   distribution eligibility.

## Correction

- Immediate: classify the development archive as local archive proof only and
  stop TestFlight readiness.
- Root cause: add archive inspection and an explicit owner-controlled
  distribution-signing configuration gate before claiming delivery readiness.

## Recurrence Guard

`scripts/inspect-apple-archive.py` exits non-zero when `get-task-allow=true` and
reports signing identity and entitlements from the archive itself.

## Owner

Issue #38 owns the distribution-signing blocker.
