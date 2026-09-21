# ReuseFirst Naming Research

## Scope And Cutoff

- Decision: establish one artifact title/tag and remove the retired name from
  current and preserved repository metadata.
- Audience: sf0.8 maintainers and future artifact-release reviewers.
- Scope: repository metadata, package contents, tests, release records, tags,
  and GitHub releases for `edoworks/sf0.8` and `edoworks/artifacts`.
- Cutoff: 2026-09-19.
- Stopping rule: stop when the retired name has no remaining textual reference
  in tracked metadata, documentation, tests, or release evidence, and when
  release/tag inventory has been checked directly.

## Source Plan

Primary sources were checked directly: the package manifest and skill,
`.factory/artifacts/reuse-registry.json`, the artifact record, ledger entries,
tests, and the GitHub tag/release inventory. Search output was treated as a
lead; each affected file was opened before editing.

## Findings

1. The canonical public skill declares the tag `reusefirst`, and the public
   README uses the same artifact name. [Canonical skill](https://github.com/edoworks/artifacts/blob/reusefirst/v1.2.0/artifacts/reusefirst/SKILL.md)
   (retrieved 2026-09-19).
2. Registry, manifest, record, ledger, tests, decision documentation, and
   feasibility evidence carried the retired artifact identifier. [Registry](../reuse-registry.json),
   [manifest](https://github.com/edoworks/artifacts/blob/reusefirst/v1.2.0/artifacts/reusefirst/MANIFEST.json), and [record](../records/reuse-gate.json)
   (retrieved 2026-09-19).
3. Direct inspection initially found the sf0.8 source repository had no tags or
   releases, but the public `edoworks/artifacts` repository had two legacy
   releases. Those were removed after the canonical `reusefirst/v1.2.0` release
   was verified.

## Counterevidence And Unknowns

- Historical external consumers, if any, were not queried. The repository
  record says publication is not approved, so no public compatibility contract
  was inferred.
- The package implementation filename `reuse_gate.py` remains descriptive
  rather than identity-bearing; changing it would add migration scope without
  addressing the title/tag inconsistency.

## Decision Implications

`reusefirst` is now the canonical artifact, skill, title, and tag prefix, and
the package path matches the tag. Future release work should create only a
`reusefirst` release/tag after human publication approval. The public release
inventory must be checked directly before any rename or cleanup claim.
