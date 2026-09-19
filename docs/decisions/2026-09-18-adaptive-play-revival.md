# Adaptive Play Revival

Date: 2026-09-18
Issue: [Adaptive pet-made play prototype revival](https://github.com/edoworks/sf0.8/issues/30)

## Decision

The pet product is revived from the archived audio-conversation direction as a
small, local adaptive play experiment. The active contract is `PET <-> LITTLE
WORLD <-> HUMAN`: a cat interacts directly with a handmade-feeling world, and
future prey behavior changes from observable interaction evidence.

This is an owner-directed revival. The product repository's GitHub archive flag
prevented issue creation there, so issue #30 in the active factory is the
canonical mirror until the repository lifecycle can be changed by an authorized
repository operation.

## Five-Whys: Lifecycle Blocker

1. Why could the product issue not be created? GitHub rejected issue creation
   because `edoworks/product-a` is archived and read-only.
2. Why is the repository archived? The prior product direction failed the
   owner's quality bar and was intentionally shelved.
3. Why does the current instruction conflict with that state? The new request
   explicitly revives the product around a materially different hypothesis, but
   the archive metadata was not yet changed.
4. Why was the metadata not changed before issue creation? The repository
   lifecycle requires an owner-authorized revival and a new quality decision;
   the work began with the existing archive state still authoritative.
5. Evidence limit: no deeper cause is established beyond the observed mismatch
   between the explicit revival instruction and GitHub's archived state.

## Correction And Guard

- Immediate correction: mirror the increment in root issue #30 and record this
  decision before implementation.
- Root-cause correction: update the root portfolio and product repository
  lifecycle metadata together, with the new PRD as the active contract.
- Mechanical guard: repository verification must reject a product whose local
  lifecycle says active while the root portfolio still says archived, and must
  report the GitHub archive flag as a release/lifecycle blocker.

## Evidence Boundary

This decision authorizes local implementation and verification only. It does not
authorize repository visibility changes, publication, App Store release, or
claims about cat welfare, health, emotion, or scientific efficacy.
