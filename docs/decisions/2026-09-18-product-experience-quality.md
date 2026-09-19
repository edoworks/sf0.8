# Product Experience Quality Decision

Issue: [Factory: Apple-first product experience quality](https://github.com/edoworks/sf0.8/issues/32)

## Repository-grounded 5-Whys

1. sf0.8 can produce technically correct software without exceptional
   experiences because its lifecycle and tests primarily prove build, behavior,
   safety, and release evidence; the design checklist is not a blocking,
   evidence-backed review contract.
2. The existing design checklist does not require a compact intent before UI
   implementation, an adversarial rendered critique, or an explicit subtraction
   pass.
3. The QA skill requests screenshots and an art-director review, but the factory
   has no deterministic record tying rendered evidence to findings, accessibility
   settings, device boundary, or unresolved design debt.
4. Current Apple capability discovery is scattered across product skills and
   product code; there is no dated, source-backed disposition distinguishing
   stable, beta, experimental, and deployment-target-blocked capabilities.
5. The definition of done therefore rewards functional completion before the
   experience has been seen, critiqued, simplified, or compared with current
   platform opportunities.

Evidence ends here. The repository does not establish that tooling, staffing,
or model quality is the deeper cause.

## Root causes and corrections

- Missing intent ownership: add `docs/design-intent-template.md` and require it
  in the experience review record.
- Missing rendered decision loop: add `scripts/apple-quality.py`, design critic,
  final-10 checklist, and explicit evidence levels.
- Stale platform knowledge: add the thin Apple Platform Intelligence source
  contract and dated authoritative source ledger.
- Invisible debt: require `design_debt` and `apple_platform_debt` lists, including
  explicit empty lists.

## Deliberately not added

No custom renderer, visual-QA framework, API catalog, agent-skill copier,
Liquid Glass wrapper, device farm, dashboard, or package registry was added.
Apple-native APIs and XCTest/XCUITest remain the product-side mechanisms.
