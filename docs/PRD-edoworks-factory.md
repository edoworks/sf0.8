# Edoworks Factory PRD

Date: 2026-09-20
Updated: 2026-09-24
Status: ACTIVE
Owner: founder (customer zero)
Parent research: [Edoworks Canonical Factory Deep Dive](research/edoworks-canonical-factory-deep-dive-2026-09-20.md)

## Product Premise

Edoworks Factory is a public, versioned, MIT-licensed software factory that
produces offline-first iOS/iPadOS apps through a deterministic paved road. The
founder is customer zero. The factory is downloaded from the generated source
archive for an exact release tag, used to scaffold and verify an app, and
produces human-gated release candidates for Apple App Store submission.

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

### Storage Envelope Law

Every disk-expensive operation declares its expected peak, maximum peak, and
maximum persistent growth before execution. Admission is based on measured
available space minus active reservations and a configured recovery floor.
Routine successful work approaches zero persistent growth unless it promotes a
named artifact with an owner and retention policy. Low-storage failures are not
retried until capacity is re-established. Automatic cleanup is limited to the
exact factory-owned reproducible or temporary paths recorded by the job; source,
uncommitted work, promoted artifacts, pinned resources, and global developer
state are never inferred to be disposable.

### Identity Governance Law

The canonical identity registry governs legal identity, brands, product names,
trademark posture, domains, contacts, and address handling while the portfolio
remains lifecycle authority. Unresolved clearance blocks adoption. Domain
ownership, prior use, filing, development, publication, or other sunk cost does
not establish clearance or authorize additional trademark or domain spend.
Private domicile values are prohibited from repository records.

## Paved Road

The factory's public API is one opinionated journey:

```
download release → doctor → init app repo → confirm PRD →
implement bounded increment → deterministic verify →
release evidence → human-authorized Apple submission
```

### Lifecycle Scripts

- `doctor.sh` — verify Xcode, simulators, storage admission, and dependencies
- `bootstrap.sh` — scaffold a new app from the factory template
- `verify.sh` — reserve storage, run build, tests, analysis, and an optional
  retained archive in factory-scoped paths, then emit a storage receipt
- `uninstall.sh` — remove factory and residual state

### What the Factory Includes

- Apple distribution capability registry and validator
- Canonical identity registry and portfolio-consistency validator
- Privacy manifest template (`PrivacyInfo.xcprivacy`)
- Release-criteria schema and evidence generator
- Recovery knowledge boundary and failure classifier
- CI policy gate (deterministic verification)
- SLSA-style provenance template for release artifacts
- Compatibility matrix (supported macOS + Xcode versions)
- Storage admission, reservation, and per-run lifecycle receipts
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
| Successful-run persistent disk growth | Zero except named retained artifacts |
| Storage attribution | 100% of retained job output has owner and retention |

## Versioning

- `v0.1.0` — Initial release: paved road, lifecycle scripts, simpler utility
  template
- `v0.1.x` — Corrections discovered during Reference App 1 qualification
- `v0.2.0` — Post-qualification hardened release (after 30-day test passes)
- `v0.3.0` — Meow-capture capability (microphone, SoundAnalysis, audio clip
  management)
- `v1.0.0` — Stable public compatibility contract (only after second
  independent consumer and paid pilot)

Every factory correction is a new tagged version. The reference app records the
exact tag and source revision and upgrades explicitly. Release records state
whether they are prereleases, immutable, and accompanied by attached assets;
those properties are not inferred from a version tag.

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
| Trademark or domain spend/transaction | Human only |
| Customer engagement | Human only |

## Evidence Contracts And Cutover Guards

Each gate below defines its evidence artifact, owner, validation command, fail
condition, and cross-system synchronization requirement. A gate is not closed
until its validation command passes and its evidence artifact is committed.

### Release Distribution Contract

- **Evidence:** a release receipt recording tag, source revision, distribution
  URL, prerelease flag, immutability flag, attached asset inventory, available
  asset digests, and README install-path verification.
- **Owner:** founder (release publication is human-authorized).
- **Validation:** a CI release-contract test resolves the documented download
  URL, verifies the tag's source revision, compares prerelease/immutability
  state and attached assets with the documentation, and verifies digests for
  any assets whose release records provide them.
- **Fail condition:** the documented URL is unavailable, the tag moves from the
  recorded source revision, a documented asset is absent, a provided digest
  does not match, or the release is marked prerelease when a stable release is
  required for cutover.
- **Synchronization:** README, release record, source revision, asset inventory,
  and CI test must agree. An assetless generated source archive must be named as
  such rather than described as an attached release artifact.

### Apple Acceptance Receipt

- **Evidence:** one typed receipt recording the clean subject revision, the
  later evidence revision that commits the receipt, app
  bundle ID, version, build number, archive and exported-artifact digests,
  effective archived `Info.plist`, authorization reference, operation,
  operator, timestamp, Apple delivery/build/group identifiers, processing
  state, review disposition, acceptance date, and sanitized feedback location
  or `NO_DURABLE_FEEDBACK`.
