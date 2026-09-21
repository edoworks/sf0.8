# End-to-End Map

Owner decision: use a new, narrow meow-capture app as the first consumer. Do
not revive Product A.

## Child increments

- [x] #74 — product contract, lifecycle boundary, and measurable acceptance
- [ ] #75 — portable production audio core and approved-fixture Mac replay
- [ ] #76 — visible, bounded, owner-started Mac live-listening probe
- [ ] #77 — polished iOS/iPadOS automatic capture and playback vertical slice
- [ ] #78 — exact-revision physical iPhone/iPad audio validation
- [ ] #79 — real-cat capture and unscripted family-visible acceptance

## Dependency order

`#74 -> #75 -> (#76 and #77) -> #78 -> #79 -> #73 closeout`

## Map closure rule

Keep #73 open until every child is complete or an explicit stop decision is
recorded. Mac fixture or live-probe success is host evidence only. Completion
requires the same production core in the Apple app, physical iPhone and iPad
evidence, automatic capture and audible playback of a real cat meow, local
deletion, and current visual evidence of the family-visible experience.

Raw household audio must remain outside Git, CI, issue comments, logs, and
durable factory evidence.

## Status

- #74 completed 2026-09-20. The contract is
  `docs/decisions/2026-09-20-meow-capture-product-contract.md`.
- #75 has a macOS/iOS shared policy and event-window boundary plus a passing
  generated non-target replay. It remains open for an owner-approved local
  real-meow fixture set; no private historical audio was reused.
- Owner-selected fresh real-meow replay passed on 2026-09-20. Non-audio evidence
  is `.factory/artifacts/evidence/host-audio-validation-owner-fixture-2026-09-20.json`.
- Next active actions: advance #76 and #77. Physical-device and family gates
  remain #78 and #79.
