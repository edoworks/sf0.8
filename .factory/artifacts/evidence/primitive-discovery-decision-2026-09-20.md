# Capability Primitive Discovery Decision

Status: `IMPLEMENTED_AND_VALIDATED`
Issue: `69`

## Factory Changes

- Added `.factory/capability-primitive-inventory.json` as an evidence overlay
  over the existing reuse registry and tool opportunity ledger.
- Added `scripts/primitive_discovery.py` and
  `scripts/validate-primitive-discovery.py`.
- Added deterministic evidence separation for problem, usage, retention,
  economic, and payment levels.
- Added conservative classification, externalization risk gates, and structured
  learning-record application without telemetry or external action.
- Added CI and ecosystem validation, targeted tests, and a human-action queue
  entry for the next Rendit experiment.

## Existing Mechanisms Reused

- `.factory/tool-opportunity-ledger.json` and `scripts/tool_opportunities.py`
  remain the second-order opportunity source of truth.
- `.factory/artifacts/reuse-registry.json` remains the shareability and
  provenance authority.
- `scripts/ecosystem_gates.py` remains the reuse/contribution gate.
- `scripts/evidence_frontier.py` remains the external-human evidence boundary.
- `.factory/human-action-queue.json` remains the authority boundary for
  observation, outreach, payment, and other external actions.

## Candidate Findings

| Candidate | Classification | Evidence boundary |
| --- | --- | --- |
| ReuseFirst | `OPEN_DISTRIBUTION` hypothesis | Verified internal/product Customer Zero use; external retention and payment unknown. |
| Rendit deterministic workflow | `DEVELOPER_PRIMITIVE` hypothesis | Problem-category and internal usage evidence present; retention, economic, and payment evidence unknown. |
| Ecosystem validators | `INTERNAL_ADVANTAGE` | Strategic sensitivity is high; internal use does not establish external demand. |
| CI status evidence | `INSUFFICIENT_EVIDENCE` | Internal recurrence exists; external problem and payment evidence unknown. |

## Evidence Matrix

No candidate currently has payment evidence. Rendit has problem and internal
usage evidence only. No candidate has verified external retention. Internal
recurrence and technical feasibility remain explicitly separate from market
evidence.

## Accidental Products

The strongest accidental-product candidates are ReuseFirst and the Rendit
workflow. ReuseFirst already has a human-approved public release, but no
external market evidence was added by this increment. Governance validators,
CI evidence, idle-work dispatch, and Apple preflight remain internal or
insufficiently evidenced because they expose factory-specific policy or lack
an independent user/workflow.

## Rendit Next Step

The smallest authorized experiment is one human-authorized external workflow
observation or interview. It should capture the job, current substitute,
frequency, friction/rework, repeat-use request, and only then an economic or
payment signal if the problem recurs. No package, skill, API, publication,
outreach, dependency installation, or payment request is authorized by this
artifact. The executable request is
`rendit-external-workflow-observation` in the human-action queue.

## Unresolved Uncertainties

- External users and workflows are unknown.
- Retention, measurable economic value, pricing, and payment are unknown.
- Rendit licensing and dependency suitability for sharing remains incomplete.
- The best external surface may be manual observation, CLI, skill, library,
  or service; no surface is selected by this increment.

## Human Authorization Requests

Only the Rendit workflow observation/interview is currently queued. It requires
participant selection, consent, privacy scope, and explicit human approval.
No autonomous external action was performed.

## Next Autonomous Step

Validate future learning records against the inventory, update evidence only
from admissible observations, and feed repeated workflows into the existing
tool opportunity ledger without promoting unknown fields or creating duplicate
opportunity systems.
