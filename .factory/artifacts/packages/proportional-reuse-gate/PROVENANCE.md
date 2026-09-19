# Provenance

- Origin: issue #31, `edoworks/sf0.8`.
- Generalization: extracted from the factory ecosystem-compounding increment;
  no Product A source, secrets, user data, or external artifact was included.
- Review: deterministic local tests and the artifact validator are the current
  evidence. Human publication approval is intentionally outstanding.
- Skill surface: `SKILL.md` is a generic procedural wrapper around the same
  decision contract; it contains no private factory paths, product context, or
  external instructions.
- Boundary: the package is independently testable, but it was not downloaded,
  installed, executed as an external artifact, or published by the factory.
