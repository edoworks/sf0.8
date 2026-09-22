# Cutover Blocker Rubberduck Review

Date: 2026-09-22
Subject: why `docs/PRD-edoworks-factory.md` was not sufficient to prevent the
cutover blockers for `edoworks/factory`, and what must change so a new session
does not repeat the same errors.
Mode: brutally honest review, not a summary.

## Brutally Honest Summary

The PRD is a strong product charter and a weak operational contract. It
correctly named every gate that now blocks cutover — Apple acceptance, 30-day
qualification, recovery, predecessor freeze, obligation disposition — but it
left the evidence, state-transition, and enforcement machinery unspecified. The
result was foreseeable: sessions treated named gates as narrative milestones
rather than fail-closed checks, and the factory reached a prerelease state
where the public download path returned 404 while the team believed the release
was verified.

This is not a case of the PRD being wrong about what matters. It is a case of
the PRD describing outcomes without defining the proof, owner, command, and
machine-checkable completion condition for each outcome. That gap allowed five
distinct blockers to accumulate without triggering any alarm until an external
review asked "is this ready to cutover?" and the answer was no on five
independent axes.

## What The PRD Got Right

- It named the correct gates: Apple acceptance, 30-day qualification, recovery
  rehearsal, issue disposition, obligation tracking, predecessor preservation.
- It defined human authority boundaries correctly: no autonomous publication,
  no credential use, no archive without human authorization.
- It specified the paved road and the clean-checkout law.
- It set semantic versioning and release-artifact pinning expectations.
- It set stop rules that would trigger re-scoping.

## What The PRD Failed To Prevent

### Blocker 1: Release/distribution contract gap

**What happened:** `v0.1.0-rc2` is a prerelease with zero uploaded assets.
The README advertised `releases/latest/download/factory.tar.gz`, which returns
404. The exact tag archive works, but the documented public install path does
not.

**Why the PRD did not prevent it:** The PRD says "downloaded as an immutable
release artifact" (line 12) and "every factory correction is a new immutable
version" (line 139), but it never defines:

- what the artifact IS (source archive, attached binary, tarball, installer)
- what immutability MEANS operationally (GitHub immutable release flag, digest
  publication, tag lock)
- what the verified install path IS (exact tag URL vs moving `latest` URL)
- what the release smoke test CHECKS (URL resolves, artifact downloads, digest
  matches, README path agrees with release record)
- who owns the release verification and what command they run

**5-Whys:**

1. Users could not use the documented path because it returned 404.
2. The prerelease had no asset at the moving `latest` URL.
3. Release verification tested the exact tag archive, not the README's public
   install command.
4. CI had no check binding release metadata, artifact availability, URL, and
   digest.
5. The PRD did not define one machine-checkable distribution contract.

**Recurrence guard:** A CI release-contract test must resolve the documented
URL, verify the expected artifact and digest, check prerelease/immutability
state, and reject any release whose README path is unavailable or whose
declared artifact does not match. This test must run against the live release
record, not just the local repository.

### Blocker 2: Issue #10 — Apple acceptance

**What happened:** Reference App 1 (NowNest) passed G8/TestFlight. G9
recovery, G10 submission, and G11 Apple acceptance remain unperformed. The
issue is open with no acceptance evidence.

**Why the PRD did not prevent it:** The PRD names Apple acceptance as a gate
(lines 95-111, 185-194) but never defines:

- what an acceptance receipt IS (Apple decision status, app version, build
  number, processing date, review disposition)
- what evidence package must be attached to close #10
- that #10 cannot close from TestFlight or simulator evidence alone
- the exact lifecycle: archive -> processing -> submission -> acceptance ->
  two clean cycles

**5-Whys:**

1. #10 is open because Apple submission/acceptance evidence is absent.
2. Evidence stops at TestFlight; human submission and Apple's decision are
   separate gates.
3. Those gates require owner authority and Apple's external process.
4. The PRD defines the gate but not the required acceptance receipt or
   closure-evidence package.
5. Cutover dependencies were not mechanically linked to an Apple-acceptance
   evidence record.

**Recurrence guard:** Define an Apple-acceptance evidence schema that
distinguishes archive, processed build, submitted version, and accepted
version. The cutover guard must reject predecessor freeze while #10 is open or
lacks a verifiable Apple decision artifact.

### Blocker 3: Issue #11 — 30-day qualification and independent evidence

**What happened:** No 30-day qualification run, no independent operator
evidence, no second-consumer evidence. The issue is open with no comments.