- **Owner:** founder (submission is human-authorized).
- **Validation:** the cutover guard verifies the receipt is tracked at its
  evidence revision, binds its artifacts to the subject revision, is internally
  consistent, and records acceptance by Apple.
  TestFlight or simulator evidence does not satisfy this gate.
- **Fail condition:** no acceptance receipt exists, or the receipt records a
  status short of Apple acceptance, references dirty/untracked input, or lacks
  provenance for an external operation.
- **Synchronization:** factory issue #10 (and #14 for Reference App 2) must be
  closed with the receipt attached before predecessor freeze can proceed.

Apple lifecycle states are distinct:

```
ARCHIVED -> UPLOADED -> PROCESSED -> TESTFLIGHT_ACTIVE ->
SUBMITTED_FOR_REVIEW -> ACCEPTED
```

Each receipt retains transition history with state-specific timestamps and may
record terminal `REJECTED`, `DEVELOPER_REJECTED`, or `WITHDRAWN` outcomes.
TestFlight activation is required by this factory's release ladder before App
Review submission even though the external API may permit other paths. No state
implies a later state. A worktree plist change does not alter an
uploaded build; validators inspect the effective plist inside the exact signed
archive or exported artifact named by the receipt. App Store Connect platform
messages (for example export-compliance guidance) are not tester feedback.
Absence of durable tester feedback is recorded as `NO_DURABLE_FEEDBACK`, never
as "no issues found." Raw private tester identities and comments are not placed
in public evidence; durable records contain sanitized findings and provenance.
Receipts live at
`.factory/artifacts/evidence/apple/<bundle>-<version>-<build>.json` and are
validated by `python3 scripts/validate-apple-receipt.py RECEIPT` once the
validator lands under the implementation issue.

### Claim-To-Evidence Contract

- Every normative PRD requirement maps to a direct assertion, measured result,
  authenticated external receipt, explicit human observation, or `NOT_RUN`.
- A test name, PR title, prose summary, source inspection, screenshot capture,
  or passing count does not prove behavior that the underlying assertion does
  not inspect.
- Every `PASS` records the source revision, mode, destination, command,
  timestamp, result artifact, and direct pass condition.
- Evidence referenced by a gate must be tracked at its evidence revision and
  bind the tested artifact to its subject revision. Dirty or untracked evidence
  cannot close a gate.
- Conflicting lifecycle, control-plane, queue, ledger, evidence, or continuation
  records fail closed until reconciled against the canonical receipt.
- `.factory/continuation-state.json` is the canonical portable continuation
  record. Human-readable continuation commands are projections and CI validates
  the checked-in projection rather than machine-local configuration.
- Evidence revisions resolve through Git object lookup. A path being tracked in
  the current worktree does not prove it existed at the cited revision.
- Remote issue and repository state is consumed through a timestamped snapshot
  with a declared maximum age. A remotely closed issue and valid closure
  evidence are separate conditions; either can block effective completion.

### Repository Metadata Contract

- Canonical lifecycle state is bound to the exact public repository description,
  homepage, archive state, visibility, license, default branch, and supported
  release properties that users can observe.
- Source-only changes do not satisfy a live metadata requirement. Repository
  fields and merged default-branch content must independently match the contract.
- An incomplete contract names every observed blocker exactly. Completion clears
  the blocker set and passes the authenticated contract without a declared-
  blocker allowance.
- Public repository-page validation includes a rendered visual check that active,
  deprecated, archived, and successor language is visible and unambiguous. A
  screenshot does not substitute for live metadata or source verification.

### Verification Outcome Contract

Verification reports one of: `PASSED`, `FAILED`,
`COMMAND_TIMEOUT_PROGRESSING`, `COMMAND_TIMEOUT_NO_PROGRESS`,
`TEST_HANG_CONFIRMED`, `INFRASTRUCTURE_ERROR`, or `INCOMPLETE_NO_RESULT`.
A command timeout alone is not a test failure or confirmed hang.
`COMMAND_TIMEOUT_NO_PROGRESS` means no test event or output occurred within the
configured inactivity threshold, which is recorded in the receipt.
`TEST_HANG_CONFIRMED` additionally requires two process samples across that
threshold showing the same active test and no output, result-bundle, or process
progress. Receipts record start time, last-progress time, current test,
completed count, exit status, threshold, process samples, and result-bundle
path. Retries are bounded and preserve the first attempt's evidence.
Every durable timeout-classification receipt under
`.factory/artifacts/evidence/verification-receipts/` is validated by CI. In the
absence of a compliant receipt, historical timeout prose remains `UNKNOWN`.

### Storage Lifecycle Contract

