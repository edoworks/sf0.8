# Bind and Validate Tool Opportunity Ledger

## Goal

Make `.factory/tool-opportunity-ledger.json` a checked-in, issue-bound factory
control-plane artifact without duplicating the product opportunity ledger or
reuse registry.

## Acceptance Criteria

- Add the owner-approved capability binding and issue ledger entry.
- Keep `python3 scripts/tool_opportunities.py validate` and `scan` fail-closed.
- Keep `python3 scripts/validate-ecosystem.py` green.
- Confirm the ledger remains separate from product opportunity and shareability
  classifications.
- Preserve all current publication, external-artifact, and human-authority
  gates.

## Stop Condition

Stop if the change requires a second opportunity registry, automatic product
creation, inferred market evidence, or a policy relaxation.

## Verification

Run the ledger validator, ecosystem validator, targeted tests, and the full
local test suite. Review changed paths before any commit or external write.
