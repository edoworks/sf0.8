# Roadmap — Factory v0.1

Source of rationale: [factory-v0.1-design-review.md](factory-v0.1-design-review.md) (twelve-week roadmap section). This file tracks execution state; update it at natural checkpoints, not retrospectively.

## Phase 0 — bootstrap (this week, bootstrap exception ≤30% factory work)

- [x] Design review committed (`docs/factory-v0.1-design-review.md`)
- [x] Prior-art anchor committed (`docs/research/prior-art.md`)
- [x] Private remote: `edoworks/sf0.8`; brand: edoworks.ai; license stance decided (Apache-2.0/CC-BY-4.0/DCO, publication-gated)
- [x] Product skeleton: `product-a/` (AGENTS.md, PRD template, handoff, repo.yaml, doctor/verify/bootstrap scripts)
- [x] NORTH_STAR.md + `.factory/governance.yaml` + `.factory/context-budget.yaml`
- [x] **HUMAN: create `product-a/ProductA.xcodeproj`** (Xcode → iOS App → SwiftUI, Swift Testing, unit+UI tests) — done 2026-09-13; agent repaired placement to repo root, removed nested `.git`
- [x] `./scripts/verify.sh` green on clean checkout — TEST SUCCEEDED, iPhone 17 Pro / iOS 26.5, 2026-09-13; swift-format lint advisory-only (indentation warnings on template code)
- [x] **HUMAN: write the real `product-a/docs/PRD.md`** — current contract; AC-1..AC-10 require evidence, not documentation claims
- [x] `edoworks/product-a` private remote created, main pushed

## Current execution authority

The production-readiness audit and single backlog are authoritative for current
sequencing: `docs/production-readiness-audit.md`. Product A's contract remains
`product-a/docs/PRD.md`; its release evidence boundary is
`product-a/docs/device-validation-runbook.md`. Historical issue status and
simulator green results do not override those documents.

## Phase 1 — weeks 2–4

- [x] First PRD-backed increment to device: record→waveform→card loop (`d803d54`), live on Karen's iPad
- [x] INC-2026-09-13 crash fix + AC-2 verified (`af9096d`); 5-Whys + guards in handoff
- [x] AC-6 profiles + persisted history, both sim destinations green (`85b5e26`)
- [x] Non-reader surfaces both layers (`280211a`); decision doc 2026-09-13
- [x] GitHub Actions `verify.yml` on `macos-26` (no release credentials) — green on second run `34769357549` after destination pinning fix (`93b737d`)
- [x] Dependabot alerts + automated security fixes enabled on both repos (private-repo branch protection blocked: **GitHub Pro required**; revisit at publication)
- [x] Recurrence guard `scripts/ci-status.sh` both repos — blocking CI result gate; no CI claim without a captured result file (5-Whys fix, INC lesson 2026-09-13)
- [ ] Second-agent handoff proof on a real task (deferred: route A is this agent; proof requires a second route active)

## Phase 2 — weeks 5–12

- [x] Legacy quarantine (both repos: zero pre-factory issues/PRs; docs/AGENTS audited current — vacuous this time, the mechanism is recorded)
- [x] Open-source gate prep (SECURITY.md + CONTRIBUTING.md both repos; LICENSE/DCO/trademark still publication-gated per Charter)
- [x] Entropy pass (both repos: 1.7M/1.1M total, no caches, no stale files, all artifacts paying rent)
- [x] Blank-Mac disaster drill (`docs/disaster-drill-2026-09-13.md`: clone-from-origin, clean verify, restore, disposability invariant — all pass; RTO ≈6 min warm)
- [x] v0.1 retrospective (`docs/v0.1-retrospective.md`: five-proofs verdict with commit-level evidence; honest gaps recorded; v0.2 earns itself or waits)

## Explicitly deferred

Learned routing/budgets; workspace MCP server; vector DB / knowledge graph; web dashboard; publication automation; flipping any repo public; self-hosted runners for public PRs (never).

## Safety-kernel increment — Issue #12

- [x] Safety-kernel PRD, threat model, constitution, boundaries, capability
  model, envelopes, evaluations, and ADR drafted.
- [x] Dependency-free deny-by-default authorization prototype added with
  scoped capabilities, hard ceilings, delegation narrowing, and hash-chained
  audit evidence.
- [x] Initial adversarial tests cover missing/unknown/expired capabilities,
  scope confusion, human-only operations, budget exhaustion, audit failure,
  and delegation amplification.
- [x] Cost-neutral Docker adapter added with a fixed restricted profile and
  fail-closed daemon/container failure handling; Docker Desktop 29.7.2 smoke
  passed for non-root execution, read-only filesystem, and no outbound TCP.
- [x] Docker execution is now reachable only through an `ALLOW` decision, with
  approved-root/symlink confinement, digest pinning, and completed-effect audit
  evidence; integrated smoke passed.
- [ ] Host-enforced sandbox, credential broker, and externally protected audit.
- [ ] Dogfood through the kernel and complete collusion evaluation before any
  meaningful autonomous external action.

## Session priority — 2026-09-17

The production-readiness audit is the active queue. Validation of this session
passed the repository lifecycle gate, 40 factory tests, the safety-kernel suite,
Product A doctor, and Product A verification (24 unit tests and 13 UI tests,
one intentional skip). These results do not close physical-device or release
gates.

1. **P0 Product A:** exact artifact, real audio/lifecycle, accessibility and
   adaptive layout, current-artifact specialist review, and migration/privacy
   inspection.
2. **P1 factory:** consolidate the governed release evidence path only after
   the archive/TestFlight path exposes the concrete missing control.
3. **P1 factory:** prove a second-agent handoff on a real bounded task when a
   second route is available; do not build transcript or harness abstractions.
4. **P2 safety:** preserve the prototype boundary; host isolation, credential
   brokering, external audit, and collusion evaluation remain blocked from
   autonomous use.
5. **Recovery:** resolve off-device backup and cold-machine authentication gaps
   as owner recovery actions.

Learned routing/budgets, MCP, vector or knowledge systems, dashboards,
publication automation, public self-hosted runners, and sf0.7/sf0.5 queue
items remain rejected or read-only evidence, not active work.
