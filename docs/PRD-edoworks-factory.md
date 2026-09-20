# Edoworks Factory PRD

Date: 2026-09-20
Status: ACTIVE
Owner: founder (customer zero)
Parent research: [Edoworks Canonical Factory Deep Dive](research/edoworks-canonical-factory-deep-dive-2026-09-20.md)

## Product Premise

Edoworks Factory is a public, versioned, MIT-licensed software factory that
produces offline-first iOS/iPadOS apps through a deterministic paved road. The
founder is customer zero. The factory is downloaded as an immutable release
artifact, used to scaffold and verify an app, and produces human-gated release
candidates for Apple App Store submission.

The factory does not autonomously publish. It does not promise Apple approval
dates. It does not manage multiple tenants until v1.0.0.

## Owner-Visible Acceptance Sentence

A founder downloads a tagged Edoworks Factory release on a clean Mac, runs
`doctor` to confirm toolchain readiness, initializes a new iOS app, implements
a bounded increment, runs deterministic verification, produces a
distribution-signed archive, and submits it to Apple with human authorization —
without private repository access, oral guidance, or hidden local state.

## Product Laws

### Human Authority Law

No credential use, upload, submission, release, or repository visibility
change happens without explicit human authorization. The factory produces
evidence and candidates; the human decides.

### Clean-Checkout Law

Every build must reproduce from the factory release artifact and the app
repository. No hidden local state, ambient credentials, or founder-only
knowledge may be required.

### Verified-Candidate Law

The factory's daily service level is a verified release candidate: clean build,
tests pass, archive produced, evidence recorded. Public App Store availability
is an external Apple process, not a factory promise.

### Differentiation Law

Every app produced through the factory must be materially differentiated.
Template-generated fleets of near-identical apps violate Apple Guideline 4.2.6
and are explicitly out of scope.

### Recovery Law

Every failure must have a machine-readable classification and a documented
recovery path. If the factory cannot recover, it must fail safely and report.

## Paved Road

The factory's public API is one opinionated journey:

```
download release → doctor → init app repo → confirm PRD →
implement bounded increment → deterministic verify →
release evidence → human-authorized Apple submission
```

### Lifecycle Scripts

- `doctor.sh` — verify Xcode, simulators, disk space, and dependencies
- `bootstrap.sh` — scaffold a new app from the factory template
- `verify.sh` — run build, unit tests, UI tests, static analysis, archive
- `uninstall.sh` — remove factory and residual state

### What the Factory Includes

- Apple distribution capability registry and validator
- Privacy manifest template (`PrivacyInfo.xcprivacy`)
- Release-criteria schema and evidence generator
- Recovery knowledge boundary and failure classifier
- CI policy gate (deterministic verification)
- SLSA-style provenance template for release artifacts
- Compatibility matrix (supported macOS + Xcode versions)
- One opinionated SwiftUI universal-app template (iPhone + iPad)

### What the Factory Excludes

- Dashboards, learned routing, transcript stores
- General portfolio automation
- Autonomous publication or self-modifying policy
- Multi-tenancy (until v1.0.0 and a second paying customer)
- macOS, watchOS, tvOS, visionOS targets (added as independently qualified
  capabilities after v1.0.0)

## Customer Zero

The founder is customer zero. Two reference apps qualify the factory in
sequence:

1. **Reference App 1 (simpler offline utility):** A minimal offline
   iOS/iPadOS utility with no special permissions (no microphone, no backend,
   no accounts). Proves the factory's paved road with the lowest App Review
   friction. Owner selects the specific concept.

2. **Reference App 2 (meow-capture):** A local cat-meow audio
   capture/replay/delete app with microphone permission and on-device
   SoundAnalysis classification. Proves the factory handles a harder
   real-world product with permission complexity and App Review scrutiny.
   Reuses the existing `audio-validation-macos` AudioReplayCore and
   `continuous-competence-ios` SwiftUI spike. Requires owner-authorized public
   name, physical-device validation, and first real-meow fixture.

## Success Metrics

Track these, not app count:

| Metric | Target |
|---|---|
| Clean-checkout build success | 100% from released artifact |
| Unattended run success (30-day qualification) | ≥95% without manual repair |
| Lead time (change to verified candidate) | Measured, trending down |
| Operator effort (human minutes per increment) | Measured, trending down |
| Escaped defects per release | 0 critical, measured minor |
| Apple review outcomes | No template/spam/privacy/metadata rejection |
| Recovery from deliberate failure | Documented and rehearsed |
| Second-operator execution | Succeeds without oral help |

## Versioning

- `v0.1.0` — Initial release: paved road, lifecycle scripts, simpler utility
  template
- `v0.1.x` — Corrections discovered during Reference App 1 qualification
- `v0.2.0` — Post-qualification hardened release (after 30-day test passes)
- `v0.3.0` — Meow-capture capability (microphone, SoundAnalysis, audio clip
  management)
- `v1.0.0` — Stable public compatibility contract (only after second
  independent consumer and paid pilot)

Every factory correction is a new immutable version. The reference app pins to
an exact release artifact digest and upgrades explicitly.

## Non-Goals

- Autonomous App Store publishing
- Multi-tenant SaaS platform
- macOS/watchOS/tvOS/visionOS in v1
- Template app fleet generation
- Customer self-service without human gates
- General-purpose CI/CD platform

## Stop Rules

Stop or re-scope if:

- Work remains founder-dependent after 30-day qualification
- Customers only want bespoke development, not the factory
- Apps converge toward templates despite differentiation efforts
- Apple repeatedly objects on template, spam, privacy, or minimum-functionality
  grounds
- Support costs exceed customer willingness to pay
- Factory governance output consistently exceeds shipped app value

## Dependencies

- Apple Xcode (current version per compatibility matrix)
- Apple Developer Program membership (human-controlled)
- App Store Connect API key (human-controlled, least-privilege)
- GitHub (public repo, releases, CI)
- Swift Package Manager (pinned dependencies)

## Authority Boundaries

| Action | Authority |
|---|---|
| Code changes in factory repo | Founder |
| Factory release publication | Founder |
| App code changes in app repo | Founder |
| Credential use | Human only |
| TestFlight upload | Human only |
| App Store submission | Human only |
| Repository visibility change | Human only |
| License or trademark decision | Human only |
| Customer engagement | Human only |

## Predecessor Disposition

sf0.8 is frozen and superseded — not archived — until the new factory proves:

1. Two Apple-accepted reference apps
2. Recovery from factory failure rehearsed
3. Every open sf0.8 issue dispositioned with successor links
4. All obligations tracked to a successor

Only then are sf0.8 and predecessors archived (read-only, never deleted).