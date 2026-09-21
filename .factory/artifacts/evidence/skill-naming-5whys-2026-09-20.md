# Skill Naming: 5-Whys

Date: 2026-09-20
Observation: the newly created `focus-reset` skill used a hyphenated identity
despite the repository's dashless canonical naming policy.

## Analysis

1. **Why was the skill noncompliant?** Its directory and frontmatter used
   `focus-reset` instead of the repository-required `focusreset`.
2. **Why was that name selected?** The external Agent Skills/OpenCode grammar
   permits hyphenated names, so external validity was mistaken for local policy
   compliance.
3. **Why did that mistake pass review?** The contract test checks the external
   lowercase-kebab grammar but does not assert the repository's dashless rule
   for newly created skills.
4. **Why was the local rule not executable?** The naming policy existed in
   evidence prose, while the skill contract and discovery checks enforced only
   the broader external grammar.
5. **Root cause supported by evidence:** local naming policy and external format
   validity were not represented as separate, executable invariants.

## Correction

- Immediate correction: renamed `.agents/skills/focus-reset` to
  `.agents/skills/focusreset` and changed its frontmatter name accordingly.
- Root-cause correction: added a focused regression test for the dashless
  canonical identity of this newly created skill.

## Recurrence Guard

The test must assert that the skill directory and frontmatter name are exactly
`focusreset` and contain no hyphen. Future policy expansion should move this
assertion into a repository-wide canonical-name validator rather than relying
on prose review.
