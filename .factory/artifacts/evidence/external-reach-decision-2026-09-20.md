# External Reach And Verified Use Decision

Status: `IMPLEMENTED_AND_VALIDATED`
Issue: `71`

## Decision

Downloads are reach signals only. They do not establish identity, execution,
usage, retention, economic value, or payment. Verified external use requires a
non-founder, consented workflow report tied to an immutable artifact revision
and containing the actual workflow and job to be done.

## Factory Changes

- Added `reach_signals` to the primitive inventory, separate from the five
  market-evidence levels.
- Added `scripts/validate-primitive-reach.py` for local validation and explicit
  optional output.
- Added `apply_reach_signal` for dry-run-safe inventory updates.
- Added duplicate, unknown-primitive, founder, automated, unconsented, and
  download-claims-execution guards.

## Evidence Boundary

`DOWNLOAD` records remain reach-only. `VERIFIED_EXECUTION` can update usage and
external-use evidence only when the report is non-founder, explicitly opted in,
revision-linked, and workflow-specific. It does not update retention,
economic, or payment evidence.

No downloader identity is inferred from IP data or automation patterns. No
telemetry, outreach, publication, release, or external mutation was performed.

## Current State

No verified external-use signal is currently recorded. ReuseFirst remains
technically released with internal/product Customer Zero evidence, but no
independent external use or payment evidence is claimed. Broader artifact
collection publication remains human-authorized and deferred.

## Falsifiable Test

For one immutable artifact revision, a consented non-founder must provide a
clean-checkout execution or reproducible workflow report tied to that revision.
If downloads occur without that evidence during the declared test window, the
claim that downloads demonstrate external use is rejected.
