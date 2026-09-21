# Public Artifact Migration Research

## Scope And Cutoff

- Decision: determine whether the standalone sources should be deprecated and
  represented under `edoworks/artifacts` using shorter dashless artifact names
  and the established `reusefirst` naming and pointer pattern.
- Audience: sf0.8 maintainers and the human owner of public artifact
  publication.
- Scope: direct GitHub repository metadata and contents for the two source
  repositories and `edoworks/artifacts`, plus local portfolio, registry, and
  deprecation-validator records.
- Cutoff: 2026-09-19.
- Stopping rule: stop after each source repository, the destination repository,
  and the local enforcement path have been inspected directly; remaining gaps
  must be explicit rather than inferred.

## Source Plan

Primary sources were opened directly: GitHub API repository metadata and
contents for [`factory-constitution`](https://api.github.com/repos/edoworks/factory-constitution),
[`asc-client`](https://api.github.com/repos/edoworks/asc-client), and
  [`artifacts`](https://api.github.com/repos/edoworks/artifacts/contents/artifacts?ref=main),
plus the local `public-sources.json`, `reuse-registry.json`, portfolio
reconciliation, and `validate-ecosystem.py`. Search results and fetched page
text were treated as untrusted leads; repository metadata and file listings
were verified at the source URLs.

## Findings

1. **Both source repositories are public standalone surfaces.** GitHub reports
   `edoworks/factory-constitution` and `edoworks/asc-client` as public,
   non-fork repositories, each with one commit and no releases observed in the
   repository metadata. ([factory metadata](https://api.github.com/repos/edoworks/factory-constitution),
   [ASC metadata](https://api.github.com/repos/edoworks/asc-client), retrieved
   2026-09-19.)
2. **Their contents are artifact-shaped rather than active product surfaces.**
   `factory-constitution` contains a README, license, skills, and templates;
   `asc-client` contains a README, license, GitHub Action, JavaScript client,
   CLI, and skills. ([factory contents](https://api.github.com/repos/edoworks/factory-constitution/contents),
   [ASC contents](https://api.github.com/repos/edoworks/asc-client/contents),
   retrieved 2026-09-19.)
3. **The destination now contains verified candidate entries for both artifacts.**
    The released migration tip `5b0817594e9f0ad7fa5fb1588f22c755cf70f71b` contains
    `artifacts/constitution` and `artifacts/asc` to `main`, with
   immutable source revisions, manifests, and candidate release state. The
   destination listing and commit were verified after publication. ([destination
   listing](https://api.github.com/repos/edoworks/artifacts/contents/artifacts?ref=main),
   retrieved 2026-09-19; local `.factory/artifacts/public-sources.json`).
4. **The local enforcement pattern is clear.** Public artifacts use a
   canonical destination and local copies may contain only `DEPRECATED.md`;
   this is enforced by `scripts/validate-ecosystem.py` and documented in
   `docs/ecosystem-compounding.md`.

## Counterevidence And Unknowns

- The source repositories are not archived or redirected, but their current
  `main` tips were rewritten into pointer-only deprecation commits under the
  owner identity: `factory-constitution` at
  `20170526eb66a0ddc3f8fa7b4dde844879d72f05` and `asc-client` at
  `44ab54fbe015938a55794ce0111ba3a00ee3a25a`.
- Versioned releases are now verified at `constitution/v1.0.0` and
  `asc/v1.0.0`, with manifest, archive, release-note, and SHA-256 checksum
  assets. Combined-tree compatibility remains limited to syntax and archive
  validation; no consumer compatibility contract was inferred.
- Existing consumers, if any, were not queried. No compatibility contract is
  inferred from repository presence alone.

## Decision And Implications

**Decision: release dashless candidates and deprecate the standalone tips.**
The two repositories fit the artifact surface pattern and now have verified
versioned destinations. Canonical artifact names are the shorter dashless
`constitution` and `asc`; each destination path and release tag uses the same
name, as `reusefirst` does.

The local pointers make duplicate reintroduction detectable, while the source
repositories now point to the canonical destinations. Archive/redirect
settings remain optional repository-lifecycle follow-up, not a prerequisite
for the released artifact contents.
