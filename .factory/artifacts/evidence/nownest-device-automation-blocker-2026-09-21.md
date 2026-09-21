# NowNest Physical UI Automation Blocker

Date: 2026-09-21
Subject: NowNest G8 physical-device automation
Status: BLOCKED, not passed

## Observed evidence

- `xcrun devicectl list devices` found paired physical devices.
- The iPhone 16 Pro Max reported iOS 26.7, Developer Mode enabled, and developer disk image services available.
- The iPad Air reported iPadOS 26.7, Developer Mode enabled, but developer disk image services unavailable.
- The Mac has Xcode 26.6 (build 17F113).
- `xcodebuild test -project NowNest.xcodeproj -scheme NowNest -destination 'id=39C04F90-1CAA-5533-8FFD-BFB33A373880' -only-testing:NowNestUITests` built and reached the phone, then failed before test execution with: `Timed out while enabling automation mode`.
- Xcode also reported: `Error locating DeviceSupport directory`.

## 5-Whys

1. **Why did automated physical UX testing not complete?** XCTest timed out while enabling automation mode on the iPhone, and the iPad could not mount developer disk image services.
2. **Why could XCTest not enable automation?** The connected devices run 26.7 while the installed Xcode is 26.6 and lacks the matching device-support payload.
3. **Why was the mismatch discovered only during the test run?** The release procedure checked simulator evidence and device pairing, but did not require a device-support compatibility preflight before launching XCUITest.
4. **Why was that preflight absent?** Physical-device validation was treated as a human-only handoff, conflating human authority for TestFlight/release actions with the ability to automate repeatable device traversal.
5. **Why did that process model persist?** The lane documented the evidence boundary but did not encode the available `devicectl`/XCUITest path as a required post-simulator step with a machine-readable compatibility gate.

## Correction

- Immediate: do not mark G8 passed. Install/use Xcode with iOS/iPadOS 26.7 device support, then rerun the NowNest UI tests on both paired devices.
- Root-cause correction: make physical-device automation a standard post-simulator lane; require a preflight that verifies connected device OS support, Developer Mode, developer disk image services, and a successful XCUITest smoke run. Keep human visual/UX observation and release authorization separate.

## Retry results

- iPhone 16 Pro Max (iOS 26.7): automated NowNest UI suite passed 5/5 after moving the confirmation assertion before the other post-capture waits. Result bundle: `/Users/hello/Library/Developer/Xcode/DerivedData/NowNest-gxffueviazfdkjchxiijuosucvwp/Logs/Test/Test-NowNest-2026.09.21_12-37-22--0700.xcresult`.
- iPad Air (iPadOS 26.7): blocked before test execution because `The developer disk image could not be mounted on this device`.
- iPad Pro simulator (iOS 26.5): automated NowNest UI suite passed 5/5. Result bundle: `/Users/hello/Library/Developer/Xcode/DerivedData/NowNest-gxffueviazfdkjchxiijuosucvwp/Logs/Test/Test-NowNest-2026.09.21_12-45-33--0700.xcresult`.
- The UI suite now retains screenshot attachments for launch, capture confirmation, parked-idea review, NOW edit, and deletion. The updated iPad simulator run passed 5/5 at `/Users/hello/Library/Developer/Xcode/DerivedData/NowNest-gxffueviazfdkjchxiijuosucvwp/Logs/Test/Test-NowNest-2026.09.21_12-51-34--0700.xcresult`.
- iPad Air physical device (iPadOS 26.7): automated NowNest UI suite passed 5/5 with screenshot attachments. Result bundle: `/Users/hello/Library/Developer/Xcode/DerivedData/NowNest-gxffueviazfdkjchxiijuosucvwp/Logs/Test/Test-NowNest-2026.09.21_13-11-18--0700.xcresult`.
- Persistence UI test passed on the iPhone simulator and physical iPad: a parked idea was saved, the app was terminated and relaunched, and the same `PARKED` idea was found in Review. Physical iPad result bundle: `/Users/hello/Library/Developer/Xcode/DerivedData/NowNest-gxffueviazfdkjchxiijuosucvwp/Logs/Test/Test-NowNest-2026.09.21_13-27-24--0700.xcresult`.
- Full iPad simulator verification passed 6 UI tests and 6 unit tests, including persistence relaunch and retained visual checkpoints. Result bundle: `/Users/hello/Library/Developer/Xcode/DerivedData/NowNest-gxffueviazfdkjchxiijuosucvwp/Logs/Test/Test-NowNest-2026.09.21_13-25-55--0700.xcresult`.
- Physical iPhone current-revision persistence journey passed in isolation with retained screenshots. Result bundle: `/Users/hello/Library/Developer/Xcode/DerivedData/NowNest-gxffueviazfdkjchxiijuosucvwp/Logs/Test/Test-NowNest-2026.09.21_13-43-40--0700.xcresult`.
- Physical iPhone current-revision deletion journey passed in isolation with retained screenshots. Result bundle: `/Users/hello/Library/Developer/Xcode/DerivedData/NowNest-gxffueviazfdkjchxiijuosucvwp/Logs/Test/Test-NowNest-2026.09.21_13-45-38--0700.xcresult`.
- One aggregate physical iPhone run had an intermittent single-test failure while the other 5 UI tests and all 6 unit tests passed; individual retries passed. The aggregate run is not represented as a clean suite.
- G8 remains open until iPad device automation and human visual checks are complete.

## Recurrence guard

Before the next physical-device run, record all of the following in the gate evidence:

- `xcodebuild -version`
- each target device OS version and `developerModeStatus`
- `ddiServicesAvailable: true`
- a successful XCUITest result bundle for both iPhone and iPad
- separate human visual observations for layout and subjective UX

Any missing or incompatible preflight item blocks G8 and prevents a false pass.
