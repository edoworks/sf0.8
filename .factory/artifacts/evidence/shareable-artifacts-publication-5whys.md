# Public Artifact Boundary Defect: 5-Whys

Date: 2026-09-19
Artifact: `reusefirst`
State: corrected locally; publication remains pending

## Observation

The first isolated release tree contained internal `sf0.8` and Product A
references in package documentation. The public-surface scan found them before
any push or release.

## Analysis

1. **Why did internal references enter the public tree?** The package README
   and provenance text were copied from the factory candidate without a
   public-language review.
2. **Why was the copy treated as public-ready?** The allowlist checked file
   paths and generated caches, but not content-level private-context terms.
3. **Why was content scanning absent?** The release procedure relied on the
   earlier feasibility report and local artifact validators, which validate the
   factory registry rather than the exact external tree.
4. **Why did the existing validators not catch it?** The public release tree
   is a separate staging repository and was not yet a first-class validation
   target in sf0.8 CI.
5. **Why was that boundary not first-class?** Publication had remained
   human-blocked, so external-tree validation had been planned but not
   operationalized.

## Correction

- Removed internal repository and product references from the public copy.
- Added a public-repository `.gitignore` for generated caches and local files.
- Added an exact-tree scan before any push or release.

## Recurrence guard

Every future artifact release must validate the staged repository, not only the
source factory, for private paths, product names, credentials, generated files,
and unsupported provenance claims. A failed scan blocks publication.
