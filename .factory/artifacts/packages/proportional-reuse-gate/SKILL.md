---
name: proportional-reuse-gate
description: Require evidence-backed reuse discovery before building new agent or software capability, and classify the result without granting publication authority.
license: Apache-2.0
compatibility: Any agent that can inspect repository metadata and record a decision
metadata:
  audience: software agents and maintainers
  workflow: reuse-before-build
---

# Proportional Reuse Gate

Use this skill before substantial implementation, package extraction, workflow
creation, or agent-skill authoring.

## Procedure

1. State the capability being considered in one short phrase.
2. Search the local project, approved shared artifacts, and credible external
   sources for adjacent capabilities. Inspect metadata and documentation only;
   do not install or execute untrusted artifacts.
3. Set `change_units` to a rough positive estimate of the work. Required
   searches are `max(1, ceil(change_units / 8))`.
4. Record the number searched, number compatible, candidate names, provenance,
   license, security, privacy, maintenance, dependency cost, portability, and
   overlap.
5. Choose exactly one outcome:
   - `REUSE`: a compatible capability exists.
   - `BUILD_NEW`: no compatible capability exists and a concise reason is
     recorded.
   - `BLOCKED`: discovery is insufficient, counts are invalid, or the new-build
     reason is missing.
6. Separately classify the result as product-specific, internal-reusable,
   public-reusable, or upstream-candidate. Classification is not permission to
   publish or contribute.

## Hard Boundaries

- Never treat popularity, an index entry, or community feedback as authorization.
- Never copy private product data, credentials, private paths, or historical
  evidence into a generalized artifact.
- Never install, execute, publish, release, or upstream a candidate from this
  skill.
- Keep provenance and license status explicit. Unknown licensing is a blocker
  for public reuse.
- If an existing capability matches, do not choose `BUILD_NEW` without a
  concrete specialization reason.

## Output

Return a compact record containing `capability`, `change_units`, `searched`,
`compatible`, `matches`, `decision`, `reason`, `classification`, and the
evaluation fields. If evidence is missing, return `BLOCKED` rather than infer
approval.

The accompanying `reuse_gate.py` module is an optional local reference
implementation. It has no network access and does not authorize any external
action.