**Why the PRD did not prevent it:** The PRD specifies targets (lines 113-127):
>=95% unattended success, operator effort measured, escaped defects measured,
recovery rehearsed, second-operator execution. But it never defines:

- the qualification protocol (what constitutes a "weekday change," what
  denominator is used, what counts as unattended success vs manual repair)
- the evidence schema (daily receipt format, metrics fields, failure
  taxonomy)
- ownership (who runs it, who records it, who validates it)
- start and stop conditions
- what blocks promotion to v0.2.0 if qualification is incomplete

**5-Whys:**

1. No 30-day or independent operator/consumer result is evidenced.
2. No dated qualification run, receipt set, denominator, or independent
   execution record exists.
3. The PRD states targets but not the protocol, evidence schema, ownership,
   or start/stop conditions.
4. F-011 expands the requirements but remains an open issue without an
   attached qualification ledger.
5. Qualification criteria were tracked as planned work, not enforced as a
   state transition required for cutover.

**Recurrence guard:** Define qualification as a version-pinned evidence bundle
with explicit denominator, period, failure taxonomy, operator identity, and
consumer test protocol. The promotion guard must reject v0.2.0 and cutover
unless the validator confirms all required receipts and independent evidence.

### Blocker 4: Issue #15 — predecessor freeze

**What happened:** `sf0.8` is still named as the active factory in
`.factory/portfolio.yaml`. The continuation record describes active sf0.8
work. #15 is open. No freeze has been performed.

**Why the PRD did not prevent it:** The PRD says "sf0.8 is frozen and
superseded — not archived — until the new factory proves..." (lines 185-194),
but it never defines:

- what "frozen" means operationally (read-only, no new PRs, no new issues,
  branch protection, successor notice in README)
- what the freeze receipt IS (who authorizes it, what file records it, what
  state transition marks it)
- that portfolio.yaml, continuation command, and GitHub state must all agree
  before freeze is declared
- the atomic transaction: prerequisite evidence -> owner authorization ->
  successor notice -> state update -> verification

**5-Whys:**

1. sf0.8 was not frozen because #15 is open and local authority still says
   it is active.
2. Its prerequisites — two Apple acceptances, recovery rehearsal, issue
   disposition — are not evidenced.
3. Freeze requires owner-controlled lifecycle and documentation changes.
4. The PRD states the prerequisite order but not the transactional lifecycle
   transition or signed freeze receipt.
5. No mechanical guard synchronizes the PRD, local portfolio, continuation
   state, and remote issue before declaring cutover.

**Recurrence guard:** Model cutover as a lifecycle transaction. The freeze
guard must reject predecessor-freeze/archive unless #10, #11, recovery, and
#16 are verified complete, and must verify that portfolio.yaml, continuation
command, and GitHub issue state all agree.

### Blocker 5: Issue #16 — predecessor obligation disposition

**What happened:** No disposition manifest exists. "Every open sf0.8 issue"
was never inventoried. Open issues across sf0.8, product-a, sf0.7, and sf0.5
have no classification, successor link, or reason.

**Why the PRD did not prevent it:** The PRD says "every open sf0.8 issue
dispositioned with successor links" and "all obligations tracked to a
successor" (lines 191-193), but it never defines:

- the issue universe (which repositories, which issue trackers, what
  non-issue obligations exist)
- the disposition schema (classification values, required fields per issue)
- the manifest format (file path, version, owner, validation command)
- who performs the inventory and who validates it
- what blocks cutover if any issue lacks a valid disposition

**5-Whys:**

1. Open predecessor obligations lack demonstrated dispositions.
2. No cross-repository inventory or machine-readable disposition manifest
   exists.
3. The PRD says "every issue" and "all obligations" but does not define the
   issue universe, schema, owner, or reconciliation procedure.
4. F-016 exists as a tracker item but has no attached evidence or completion
   guard.
5. Cutover was not coupled to an obligation ledger that could fail closed on
   undispositioned work.

**Recurrence guard:** Maintain a versioned obligation/disposition manifest
covering all predecessor repositories. The cutover guard must compare the
manifest against live open issues and fail if any issue lacks a valid
disposition, reason, successor, or retained-evidence reference.

## Cross-Cutting Root Cause

The PRD specified **what must eventually be true**, but not:

1. **Canonical evidence schemas** — no receipt format for any gate
2. **Evidence ownership** — no named owner or command for each gate
3. **Version-pinned ledgers** — no qualification log, no obligation manifest
4. **Atomic state transitions** — no transactional cutover model
5. **Fail-closed guards** — no CI check or validator that rejects incomplete
   gates
