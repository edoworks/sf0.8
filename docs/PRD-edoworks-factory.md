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

## Evidence Contracts And Cutover Guards

Each gate below defines its evidence artifact, owner, validation command, fail
condition, and cross-system synchronization requirement. A gate is not closed
until its validation command passes and its evidence artifact is committed.

### Release Distribution Contract

- **Evidence:** a release receipt recording tag, artifact URL, digest,
  prerelease flag, immutability flag, and README install-path verification.
- **Owner:** founder (release publication is human-authorized).
- **Validation:** a CI release-contract test resolves the documented download
  URL, verifies the artifact and digest, checks prerelease/immutability state,
  and rejects any release whose README path is unavailable or whose declared
  artifact does not match the release record.
- **Fail condition:** the documented URL returns 404, the artifact digest does
  not match, or the release is marked prerelease when a stable release is
  required for cutover.
- **Synchronization:** README, release record, and CI test must all agree on
  the exact artifact URL and digest.

### Apple Acceptance Receipt

- **Evidence:** a receipt recording app bundle ID, version, build number,
  Apple processing status, submission date, review disposition, and acceptance
  date. Distinguishes archive, processed build, submitted version, and
  accepted version.
- **Owner:** founder (submission is human-authorized).
- **Validation:** the cutover guard verifies the receipt is committed and its
  acceptance status is confirmed. TestFlight or simulator evidence does not
  satisfy this gate.
- **Fail condition:** no acceptance receipt exists, or the receipt records a
  status short of Apple acceptance.
- **Synchronization:** factory issue #10 (and #14 for Reference App 2) must be
  closed with the receipt attached before predecessor freeze can proceed.

### Qualification Ledger

- **Evidence:** a version-pinned ledger recording daily receipts for the
  qualification period: date, change description, unattended success flag,
  manual repair flag, failure classification, operator identity, denominator,
  and cumulative success rate.
- **Owner:** founder (qualification execution is owner-authorized).
- **Validation:** the promotion guard verifies the ledger covers at least 10
  consecutive weekday changes, cumulative unattended success rate >= 95%, at
  least one second-operator run, and a complete failure taxonomy.
- **Fail condition:** the ledger is missing, incomplete, below threshold, or
  lacks independent-operator evidence.
- **Synchronization:** factory issue #11 must be closed with the ledger
  attached before v0.2.0 promotion or predecessor freeze.

### Obligation Disposition Manifest

- **Evidence:** a versioned manifest covering all predecessor repositories
  (sf0.8, product-a, sf0.7, sf0.5) listing every open issue with: repository,
  issue number, classification (migrated, completed, superseded, rejected,
  duplicate, retained-evidence), successor link, reason, and review date.
- **Owner:** founder (disposition is owner-reviewed, not automated).
- **Validation:** the cutover guard compares the manifest against live open
  issues and fails if any issue lacks a valid disposition, reason, successor,
  or retained-evidence reference.
- **Fail condition:** any open predecessor issue is not in the manifest, or any
  manifest entry lacks a required field.
- **Synchronization:** factory issue #16 must be closed with the manifest
  attached before predecessor freeze.

### Cutover Lifecycle Transaction

Predecessor freeze is a guarded atomic transaction, not a checklist item. The
following must all pass before sf0.8 is declared frozen:

1. Release distribution contract validated.
2. Apple acceptance receipts for both reference apps validated.
3. Qualification ledger validated.
4. Obligation disposition manifest validated.
5. Recovery rehearsal evidence validated.
6. Owner authorization recorded.
7. Successor notices published in sf0.8 README and repository description.
8. `portfolio.yaml` updated to name `edoworks/factory` as the active factory.
9. Continuation command updated to reflect cutover completion.
10. Factory issues #10, #11, #15, and #16 verified closed via the
    issue-closeout guard.

The cutover guard must reject freeze if any step is missing, incomplete, or
contradicted by another system's state.

## Predecessor Disposition

sf0.8 is frozen and superseded — not archived — until the new factory proves:

1. Two Apple-accepted reference apps (Apple Acceptance Receipt validated)
2. Recovery from factory failure rehearsed (recovery evidence committed)
3. Every open sf0.8 issue dispositioned with successor links (Obligation
   Disposition Manifest validated)
4. All obligations tracked to a successor (manifest covers all predecessor
   repositories)

Only then are sf0.8 and predecessors archived (read-only, never deleted).