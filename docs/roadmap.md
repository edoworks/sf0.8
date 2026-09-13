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
- [x] **HUMAN: write the real 1-page `product-a/docs/PRD.md`** — done 2026-09-13 ("Whisker & Whistle" working title; AC-1..AC-8 open)
- [x] `edoworks/product-a` private remote created, main pushed

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

- [ ] Legacy quarantine (active product only)
- [x] SQLite telemetry ledger (`.factory/factory.sqlite` + `scripts/ledger.sh`; disposability verified)
- [x] Encrypted backup + first restore test (`scripts/backup.sh`/`restore.sh`; restore verified, RPO/RTO measured as same-session)
- [x] Simple two-route routing policy (`.factory/routing.md` — deterministic, learnable-later)
- [x] Portfolio inventory + lifecycle states (`.factory/portfolio.yaml`; 2 repos classified)
- [ ] Open-source gate prep (LICENSE, DCO, SECURITY.md, trademark note) — publication is human-gated
- [ ] Entropy pass; blank-Mac disaster drill; v0.1 retrospective

## Explicitly deferred

Learned routing/budgets; workspace MCP server; vector DB / knowledge graph; web dashboard; publication automation; flipping any repo public; self-hosted runners for public PRs (never).
