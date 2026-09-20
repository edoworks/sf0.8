#!/usr/bin/env bash
set -euo pipefail

# Edoworks Factory — repo, labels, and issues creation script
# Run this once after owner approval.
# Prerequisites: gh CLI authenticated as hellofoculoom

set -x

# 1. Verify identity
gh api user --jq .login

# 2. Create the public repo (skip if it already exists)
if ! gh repo view edoworks/factory >/dev/null 2>&1; then
  gh repo create edoworks/factory --public \
    --description "A public, versioned, MIT-licensed software factory for producing offline-first iOS/iPadOS apps through a deterministic paved road."
else
  echo "Repo edoworks/factory already exists, skipping creation."
fi

# 3. Create labels
LABELS=(
  "phase-0:0e8a16:Owner charter and decisions"
  "phase-1:1d76db:Factory skeleton v0.1.0"
  "phase-2:5319e7:Reference app 1 simpler offline utility"
  "phase-3:bfd4f2:Factory hardening and 30-day qualification"
  "phase-4:fbca04:Reference app 2 meow-capture"
  "phase-5:c5def5:Predecessor disposition and archival"
  "factory:a2eeef:Factory infrastructure or tooling"
  "product:a2eeef:Product or app feature"
  "gate:e99695:Release gate or qualification milestone"
  "owner-only:b60205:Requires human or owner authorization"
  "documentation:0075ca:Improvements or additions to documentation"
  "enhancement:a2eeef:New feature or request"
  "bug:d73a4a:Something isn't working"
)

for label in "${LABELS[@]}"; do
  IFS=':' read -r name color desc <<< "$label"
  gh label create "$name" --color "$color" --description "$desc" --repo edoworks/factory --force
done

# 4. Create issues
# Each issue is created with --body-file pointing to a temp file

create_issue() {
  local title="$1"
  local labels="$2"
  local body="$3"
  # Skip if an issue with the same title already exists
  local existing
  existing=$(gh issue list --repo edoworks/factory --state open --search "in:title ${title}" --json number --jq 'length' 2>/dev/null || echo "0")
  if [ "$existing" != "0" ]; then
    echo "Issue already exists, skipping: $title"
    return 0
  fi
  local tmpfile
  tmpfile=$(mktemp)
  printf '%s\n' "$body" > "$tmpfile"
  gh issue create --repo edoworks/factory --title "$title" --label "$labels" --body-file "$tmpfile"
  rm -f "$tmpfile"
}

# F-001
create_issue "Record owner charter and reconcile naming" "phase-0,owner-only,documentation" "Record the Edoworks Factory charter that supersedes sf0.8's canonical priority.

Deliverables:
- CHARTER.md with: one customer (founder as customer zero), one Apple-app paved road, non-goals, public API definition, success metrics, authority boundaries
- Naming reconciliation: resolve edoworks/edoworks collision (repo = edoworks/factory), CLI/package name, constitution branding inconsistency (FACTORY_CONSTITUTION.md:29 says Foculoom vs NORTH_STAR.md:1 says edoworks.ai)
- Explicit meow-capture lane decision: preserved as second reference app, not abandoned
- Supported macOS + Xcode version matrix
- Agent/provider dependencies for the public factory
- Support promise + telemetry posture
- Trademark policy for edoworks brand

Gate: Owner signs off on charter. No code is written.

Reference: docs/PRD-edoworks-factory.md"

# F-002
create_issue "Create edoworks/factory public repo with MIT license" "phase-1,factory,owner-only" "Create the fresh public repository with minimal scaffolding.

Deliverables:
- Public repo edoworks/factory (fresh, not a fork of sf0.8)
- LICENSE (MIT)
- README.md (what it is, how to install, what it produces)
- SECURITY.md (public security posture and contact)
- CONTRIBUTING.md (support boundaries, contribution policy)
- .gitignore for Swift/Xcode/Python
- Default branch: main

No sf0.8 history or private control-plane data is published.

Gate: Repo exists and is publicly cloneable."

# F-003
create_issue "Port allowlisted factory components from sf0.8" "phase-1,factory" "Extract provenance-reviewed components from sf0.8 into edoworks/factory. No private history, no control-plane data, no secrets.

Components to port:
- Apple distribution capability registry + validator (scripts/validate-apple-distribution.py, schema files)
- Privacy manifest template (PrivacyInfo.xcprivacy pattern from product-a)
- Release-criteria schema (.factory/automation/release-criteria.json)
- Recovery knowledge boundary pattern (.factory/recovery/)
- CI policy gate subset (.github/workflows/checks.yml validation steps)
- Apple quality review script (scripts/apple-quality.py)

Each extraction must have:
- Provenance manifest (source file, source commit, license clearance)
- No references to private repos, private products, or internal-only paths
- Tests ported alongside

Gate: All ported scripts pass on clean checkout."

