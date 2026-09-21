# Routine Tool Routing Gap

## Impact

Deterministic command and status work could be issued through a standard model
turn even though the routing policy requires routine handling. The available
ledger evidence reports `$0.42` across recent runs but does not attribute tool
calls to a provider or model, so the exact excess cost is not established.

## Evidence-Based 5 Whys

1. A standard model could handle shell-oriented work because the coherence guard
   rejected routine classifications only for the complex frontier tier.
2. The guard had a narrower scope because the initial safety rule was written to
   prevent the highest-cost escalation, not to prevent all non-routine dispatch.
3. Individual tool calls could not independently change model tier because
   OpenCode's `chat.params` hook exposes request parameters, not model
   substitution, and tool hooks do not receive model identity.
4. Attribution was incomplete because the routing telemetry stored aggregate
   runs and costs without session-level model and tool metadata.
5. Evidence does not establish why the original design stopped at the complex
   boundary; deeper process causes would be assumptions.

## Corrections And Guards

- Immediate correction: reject routine-class requests on both standard and
  complex routes, directing them to `small` or `explore`.
- Root-cause correction: record provider/model, agent, session, and tool name at
  the request/tool boundary without persisting command text or credentials.
- Mechanical guards: unit tests reject routine work on standard and complex
  routes, classify shell/status phrases as routine, and verify sanitized tool
  attribution records.
- Verification: run the complete OpenCode routing test suite and inspect the
  resulting attribution record shape.

## Startup Regression

### Evidence-Based Whys

1. OpenCode could not complete startup after the attribution change because the
   configured legacy plugin module exposed multiple function exports.
2. OpenCode 1.18.19 treats every exported function in a legacy module as a
   plugin initializer, not merely the default export.
3. The attribution helper was exported from `cost-router.mjs` for unit tests,
   so the loader attempted to initialize it as a plugin and received no hook.
4. The tests checked JavaScript syntax and helper behavior but not the module
   export contract used by the OpenCode loader.
5. Evidence does not establish a deeper process cause; the missing loader-shape
   smoke test is the furthest supported cause.

### Corrections And Guard

- Immediate correction: move helper exports to `cost-router-lib.mjs`, leaving
  `cost-router.mjs` with only its default plugin initializer.
- Root-cause correction: add a regression test requiring exactly one export from
  the configured legacy plugin and retain a clean startup smoke test in the
  verification procedure.
- Verification: restart OpenCode normally, confirm the router config hook runs,
  and confirm the selected plan/build routes match the approved registry.

### Verification Result

On 2026-09-16, `npm test` passed with 33 tests and 0 failures. The configured
plugin exported only `default`; the live config hook selected
`ollama/granite4.1:3b` for `small` and `explore`, and
`openai/gpt-5.6-luna` for `plan` and `build`. A normal `opencode serve` smoke
test reached its listening state without debug mode.
