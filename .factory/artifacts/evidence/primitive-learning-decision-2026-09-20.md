# Primitive Learning Feedback Decision

Status: `IMPLEMENTED_AND_VALIDATED`
Issue: `70`

## Implemented

- Added `scripts/validate-primitive-learning.py` as a local, dry-run-by-default
  ingestion command.
- Extended the primitive inventory with explicit opportunity mappings.
- Added `apply_learning_to_opportunities` to update linked opportunity evidence
  without creating new opportunities or inferring unsupported stages.
- Added explicit booleans for problem observation, usage, retention, and
  economic value.
- Preserved the payment ladder: interest and contact exchange are not payment;
  deposit, preorder, purchase, and repeat purchase are payment evidence.
- Rejected synthetic results, duplicate/unknown references, invalid payment
  stages, and incomplete evidence records.
- Added an explicit duplicate-result guard so replay cannot inflate recurrence
  or evidence history.

## Boundaries Preserved

The command performs no outreach, observation, consent collection, payment,
publication, deployment, telemetry, dependency installation, or private-data
transfer. It only consumes an already admissible local result. Source records
are not mutated unless both explicit output paths are supplied.

## Feedback Flow

`learning result -> primitive inventory evidence -> linked opportunity evidence`

The flow does not automatically promote a candidate to a product, package,
metered service, or externalized capability. Unknown fields remain unknown.

## Next Autonomous Step

When a human-authorized Rendit observation exists, validate it with the command,
review the dry-run output, and write updated records only after the evidence is
confirmed. Then reassess the existing opportunity lifecycle with the established
tool-opportunity validator.
