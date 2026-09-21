# Rendit Probe Dependency Blocker 5-Whys

Date: 2026-09-19
Issue: #67
Status: `BLOCKED_DEPENDENCY`

## Observed failure

The pinned clean Rendit worktree validated all recipes and passed 44 targeted
determinism, provenance, no-network, no-AI, and validation tests, but the
actual render command could not run because the pinned `resvg` binary was not
available.

## 5-Whys

1. **Why was the render not executed?** `scripts/rendit-render.sh` stopped at
   its required resvg binary check.
2. **Why was resvg unavailable?** The clean probe environment did not contain
   the pinned native renderer.
3. **Why was it not installed during the probe?** Issue #67 explicitly forbids
   dependency installation and the factory treats installation as human-only.
4. **Why does the workflow depend on that binary?** Rendit’s deterministic
   rendering contract includes a hash-pinned native renderer rather than a
   pure-Python fallback.
5. **Root cause:** The source revision and test environment were reproducible,
   but the required native capability was not provisioned. Evidence does not
   establish a Rendit source defect or market opportunity.

## Correction and recurrence guard

- Immediate correction: record `BLOCKED_DEPENDENCY`; do not claim rendered
  output, byte identity, or packaging readiness.
- Root-cause correction: create a separate human-authorized environment lane
  that supplies the exact pinned binary, without changing Rendit’s runtime or
  installing dependencies autonomously.
- Mechanical guard: preserve the preflight check in `rendit-render.sh`; the
  probe evidence requires explicit render, meta, and hash results before any
  deterministic-output claim.

## Evidence

- `.factory/artifacts/evidence/rendit-workflow-probe-2026-09-19.json`
- Pinned source revision: `b00549fcab43e9d3d1ee9ec3a0222ffb446807a5`
- `make validate`: 59 files passed.
- Selected pytest run: 44 tests passed.
