# Software Engineering Practice Question Set

Date: 2026-09-20
Audience: software engineers refreshing day-to-day engineering judgment

## Coverage

Both the mobile web and native iOS banks now include reference-backed questions
on:

- testing boundaries, failure contracts, regressions, and integration seams;
- observability, diagnostic context, redaction, and actionable signals;
- secret handling, least privilege, runtime injection, scanning, and rotation;
- API compatibility, independent deployment, migration, and deprecation.

Each question includes four visible contract cases, progressive hints, an
explanation, and a reference. The cases reinforce practices without claiming
that passing a case establishes production readiness.

The mobile surface now also exposes a local learning library before session
start, with common questions, text-based visual walkthroughs, and source links;
the native iOS surface provides the corresponding concept library.

## Cache Recurrence Analysis

Visual verification initially showed the previous start screen because the
service worker cache key remained at `v1` after the UI changed. The immediate
correction was to bump the cache key to `v2`. The root cause was treating the
offline asset cache as static while changing the application bundle. The
recurrence guard is a required cache-version change for future asset revisions,
plus a rendered screenshot check after UI changes.

## Evidence Boundary

The question content is a learning aid, not a substitute for a team’s coding
standards, threat model, incident process, or platform documentation. Vendor and
framework behavior should be checked against the version actually deployed.

## Recurrence Guard

The mobile contract tests require at least four software-practice questions with
references and four cases each. Native tests require the same practice IDs to be
present in the iOS bank. Future question additions should preserve a failure or
boundary case and a source link.
