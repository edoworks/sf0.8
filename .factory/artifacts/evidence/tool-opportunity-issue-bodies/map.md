# Tool Opportunity Discovery Map

## Decision

Operationalize the evidence-first tool-opportunity ledger without treating
internal infrastructure as market validation.

## Scope

- Keep `.factory/tool-opportunity-ledger.json` as the signal source of truth.
- Preserve existing product opportunity, reuse registry, human-action queue,
  and publication gates.
- Track only the three child increments linked from this map.

## Priority

1. Bind and validate the ledger in the factory control plane.
2. Measure recurrence and a second consumer for the strongest internal signals.
3. Run one bounded Rendit workflow prototype only after its acceptance gate is
   explicit; no public packaging.

## Out Of Scope

No new product, public package, dependency installation, external publication,
customer recruitment, payment request, or repository lifecycle mutation.

## Success

Each child closes only with its stated evidence and stop condition. Unknown
external demand remains unknown.
