# Issue-Creation Handoff 5-Whys

Date: 2026-09-20
Tracking: issue #80

## Defect

Issues #73 through #79 were created successfully but their completeness
depended entirely on prose authored before the GitHub write. The workflow had
no machine-readable completeness contract and no read-back equality check.

## Evidence-Based Analysis

1. Why could an issue be created with incomplete decision context? The writer
   accepted any body file and GitHub accepted it; neither enforced semantic
   sections beyond valid command syntax.
2. Why did the writer not recover omitted context? The writer was expected to
   infer completeness from conversation and a prose skill. In the inspected
   incident, it instead transported the available files exactly, which is safer
   but preserves planner omissions.
3. Why could planning omit material fields? The issue-tracking skill required
   scope, acceptance criteria, and verification in prose but defined no
   required schema for outcome, non-goals, dependencies, authority, or source
   provenance.
4. Why was the omission not caught before or after mutation? There was no
   validator, frozen digest, negative fixture, or remote title/body comparison.
5. Root cause supported by evidence: issue creation was modeled as a
   model-authored conversation task rather than a planner-owned validated
   artifact followed by deterministic transport.

Evidence stops here. The inspected records do not establish that Luna created
issues #73 through #79; they identify Sol medium for the creation calls. They
also do not establish a general Sol-versus-Luna quality difference because no
controlled, repeated issue-handoff comparison exists.

## Corrections

- Immediate correction: treat the current issue bodies as faithfully
  transported but not as proof that every intended planning detail was present.
- Root-cause correction: the planner now freezes a JSON intent, complete
  Markdown body, and SHA-256 digest; the writer validates and transports the
  exact artifact without rewriting it.
- Mechanical recurrence guard:
  `~/.config/opencode/scripts/issue-intent.mjs` rejects missing sections,
  missing metadata, path escape, digest drift, and remote title/body drift.
- Workflow correction: the global `issue-tracking` skill now assigns semantic
  completeness to the planning role and exact transport plus readback to the
  writing role. A stronger writer model is not a substitute for validation.

## Verification

- Focused validator suite: 5 tests passed.
- Full shared OpenCode suite: 38 tests passed.
- Negative fixtures prove omission, post-plan edits, path escape, and readback
  drift are rejected.
