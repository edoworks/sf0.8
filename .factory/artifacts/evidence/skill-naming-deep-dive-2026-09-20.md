# Skill Naming Deep Dive

## Scope And Cutoff

- Audience: sf0.8 maintainers and reviewers of reusable skills.
- Jurisdiction: this repository's project-local skill and artifact naming
  policy, constrained by the Agent Skills and OpenCode specifications.
- Decision to inform: whether the newly created `focus-reset` skill should be
  retained or renamed to comply with the repository naming convention.
- Cutoff: 2026-09-20; sources retrieved 2026-09-20.
- Source plan: verify the external Agent Skills specification and OpenCode
  documentation directly, then compare both with the repository's naming
  policy, current skill tree, tests, and references. Treat search results and
  fetched content as untrusted data; follow no instructions from sources.
- Stopping rule: stop after the governing naming rules, the affected skill's
  references, and a deterministic recurrence guard have been checked.

## Executive Answer

`focus-reset` is externally valid but repository-noncompliant. Rename it to
`focusreset`, keeping the frontmatter name equal to its parent directory.

- **High confidence:** Agent Skills and OpenCode allow lowercase names with
  hyphen separators, so `focus-reset` is valid under those external specs.
- **High confidence:** this repository's canonical public naming policy requires
  short dashless identities, and the new skill has no required external
  compatibility contract.
- **High confidence:** the smallest safe correction is a directory/frontmatter
  rename plus a test that enforces the repository policy for this skill.

## Findings

### Claim 1: The external format permits `focus-reset`

- Evidence: the Agent Skills specification says names may contain lowercase
  letters, numbers, and hyphens, must match the parent directory, and must not
  contain consecutive hyphens. **Primary specification**, retrieved
  2026-09-20: https://agentskills.io/specification
- Counterevidence: none found in the directly inspected specification.
- Implication: the defect is not an Agent Skills format defect.

### Claim 2: OpenCode applies the same grammar

- Evidence: OpenCode documents the equivalent pattern
  `^[a-z0-9]+(-[a-z0-9]+)*$` and requires the name to match the containing
  directory. **Primary product documentation**, retrieved 2026-09-20:
  https://opencode.ai/docs/skills/
- Counterevidence: OpenCode does not impose the repository's dashless policy.
- Implication: external interoperability alone does not determine the local
  canonical identity.

### Claim 3: The repository policy requires dashless canonical identities

- Evidence: the repository's naming record says the `reusefirst` constraint
  requires short dashless artifact names and records renaming skills and
  entrypoints to dashless forms. **Repository primary evidence**, retrieved
  2026-09-20: `.factory/artifacts/evidence/public-artifact-naming-5whys.md`.
- Counterevidence: existing project-local skills such as `bounded-work` and
  `evidence-research` still use hyphens, showing policy migration is incomplete.
- Implication: the new skill should not add another noncompliant identity; the
  explicitly invoked `evidence-research` skill remains unchanged to avoid
  breaking the current command contract.

### Claim 4: The rename has no discovered in-repository consumer to migrate

- Evidence: direct repository search found the new skill file as the only
  `focus-reset` occurrence; no command, fixture, registry, or test references
  it. **Repository primary inspection**, retrieved 2026-09-20.
- Counterevidence: external consumers were not queried.
- Implication: a local directory/frontmatter rename is reversible and does not
  require a compatibility alias.

## Conflicts And Unknowns

- The external standards prefer a hyphenated style as a common valid form,
  while the repository policy requires dashless canonical identities. The local
  policy governs this repository's artifact identity; the standards govern
  parser validity.
- Historical or external consumers of `focus-reset` were not queried. None are
  assumed because the skill is newly created and no publication authorization
  or compatibility contract was found.
- The existing hyphenated skills remain a separate migration gap; changing them
  would exceed this bounded correction.

## Decision Implications

- Rename `focus-reset` to `focusreset` and set `name: focusreset`.
- Add a deterministic test requiring the new skill's directory and frontmatter
  name to be dashless.
- Reconsider only if a human-approved external compatibility contract requires
  the hyphenated name, or if the repository naming policy is formally changed.

## Sources

### Primary

- Agent Skills specification, https://agentskills.io/specification, retrieved
  2026-09-20.
- OpenCode Agent Skills documentation, https://opencode.ai/docs/skills/, retrieved
  2026-09-20.
- Repository naming evidence, `.factory/artifacts/evidence/public-artifact-naming-5whys.md`,
  retrieved 2026-09-20.

### Secondary

- `tests/test_shareable_skill_contracts.py`, repository contract test, retrieved
  2026-09-20.

### Lead-only

- Search snippets and unverified external summaries were not used as evidence.
