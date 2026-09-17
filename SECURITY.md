# Security policy

**Repo status:** private (edoworks/sf0.8). No public releases yet.

## Reporting

Security and privacy issues get priority treatment under the Humanity & Safety Charter (`.factory/governance.yaml`). Report privately to the owner, not in public issues.

## Scope

This repo is the orchestration layer. It contains design documents, governance policy, and factory tooling — no signing credentials, no product secrets, no personal data. The private control plane lives outside this repo.

If a credential, personal/work reference, or private path leaks into history, that is a security incident under the Charter's `sensitive_data_to_unapproved_cloud` rule.

## Expectations

- Deterministic verification beats AI confidence: nothing is closed without `./scripts/verify.sh` or equivalent evidence.
- Release/publish/visibility changes are human-approved only.
- The safety-kernel prototype in `safety_kernel/` decides authorization but
  does not execute effects or provide host-level sandboxing. Its local audit
  chain is tamper-evident, not immutable against a privileged host.