# F-004
create_issue "Implement lifecycle scripts: doctor, bootstrap, verify, uninstall" "phase-1,factory" "Create the paved-road lifecycle scripts.

- doctor.sh: verify Xcode version, simulators, disk space, dependencies; report pass/fail per check
- bootstrap.sh: scaffold a new iOS app from the factory template (SwiftUI universal, iPhone+iPad)
- verify.sh: run build, unit tests, UI tests, static analysis, archive; produce machine-readable evidence
- uninstall.sh: remove factory and residual local state

Each script must:
- Exit non-zero on failure with machine-readable error code
- Produce evidence receipt (JSON) on success
- Have no hidden local state dependency
- Work on a clean Mac with only Xcode installed

Gate: doctor.sh passes on a clean Mac."

# F-005
create_issue "Create SwiftUI universal app template" "phase-1,factory" "Create the opinionated SwiftUI universal-app template that bootstrap.sh uses.

Template includes:
- SwiftUI @main App with NavigationStack
- Adaptive iPhone+iPad layouts (not separate branches)
- Local persistence (UserDefaults/SwiftData)
- Import/export capability
- Deliberate states: first-launch, content, empty, error
- PrivacyInfo.xcprivacy (no tracking, no collected data)
- Unit test target with example tests
- UI test target with example XCUITests
- Accessibility labels and traits on all interactive elements
- xcodegen project.yml (pinned, reproducible)

No microphone, backend, accounts, analytics, or payment.

Gate: Template builds and tests pass on simulator for iPhone and iPad."

# F-006
create_issue "Implement CI policy gate for edoworks/factory" "phase-1,factory" "Create .github/workflows/checks.yml for deterministic verification CI.

Steps:
- Run doctor.sh
- Run verify.sh on the template app
- Run ported validators (validate-apple-distribution, validate-lifecycle, validate-recovery)
- Run ported unit tests (Python policy tests)
- Run safety-kernel verification if applicable
- Produce machine-readable evidence artifact

Use ephemeral GitHub-hosted macOS runner (not self-hosted) for public reproducibility.

Gate: CI passes on a clean PR."

# F-007
create_issue "Release v0.1.0-rc1 with immutable artifact and provenance" "phase-1,factory,gate" "Cut the first release candidate.

Deliverables:
- Tag v0.1.0-rc1 (immutable)
- GitHub release with artifact + SLSA-style provenance/digest
- CHANGELOG.md entry
- compatibility-matrix.md (supported macOS + Xcode versions)
- public-api.md (the paved-road contract)
- Clean-machine install receipt (evidence that doctor.sh passes on a fresh Mac)

Gate: Clean-machine install from downloaded artifact succeeds without source-tree access."

# F-008
create_issue "Select and define Reference App 1 (simpler offline utility)" "phase-2,product,owner-only" "Owner selects the specific offline utility concept for Reference App 1.

Constraints:
- Offline-only, no network, no accounts, no special permissions
- iPhone + iPad adaptive layouts
- Meaningful enough to not be a spam/template app
- Owner-visible value (founder would actually use it)

Deliverables:
- PRD for the reference app (features, acceptance criteria, App Review readiness)
- Separate repository created (edoworks/<app-name>) pinned to factory v0.1.0-rc1

Gate: Owner approves PRD and app concept."

# F-009
create_issue "Build Reference App 1 using downloaded factory v0.1.0" "phase-2,product" "Build the simpler offline utility using only the downloaded factory release (not the source checkout).

Process:
1. Download v0.1.0-rc1 artifact
2. Run doctor.sh
3. Run bootstrap.sh to scaffold
4. Implement features per PRD
5. Run verify.sh for each increment
6. Produce distribution-signed archive

Every factory correction discovered during this phase ships as a new factory version (v0.1.1, v0.1.2, etc.). The app upgrades explicitly.

Gate: App builds and tests pass from clean checkout."

# F-010
create_issue "Reference App 1: Apple submission and acceptance" "phase-2,product,gate,owner-only" "Complete the full release ladder for Reference App 1.

Gates (each must pass):
1. Clean build + tests pass
2. Simulator evidence on iPhone + iPad
3. Accessibility audit (VoiceOver + Reduce Motion)
4. Privacy manifest validation
5. Distribution archive produced through factory
6. Human-authorized TestFlight upload
7. Apple processing succeeds
8. Physical-device smoke test
9. Recovery test (deliberately break and restore)
10. Human-authorized App Store submission
11. Apple accepts

Must complete two full clean-checkout-to-Apple-processing cycles.

Gate: Apple accepts Reference App 1."

# F-011
create_issue "30-day factory qualification" "phase-3,factory,gate" "Run the 30-day qualification to prove factory reliability.