- **Evidence:** every `doctor` and `verify` receipt records filesystem capacity,
  starting and ending available bytes, required bytes, recovery-floor bytes,
  active reservation bytes, this job's reservation, run-owned paths, cleanup
  outcome, retained artifacts, and any unknown persistent growth. Verification
  additionally records minimum available space and peak consumption when the
  platform can measure them reliably.
- **Owner:** the creating job owns temporary and reproducible paths until it
  completes; a product or release owner must explicitly accept promoted
  artifacts. External stores such as global Xcode state, OpenCode history,
  model caches, Docker, and virtual machines remain external owners and are
  inventory-only until an owner-specific retention policy exists.
- **Admission:** a disk-expensive job acquires an atomic lease before creating
  expensive state. Available bytes minus live reservations and the configured
  recovery floor must cover its declared maximum peak. Unknown expensive jobs
  fail closed; read-only diagnosis remains available.
- **Concurrency:** reservation creation is serialized. Leases bind job identity,
  process identity, boot identity, owned roots, creation time, and expiry.
  Cleanup cannot target a resource with a live lease.
- **Success:** run-owned reproducible and temporary paths are retired, selected
  artifacts are promoted explicitly, and unexplained persistent growth above a
  declared measurement tolerance fails the receipt. The tolerance is reported,
  calibrated from observed shared-filesystem drift, and never subtracted from
  measured growth.
- **Failure:** run-owned state is preserved at a reported path for a bounded
  diagnostic period. A low-space failure is non-retryable until a later
  preflight proves sufficient unreserved capacity.
- **Crash recovery:** startup or the next preflight reconciles expired leases.
  Orphaned resources are quarantined before any owner-specific, idempotent
  cleanup. Correctness must not depend only on an EXIT trap.
- **Thresholds:** absolute recovery floors and workload maxima are calibrated
  from measured representative runs. Percentage free is advisory and cannot
  replace the absolute completion envelope. The historical 5 GB and current
  10 GB checks are not treated as validated universal limits.
- **Fail condition:** verification starts without a reservation, active jobs can
  overcommit capacity, cleanup escapes a recorded owned root, retained growth
  lacks an owner, or a storage receipt omits required measurements.
- **Implementation:** `edoworks/factory` issue #60 owns the initial
  non-destructive governor increment. A background daemon and global cache
  migration remain out of scope until simpler preflight reconciliation proves
  insufficient.

### Integrated Completion Contract

Non-trivial work starts from a canonical issue and a dedicated feature branch.
Implementation is complete only after review of the final diff, applicable
verification, commit, identity-verified push, pull request, checks, merge,
verification of the merged target revision, and safe feature-branch cleanup.
Before waiting on a self-hosted check, completion procedure verifies that the
repository-scoped service and listener are active. A zero-step queued job with
an unavailable runner is a blocker, not normal CI latency; readiness must fail
fast rather than consume the general check timeout.
CI observation is state-aware: report transitions among queued, active step, and
terminal states; distinguish expected long-running work from no-progress; and
apply explicit queue, step-progress, and overall deadlines. Long blocking
`gh ... --watch` calls are not completion evidence because they hide state and
delay diagnosis.
Dirty or untracked implementation/evidence blocks integrated-complete status.
Notifications distinguish a completed audit or local preparation from an
integrated repository change. A material defect, blocker, trust gap, or
recurring workflow failure also requires an evidence-backed root-cause record
and a verified mechanical recurrence guard before closure.

### 2026-09-22 Evidence-Integrity 5-Whys

1. Completion claims were unreliable because prose, test names, and passing
   counts were treated as proof of the behavior they named.
2. Green tests did not establish PRD compliance because requirements were not
   mapped to direct positive and negative assertions.
3. Release state drifted because app evidence, factory evidence, queues,
   ledgers, and continuation files represented it independently.
4. Drift persisted because no typed receipt reconciled source, artifact,
   authorization, external operation, feedback, and resulting state.
5. The root cause was a completion model that rewarded artifact existence and
   command success without enforcing semantic coverage and provenance.

The immediate correction is to downgrade unsupported claims and repair the
known product/test defects. The root correction is the claim-to-evidence
contract and canonical lifecycle receipt above. The recurrence guards are the
tracked-evidence, state-reconciliation, timeout-classification, and integrated-
completion checks specified here and implemented under factory map issue #42.

### Qualification Ledger

- **Evidence:** a version-pinned ledger recording daily receipts for the
  qualification period: date, change description, unattended success flag,
  manual repair flag, failure classification, operator identity, denominator,
  and cumulative success rate.
- **Owner:** founder (qualification execution is owner-authorized).
- **Validation:** the promotion guard verifies a 30-calendar-day observation
  window containing qualifying changes on at least 10 consecutive weekdays,
  cumulative unattended success rate >= 95%, at least one second-operator run,
  and a complete failure taxonomy.
- **Calendar validation:** weekday names are derived from ISO dates; inconsistent
  names, duplicate dates, or invalid business-day sequences fail validation.
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
