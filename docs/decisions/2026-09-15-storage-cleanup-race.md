# Storage Cleanup Race

## Evidence

The first deletion pass found no `xcodebuild` or `xctest` process and no booted
simulator, but Xcode and Simulator applications were still open. Removing the
109 plist-marked ephemeral XCTest device trees produced `Directory not empty`
errors for several trees. After both applications were quit, the remaining
ephemeral trees were removed successfully.

## 5-Whys

1. Why did the first cleanup pass report deletion errors? Some device trees were
   still being accessed or recreated.
2. Why were they still being accessed? Xcode and Simulator were open even
   though no test runner or booted device was detected.
3. Why did cleanup proceed while those applications were open? The preflight
   checked test processes but not the owning GUI applications.

The analysis stops because the deeper daemon or filesystem cause is not
established by the evidence.

## Correction and Guard

- Immediate correction: quit Xcode and Simulator, then retry only the remaining
  ephemeral trees.
- Root-cause correction: treat open Xcode/Simulator applications as an unsafe
  cleanup state, even when no test runner is active.
- Mechanical guard: before deleting XCTest device data, require zero exact
  matches for `Xcode`, `Simulator`, `xcodebuild`, and `xctest`, and re-check the
  plist `isEphemeral` flag immediately before each deletion.