Requirements:
- 10 consecutive weekday changes producing reproducible archives
- >=95% unattended run success without manual repair
- Machine-readable failure classification and recovery for every failure
- No hidden local state dependency
- Second-operator documented execution (no oral help)
- Measure: lead time, operator effort, escaped defects, storage growth, failure causes
- Move routine builds to ephemeral CI
- Credential isolation: per-customer, least-privilege API keys

Gate: 30-day qualification passes with evidence. Factory bumped to v0.2.0."

# F-012
create_issue "Authorize meow-capture public identity and physical-device validation" "phase-4,product,owner-only" "Owner-gated prerequisites for Reference App 2.

Decisions required:
- Authorize a public product name (meow-capture is a codename)
- Authorize physical-device validation session
- Authorize first real-meow fixture
- Decide whether Apple Intelligence is included or excluded
- Confirm export-compliance answer for Sound Analysis encryption

Reference: docs/decisions/2026-09-20-meow-capture-product-contract.md

Gate: Owner authorizes each item."

# F-013
create_issue "Build Reference App 2 (meow-capture) using factory v0.2.0" "phase-4,product" "Build meow-capture using the hardened factory release.

Reuses from sf0.8 (allowlisted, provenance-reviewed):
- experiments/audio-validation-macos/ AudioReplayCore (iOS-declared)
- experiments/continuous-competence-ios/ SwiftUI spike
- 2026-09-20-meow-capture-product-contract.md acceptance contract

Acceptance contract:
- Owner-started bounded listening session with visible mic indicator
- Production pipeline identifies likely cat vocalization, retains bounded clip
- Local replay of exact retained clip
- Local deletion of clip
- Explicit stop or time bound
- Deliberate states on iPhone and iPad
- Raw household audio stays local (never in Git, CI, logs, issues)
- No fake classifier result; no translation/emotion/health/veterinary claim
- Microphone permission OS-mediated, fails closed

Gate: App builds and tests pass from clean checkout."

# F-014
create_issue "Reference App 2: Apple submission and acceptance" "phase-4,product,gate,owner-only" "Complete the full release ladder for meow-capture.

Gates (same as F-010 plus):
- Mac fixture replay via AudioReplayCore
- Physical iPhone + iPad permission/interruption/persistence evidence
- Owner-supervised real-cat observation (separately gated)
- NSMicrophoneUsageDescription purpose string
- Export-compliance for Sound Analysis encryption
- Age rating determination
- Apple Intelligence fallback evidence if used
- Human-authorized App Store submission
- Apple accepts

Gate: Apple accepts meow-capture. This establishes founder-internal canonicality."

# F-015
create_issue "Freeze sf0.8 and publish successor notices" "phase-5,factory,owner-only" "Begin predecessor disposition after both reference apps are Apple-accepted.

Prerequisites (all must be met):
- Edoworks factory has produced two Apple-accepted apps
- Recovery from factory failure rehearsed

Actions:
- Freeze sf0.8 (read-only, no new work)
- Publish successor notices in sf0.8 README and key docs
- Update continue-sf08.md to point at edoworks/factory

Gate: sf0.8 frozen with successor notices published."

# F-016
create_issue "Disposition all open sf0.8 issues with successor links" "phase-5,factory" "Classify every open issue across sf0.8, product-a, sf0.7, sf0.5.

Dispositions: migrated / completed / superseded / rejected / duplicate / retained-evidence

Each issue must have:
- A disposition label
- A successor link (to edoworks/factory issue or explicit retained-evidence note)
- A reason

No blanket closure. Every obligation must be tracked to a successor.

Gate: Zero open issues without a disposition."

# F-017
create_issue "Archive predecessor repositories after recovery proof" "phase-5,factory,owner-only,gate" "Archive repositories only after all prerequisites are met.

Prerequisites:
- F-015 complete (sf0.8 frozen)
- F-016 complete (all issues dispositioned)
- Recovery proof verified (can restore from archive if needed)
- Preservation manifest for portfolio-archaeology/ complete
- All security, legal, privacy, retention obligations tracked to successor

Actions:
- Archive repositories (read-only, never delete)
- Verify archival did not destroy data

Gate: All predecessors archived. Recovery verified post-archive."

# F-018
create_issue "Productization gate: assess paid pilot readiness" "gate,owner-only" "Future gate. Do not start until F-014 is complete.

Conditions for proceeding:
- At least one paying external design partner
- Repeat customer demand (renewal or second app)
- Sustainable support economics measured
- Tenant isolation demonstrated
- Second independent consumer creates+verifies an app from released artifact without private founder knowledge
- No template/spam/privacy/metadata/minimum-functionality objections from Apple

If conditions fail: Continue as bespoke managed development service.
If conditions pass: Bump to v1.0.0 with stable public compatibility contract.

Gate: Owner decision recorded."

set +x
echo "=== Done. Repo, labels, and 18 issues created in edoworks/factory ==="