# Run Bounded Rendit Workflow Probe

## Goal

Test one deterministic Rendit render/validation workflow as an internal
prototype and possible shovel without splitting the canonical runtime or
claiming external demand.

## Acceptance Criteria

- Use one clean, pinned Rendit source revision.
- Keep one canonical runtime and one workflow-level wrapper only.
- Preserve deterministic fixtures, provenance, dependency isolation, and
  negative trigger tests.
- Demonstrate one genuine second consumer or record that it is absent.
- Record setup cost, task success, repeat use, integration pull, and unresolved
  licensing/dependency questions as evidence or unknowns.

## Stop Condition

Stop and retain Rendit as internal infrastructure if determinism or provenance
cannot be preserved, the second consumer does not appear, or the artifact is
useful without any pull toward the integrated workflow.

## Hard Boundary

No public packaging, publication, dependency installation, external feedback
campaign, or product expansion is authorized by this issue.
