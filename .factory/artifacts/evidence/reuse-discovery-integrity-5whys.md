# Reuse Discovery Integrity 5-Whys

Date: 2026-09-19

## Defect

The reuse-before-build gate could accept self-reported search counts without
candidate evidence, and CI validated every change against a fixed historical
issue ledger. The Executive Council ledger therefore omitted relevant external
candidates while still claiming completed discovery.

## Analysis

1. Why could external discovery be claimed without external candidates? The
   gate accepted integer `searched` and `compatible` values plus free text.
2. Why were those values not checked? Candidate records were optional and not
   normalized under the reuse record.
3. Why could unrelated CI changes still pass? The workflow always supplied
   `issue-33.json` instead of selecting ledgers changed with the current diff.
4. Why was the mismatch not detected? Ledgers did not declare their capability
   and covered changed paths in a machine-verifiable form.
5. Evidence ends here. No claim is made about the historical intent behind the
   fixed ledger wiring.

## Corrections

- Immediate: correct issue 52 with the external candidates actually reviewed.
- Root cause: require normalized, unique candidate records; derive count
  consistency; require external coverage for new or extended machinery; and
  bind every gated changed path to a capability-bound issue ledger.
- Authority correction: classify dependency installation, skill activation,
  MCP configuration, plugin installation, and external contribution as
  human-only, including common command aliases.
- Recurrence guards: ecosystem, control-plane, safety-kernel, and CI tests now
  reject count-only evidence, duplicate candidates, missing external coverage,
  unbound paths, fixed stale ledgers, invalid test-only ledgers, and
  install/publish aliases including package-manager flag and module forms.
