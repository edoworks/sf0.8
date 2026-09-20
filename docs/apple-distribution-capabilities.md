# Apple Distribution Capabilities

Last verified: 2026-09-18

The registry is authoritative: `.factory/apple-distribution/capabilities.json`.

| Capability | State | Platforms | App Review stage |
|---|---|---|---|
| `iOS app` | `SUPPORTED_UNVERIFIED` | iOS | `SUPPORTED_UNVERIFIED` |
| `iPadOS app` | `SUPPORTED_UNVERIFIED` | iPadOS | `SUPPORTED_UNVERIFIED` |
| `Universal iPhone/iPad app` | `PARTIAL` | iOS, iPadOS | `PARTIAL` |
| `Native macOS app` | `UNSUPPORTED` | macOS | `UNSUPPORTED` |
| `Mac Catalyst app` | `UNSUPPORTED` | macOS, Mac Catalyst | `UNSUPPORTED` |
| `watchOS companion` | `UNSUPPORTED` | watchOS, iOS | `UNSUPPORTED` |
| `watchOS standalone app` | `UNSUPPORTED` | watchOS | `UNSUPPORTED` |
| `tvOS app` | `UNSUPPORTED` | tvOS | `UNSUPPORTED` |
| `visionOS app` | `UNSUPPORTED` | visionOS | `UNSUPPORTED` |
| `Apple-platform game` | `PARTIAL` | iOS, iPadOS, macOS, tvOS, visionOS | `PARTIAL` |
| `App Clip` | `UNSUPPORTED` | iOS | `UNSUPPORTED` |
| `Universal purchase` | `UNSUPPORTED` | iOS, iPadOS, macOS, watchOS, tvOS | `UNSUPPORTED` |
| `Game Center` | `UNSUPPORTED` | iOS, iPadOS, macOS, tvOS, visionOS | `UNSUPPORTED` |
| `CloudKit` | `UNSUPPORTED` | iOS, iPadOS, macOS, watchOS, tvOS, visionOS | `UNSUPPORTED` |
| `Sign in with Apple` | `UNSUPPORTED` | iOS, iPadOS, macOS, watchOS, tvOS, visionOS | `UNSUPPORTED` |
| `Foundation Models / Apple Intelligence` | `PARTIAL` | iOS, iPadOS, macOS | `PARTIAL` |
| `In-App Purchases` | `PARTIAL` | iOS, iPadOS, macOS, watchOS, tvOS, visionOS | `PARTIAL` |
| `Auto-renewable subscriptions` | `PARTIAL` | iOS, iPadOS, macOS, watchOS, tvOS, visionOS | `PARTIAL` |
| `Apple-hosted assets` | `SUPPORTED_UNVERIFIED` | iOS, iPadOS, macOS, watchOS, tvOS, visionOS | `SUPPORTED_UNVERIFIED` |
| `Kids Category / child-directed product` | `PARTIAL` | iOS, iPadOS | `PARTIAL` |
| `Microphone, camera, or photos` | `PARTIAL` | iOS, iPadOS, macOS | `PARTIAL` |
| `Networking or cloud services` | `PARTIAL` | iOS, iPadOS, macOS, watchOS, tvOS, visionOS | `PARTIAL` |
| `User-generated content` | `PARTIAL` | iOS, iPadOS, macOS, watchOS, tvOS, visionOS | `PARTIAL` |
| `Apps with accounts` | `PARTIAL` | iOS, iPadOS, macOS, watchOS, tvOS, visionOS | `PARTIAL` |
| `Apps without accounts` | `SUPPORTED_UNVERIFIED` | iOS, iPadOS, macOS, watchOS, tvOS, visionOS | `SUPPORTED_UNVERIFIED` |
| `Free apps` | `SUPPORTED_UNVERIFIED` | iOS, iPadOS, macOS, watchOS, tvOS, visionOS | `SUPPORTED_UNVERIFIED` |
| `Paid apps` | `UNSUPPORTED` | iOS, iPadOS, macOS, watchOS, tvOS, visionOS | `PARTIAL` |
| `Export compliance` | `PARTIAL` | iOS, iPadOS, macOS, watchOS, tvOS, visionOS | `PARTIAL` |
| `Accessibility evidence and declarations` | `PARTIAL` | iOS, iPadOS, macOS, watchOS, tvOS, visionOS | `PARTIAL` |
| `Privacy declarations and privacy policy` | `PARTIAL` | iOS, iPadOS, macOS, watchOS, tvOS, visionOS | `PARTIAL` |

## Canonical Apple Products

Distribution consumes `.factory/portfolio.yaml` and does not maintain a product registry.

| Product | Repository | Lifecycle | Release state |
|---|---|---|---|
| `product-a` | `edoworks/product-a` | `active` | `never_released` |
| `vorynce` | `foculoom/vorynce` | `active` | `previously_released` |

## Human Authority

The factory may prepare evidence and drafts, but never submits, publishes, or releases. `APP_REVIEW_READY` is not Apple approval.