6. **Cross-system synchronization** — no requirement that PRD, portfolio,
   continuation, and GitHub agree before declaring state

The issue definitions (F-007 through F-016) improved specificity but remained
plans rather than enforced evidence gates. The clean-runner incident
(2026-09-20) and the open-issue-closeout incident (2026-09-22) both
documented the same pattern: verification checked the wrong thing or did not
check at all, and no guard failed.

## What Must Change Before A New Session

### PRD amendments (this session)

Add a new section: **Evidence Contracts and Cutover Guards**. This section
must define, for each gate:

- the evidence artifact (schema, file path, required fields)
- the owner (who produces it, who validates it)
- the validation command (what mechanical check confirms it)
- the fail condition (what state rejects cutover or promotion)
- the cross-system synchronization requirement

### Process changes

1. **Release contract test:** CI must resolve the documented download URL,
   verify artifact and digest, check prerelease/immutability state, and reject
   mismatch. This test must run against the live release record.
2. **Apple-acceptance receipt:** Define a schema distinguishing archive,
   processed build, submitted version, and accepted version. The cutover
   guard rejects predecessor freeze without it.
3. **Qualification ledger:** Define a version-pinned evidence bundle with
   daily receipts, denominator, failure taxonomy, operator identity, and
   consumer test protocol. The promotion guard rejects v0.2.0 without it.
4. **Cutover lifecycle transaction:** Model freeze as a guarded transaction:
   prerequisite evidence -> owner authorization -> successor notice ->
   portfolio update -> continuation update -> GitHub state verification.
5. **Obligation manifest:** Maintain a versioned manifest covering all
   predecessor repositories. The cutover guard fails on undispositioned work.
6. **Issue-closeout guard:** Already implemented
   (`~/.config/opencode/scripts/issue-closeout.mjs`). Must be run before
   reporting any tracked chunk complete.

### Continuation command updates

The continuation command must reflect:

- the five cutover blockers and their evidence-contract requirements
- the mandatory issue-closeout guard
- the release-contract test requirement
- the qualification-ledger requirement
- the obligation-manifest requirement
- the cross-system synchronization requirement
- the corrected cutover state: not ready, five gates open

## Confidence

- **HIGH:** The PRD named the correct gates but lacked executable evidence
  contracts.
- **HIGH:** The five blockers are genuine, not administrative noise.
- **HIGH:** The cross-cutting root cause is the absence of fail-closed
  evidence guards.
- **MEDIUM:** Some blockers (#10 Apple acceptance) are partly external and
  cannot be fully prevented by PRD changes alone; the PRD can only ensure
  they are tracked correctly and not bypassed.

## Sources

### Primary

- `/Users/hello/sf0.8/docs/PRD-edoworks-factory.md`, inspected 2026-09-22
- `/Users/hello/sf0.8/docs/research/edoworks-factory-release-deep-dive-2026-09-22.md`, inspected 2026-09-22
- `/Users/hello/sf0.8/docs/research/edoworks-canonical-factory-deep-dive-2026-09-20.md`, inspected 2026-09-22
- `/Users/hello/factory/docs/open-issue-queue-audit-2026-09-22.md`, inspected 2026-09-22
- `/Users/hello/factory/docs/incidents/2026-09-20-clean-runner-lifecycle-verification.md`, inspected 2026-09-22
- `/Users/hello/factory/docs/incidents/2026-09-22-open-issue-closeout.md`, inspected 2026-09-22
- `/Users/hello/sf0.8/.factory/edoworks-factory-issues.json`, inspected 2026-09-22
- `/Users/hello/sf0.8/.factory/portfolio.yaml`, inspected 2026-09-22
- `/Users/hello/.config/opencode/commands/continue-sf08.md`, inspected 2026-09-22

### Secondary

- `/Users/hello/sf0.8/docs/v0.1-retrospective.md`, inspected 2026-09-22
- `/Users/hello/sf0.8/.factory/artifacts/evidence/nownest-g8-visual-testflight-2026-09-21.json`, inspected 2026-09-22
- `/Users/hello/sf0.8/.factory/artifacts/evidence/nownest-validation-summary-2026-09-21.json`, inspected 2026-09-22

### Lead-Only

- Full prior session transcripts were unavailable; conclusions rely on
  repository artifacts, Git history, and verified GitHub records.