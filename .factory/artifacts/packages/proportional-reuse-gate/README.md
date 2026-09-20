# Proportional Reuse Gate

This package is a portable, dependency-free decision contract. Before building
new work, search for compatible existing work in proportion to the change
size. A new build is allowed only when the search is sufficient and the reason
is recorded. The result is advisory evidence, not publication or installation
authority.

`SKILL.md` is the agent-facing wrapper. It describes when to load this
capability, what evidence to collect, and which decisions are allowed. It does
not authorize installation, publication, upstream contribution, or external
execution.

`reuse_gate.py` is independently usable without sf0.8. The factory keeps a
separate implementation because its richer evaluator also handles provenance,
security, and contribution classification; the package contract is tested
against the same boundary cases without importing factory code.

## Versioned consumption

`MANIFEST.json` is the traceable distribution boundary. Consumers pin the
artifact id, semantic version, source revision, and checksum instead of relying
on an unversioned source path. This is intentionally a repository-visible,
dependency-free mechanism; a registry is not justified by the current two-
consumer trial.

## Evaluation

The package includes deterministic contract tests and decision cases under
`tests/` and `examples/`. These cases check that insufficient discovery,
invalid counts, and undocumented new builds are blocked.
