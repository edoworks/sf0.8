# Issue 52 Metadata And Release Claim 5-Whys

Date: 2026-09-24

## Public claim drift

1. Active public metadata advertised a broken Rung homepage and deprecated
   repositories still described themselves as active products.
2. Repository descriptions, homepage fields, README lifecycle text, licenses,
   and release records were maintained independently.
3. The canonical inventory recorded lifecycle but not the public metadata
   fields or release properties that users actually saw.
4. The public-surface preflight checked visibility and the presence of any
   detected license, but did not compare descriptions, homepages, archive
   state, exact license policy, mutability, or asset inventory with a contract.
5. Completion evidence therefore accepted internally consistent source files
   without proving that live repository and release surfaces matched them.

Root cause: no machine-readable contract joined canonical lifecycle state to
the exact public metadata and release fields.

Immediate correction: correct supported source claims, record current live
metadata, retire the broken custom-domain surface, and leave denied metadata
writes explicitly blocked.

Root-cause correction: `.factory/repository-metadata-target.json` and the
extended public-surface preflight compare exact metadata, release mutability,
and attached assets. Issue 52 cannot close while that contract is blocked.

## ReuseFirst release divergence

1. Documentation called `reusefirst/v1.2.1` immutable and implied attached
   checksums even though its release record is mutable and assetless.
2. Release metadata was prepared on a detached commit and initially did not
   reach the default branch.
3. The catalog represented all artifacts with one blanket release-assets
   model instead of recording distribution properties per artifact.
4. Tests covered artifact behavior but not catalog-to-release agreement.

Root cause: publication state and consumer claims were not validated against
the live release record and tagged tree.

Immediate correction: mark the existing tag as a historical release with
known defects and reconcile corrected source onto `main` without moving the tag
or publishing a replacement.

Root-cause correction: the artifacts catalog and CI now check versions,
licenses, mutability, asset counts, and the two known tag defects.

## Factory CI rate-limit failure

1. The first Factory PR check failed with GitHub API HTTP 403.
2. Its live release test used unauthenticated API requests.
3. Shared runner traffic exhausted the anonymous rate limit.
4. The workflow had a read token but did not expose it to the test.

Root cause: a required network assertion depended on anonymous API capacity.

Correction and guard: the workflow passes its scoped read token, the test
authenticates when one is available, and missing release fields no longer pass
through permissive defaults. The corrected check passed before merge.

## sf0.8 changed-path gate failure

1. The first sf0.8 PR run `35945261793` blocked four changed machinery paths.
2. The feature added validators and workflow enforcement without a current
   issue ledger claiming those paths.
3. Issue #52 existed in the canonical Factory tracker but had not been added to
   sf0.8's capability binding registry.
4. Local unit and semantic validators do not substitute for the complete-event
   changed-path ownership gate.

Root cause: the increment omitted its repository-local capability binding and
reuse ledger before opening the PR.

Correction and guard: bind the exact Factory issue and add
`.factory/artifacts/ledger/issue-52.json` with only the four gated paths. Re-run
the same pull-request range validator before updating the PR.

## Remaining authority blockers

- The normal `gh repo edit` command is denied by active tool policy. No API
  workaround was used.
- PR creation is denied for `edoworks/asc-client` and
  `edoworks/factory-constitution`. Reviewed feature branches are pushed, but
  direct pushes to `main` are prohibited.

These are observed trust-boundary constraints, not evidence that the target
state was reached.

## Evidence References

- Factory correction: `edoworks/factory` PR #58, merged as
  `d1f13f7824c176840d16555b9dd2524c7c1be674`; corrected policy run
  `35940629675` passed.
- Artifacts correction: `edoworks/artifacts` PR #3, merged as
  `9d868f8565c94709a34d7dd79501d994776e46bd`; catalog contract run
  `35942798691` passed.
- Detached ReuseFirst release history: tag target
  `30502b958a485e5466e20c554ee3c159044bb0a6`; the later default-branch
  reconciliation before issue #52 was `3f2270c477de13d71a47ed0e2781303a52adeb6a`.
- Current live metadata snapshot timestamp and revisions are recorded in
  `.factory/repository-inventory.json`.
- Current desired metadata and exact declared blockers are recorded in
  `.factory/repository-metadata-target.json` and checked in CI.
