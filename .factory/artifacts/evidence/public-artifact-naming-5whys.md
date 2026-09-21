# Public Artifact Naming: 5-Whys

Date: 2026-09-19
Observation: the first published candidate paths used dashes despite the
`reusefirst` naming constraint requiring short dashless artifact names.

## Analysis

1. **Why did the paths use dashes?** The source repository names were copied
   into artifact IDs and paths without a separate canonical-name decision.
2. **Why was that accepted?** The migration review checked ownership and
   provenance but did not make the naming grammar an executable invariant.
3. **Why was the grammar implicit?** `reusefirst` was treated as an example,
   not as a repository-wide naming contract.
4. **Why could the error reach `main`?** Catalog, manifest, pointer, and tag
   fields were reviewed independently instead of being compared mechanically.
5. **Why was there no comparison guard?** The validator enforced destination
   shape and publication state, but not dashless artifact identity.

## Correction

- Renamed the canonical artifact identities to `constitution` and `asc`.
- Renamed canonical paths, planned tags, skills, and entrypoint filenames to
  dashless forms.
- Kept dashed source repository URLs only as historical external identities.
- Updated sf0.8 registry, portfolio, pointers, and evidence.

## Recurrence Guard

The migration validator now requires each target path to equal
`artifacts/<artifact>` and each planned tag to equal `<artifact>/v1.0.0`.
The artifact registry and catalog must therefore derive their public identity
from the same short dashless name rather than from a source repository slug.
