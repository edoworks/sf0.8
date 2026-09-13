# Roadmap — Factory v0.1

Source of rationale: [factory-v0.1-design-review.md](factory-v0.1-design-review.md) (twelve-week roadmap section). This file tracks execution state; update it at natural checkpoints, not retrospectively.

## Phase 0 — bootstrap (this week, bootstrap exception ≤30% factory work)

- [x] Design review committed (`docs/factory-v0.1-design-review.md`)
- [x] Prior-art anchor committed (`docs/research/prior-art.md`)
- [x] Private remote: `edoworks/sf0.8`; brand: edoworks.ai; license stance decided (Apache-2.0/CC-BY-4.0/DCO, publication-gated)
- [x] Product skeleton: `product-a/` (AGENTS.md, PRD template, handoff, repo.yaml, doctor/verify/bootstrap scripts)
- [x] NORTH_STAR.md + `.factory/governance.yaml` + `.factory/context-budget.yaml`
- [ ] **HUMAN: create `product-a/ProductA.xcodeproj`** (Xcode → iOS App → SwiftUI, Swift Testing, unit+UI tests)
- [ ] `./scripts/verify.sh` green on clean checkout
- [ ] **HUMAN: write the real 1-page `product-a/docs/PRD.md`** — exit criterion for Phase 0
- [ ] `edoworks/product-a` private remote created, main pushed

## Phase 1 — weeks 2–4

- [ ] First PRD-backed increment to device/internal TestFlight; handoff format written from actual work
- [ ] GitHub Actions `verify.yml` on `macos-26` (no release credentials); rulesets: protected main + required verify check
- [ ] Secret scanning + push protection + Dependabot on both repos
- [ ] One primary agent + one fallback; handoff proven on a real task

## Phase 2 — weeks 5–12

- [ ] Legacy quarantine (active product only)
- [ ] SQLite telemetry ledger + encrypted backup + first restore test
- [ ] Simple two-route routing policy (privacy/risk/complexity → primary/fallback)
- [ ] Portfolio inventory + lifecycle states (no mass rebuild)
- [ ] Open-source gate prep (LICENSE, DCO, SECURITY.md, trademark note) — publication is human-gated
- [ ] Entropy pass; blank-Mac disaster drill; v0.1 retrospective

## Explicitly deferred

Learned routing/budgets; workspace MCP server; vector DB / knowledge graph; web dashboard; publication automation; flipping any repo public; self-hosted runners for public PRs (never).
