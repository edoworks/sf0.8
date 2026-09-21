# ReuseFirst Canonical Metadata Reconciliation

Status: `MERGED_CANDIDATE_PREPARATION`
Artifact: `reusefirst`
Revision: `30e588b4dc0d869da9b58a01d91c22d6f4931361`

## Verified Contradiction

The pinned public tree and release page are visible, and Customer Zero
dogfooding now passes for the factory, Product A, Vorynce, and the modeled
Intent Compiler workflow. However, the canonical `MANIFEST.json` at the pinned
revision reports:

```json
{
  "source_revision": "issue-31-working-tree",
  "release_state": "CANDIDATE_UNRELEASED",
  "publication_approved": false
}
```

The local source record and release evidence identify the immutable revision as
`30e588b4dc0d869da9b58a01d91c22d6f4931361` and confirm the release page.

## Proposed Canonical Change

An owner-authorized change in `edoworks/artifacts` should update only the
canonical manifest to:

```json
{
  "source_revision": "30e588b4dc0d869da9b58a01d91c22d6f4931361",
  "release_state": "RELEASED",
  "publication_approved": true
}
```

The change should retain the existing artifact contents, tests, license,
provenance, and release tag. It should include the Customer Zero evidence URL
or an equivalent canonical evidence reference.

Prepared as [edoworks/artifacts#2](https://github.com/edoworks/artifacts/pull/2).
The PR merged as candidate preparation. It did not mutate the existing
`reusefirst/v1.2.0` tag or publish `v1.2.1`.

## Local Guard State

- `.factory/artifacts/reuse-registry.json`: `PUBLIC_CANDIDATE`, approval false
- `.factory/artifacts/publication-state-reconciliation.json`:
  `PENDING_EXTERNAL_METADATA_RECONCILIATION`
- No local promotion or external release was performed.

## Verification Evidence

- `.factory/artifacts/evidence/reusefirst-customer-zero-dogfood.json`
- `.factory/artifacts/evidence/reusefirst-customer-zero-5whys-2026-09-20.md`
- `https://github.com/edoworks/artifacts/tree/reusefirst/v1.2.0/artifacts/reusefirst`
- `https://github.com/edoworks/artifacts/releases/tag/reusefirst/v1.2.0`
