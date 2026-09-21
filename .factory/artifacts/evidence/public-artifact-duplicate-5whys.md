# Public Artifact Duplicate: 5-Whys

Date: 2026-09-19
Artifact: `reusefirst`
State: corrected locally; canonical public source verified

## Observation

The private factory retained a second source tree after `reusefirst` had been
released from `edoworks/artifacts` at `reusefirst/v1.2.0`.

## Analysis

1. **Why did the duplicate remain?** The local artifact registry was created
   before the public repository became the release source of truth.
2. **Why was it not retired at release time?** The registry tracked publication
   approval and candidate metadata, but not canonical external ownership.
3. **Why was canonical ownership absent?** Public distribution was treated as a
   feasibility decision rather than a source-of-truth transition.
4. **Why could stale paths survive?** No validator rejected source files under a
   local directory whose artifact had a public canonical repository.
5. **Why was that guard missing?** The migration boundary had not been modeled
   as an explicit artifact lifecycle state.

## Correction

- Recorded the canonical repository, version, tag, and source revision in
  `.factory/artifacts/public-sources.json`.
- Removed the local implementation, tests, manifest, skill, and license copy.
- Left a deprecation marker so old paths fail visibly instead of being reused.
- Updated local records and research citations to the canonical release.

## Recurrence guard

`scripts/validate-ecosystem.py` rejects files beyond `DEPRECATED.md` beneath a
local path marked `deprecated_pointer_only`. New public artifacts must record a
canonical source and cannot retain a second implementation tree.
