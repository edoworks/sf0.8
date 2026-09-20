# Apple Toolchain Freshness

Retrieved 2026-09-18 from Apple sources:

- Xcode SDK and system requirements: https://developer.apple.com/support/xcode/
  currently lists Xcode 27.1 beta and its SDK/deployment support matrix.
- App Store Connect build upload guidance:
  https://developer.apple.com/help/app-store-connect/manage-builds/upload-builds/
- TestFlight overview: https://developer.apple.com/testflight/
  requires an App Store Connect app record, uploaded beta build, and beta
  information; external testing additionally requires beta description and
  beta review information.

Execution machine:

- Xcode 26.6, build 17F113
- iPhoneOS SDK 26.5
- Product A archive deployment target: iOS 26.5
- `altool`: available, Apple version 26.40.1 (174001)
- `iTMSTransporter`: available

The registry records source URLs and retrieval dates. It does not treat the
machine's installed Xcode or remembered requirements as authoritative Apple
policy. No Apple upload or processing operation was invoked.
