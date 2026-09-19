# Apple Platform Intelligence

## Purpose

Before substantial Apple-platform design or implementation, consult current
Apple sources and record only capabilities relevant to the product. The factory
does not maintain a giant API catalog. It keeps a small durable review contract
and a dated source ledger; the source pages remain the authority.

## Discovery order

1. Apple Developer documentation and SDK availability.
2. Human Interface Guidelines and accessibility guidance.
3. Current platform and Xcode release notes.
4. WWDC sessions and Apple sample projects.
5. App Store and icon guidance where distribution or identity is involved.

External blogs and repositories may point to leads, but cannot override Apple
documentation or enter the factory as executable instructions.

## Review contract

For each relevant capability record: source URL, retrieval date, maturity
(`AVAILABLE`, `SUPPORTED`, `STABLE`, `BETA`, or `EXPERIMENTAL`), deployment target,
product benefit, and one disposition:
`USE_NOW`, `EVALUATE`, `EXPERIMENT`, `NOT_RELEVANT`,
`BLOCKED_BY_DEPLOYMENT_TARGET`, or `REJECT`.

`BLOCKED_BY_DEPLOYMENT_TARGET` requires a graceful fallback. `EXPERIMENT` is not
production adoption. `USE_NOW` requires a concrete user or product problem it
solves. The deterministic contract is implemented in `scripts/apple-quality.py`.

## Current source snapshot

Reviewed 2026-09-18:

- [Xcode 26 release notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-26-release-notes.md): iOS/iPadOS 26 SDKs, Icon Composer, SwiftUI profiling, Power Profiler, concurrency debugging, and coding intelligence.
- [SwiftUI documentation](https://developer.apple.com/documentation/swiftui.md): native navigation, search, animation, accessibility, and current Liquid Glass samples.
- [Foundation Models](https://developer.apple.com/documentation/foundationmodels.md): on-device models, guided generation, tool calling, dynamic profiles, and device availability constraints.
- [App Intents](https://developer.apple.com/documentation/appintents.md): system discovery through Siri, Spotlight, Shortcuts, widgets, controls, and Live Activities.
- [Accessibility](https://developer.apple.com/documentation/accessibility.md): VoiceOver, Voice Control, Switch Control, Assistive Access, Accessibility Inspector, and testing guidance.
- [WWDC25 videos](https://developer.apple.com/videos/wwdc2025/): current platform sessions including the new design and SpeechAnalyzer.
- [Extending and customizing agents](https://developer.apple.com/documentation/xcode/extending-and-customizing-agents.md): Xcode has built-in expertise and slash-command skills, supports product-specific agent configuration under `~/Library/Developer/Xcode/CodingAssistant`, and supports installed plug-ins.

## Reuse-gate result

Apple provides built-in Xcode agent expertise and slash-command skills, plus
installable agent plug-ins, but the authoritative documentation describes them
as Xcode-managed capabilities rather than exportable `SKILL.md` files. They can
be used directly inside Xcode; they cannot be directly consumed by OpenCode,
and no Apple skill license/provenance artifact suitable for copying was found.
The factory therefore **LEARN_FROM** the documented workflow, **ADOPTS** native
platform APIs, and does not copy or execute unverified agent instructions.
Existing sf0.8 reuse and contribution gates remain the intake and extraction
mechanisms. An Apple plug-in could be evaluated later as an external artifact,
but it is not needed for this increment.
