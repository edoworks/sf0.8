# Portfolio Reuse Candidate Intake

Date: 2026-09-20
Scope: local-only preflight of Rung, Rendit, and FLocal
Decision: whether any candidate is ready for shared-artifact promotion
Authority: evidence record only; extraction, licensing acceptance, publication,
and release remain human-gated

## Evidence

| Candidate | Revision/state | License signal | Independent verification | Current disposition |
|---|---|---|---|---|
| Rung | Git `e1f2d922ed88623abb8b6800031dea8cf04cf880`; clean worktree | MIT in `LICENSE` and package metadata | 64 tests passed, including determinism and distribution contracts; separate `rungreport` pins engine commit `735142bf` | `REUSE_CANDIDATE`; consumer evidence exists, but current artifact intake and compatibility review are not approved |
| Rendit | Git `b00549fcab43e9d3d1ee9ec3a0222ffb446807a5`; source checkout dirty with modified tests and outputs plus untracked output; prior isolated probe used this pinned revision | No repository-root license was found; bundled assets carry mixed and restrictive license notices | Prior isolated probe passed 44 selected tests and identical deterministic renders; provenance records identify `gem-cascade`, `endless-runner-template`, and `docketloom-rebuild` | `REUSE_CANDIDATE`; defer pending complete dependency/asset license review and a domain-neutral workflow contract |
| FLocal | No Git `HEAD` or repository metadata available in the inspected path | MIT in `LICENSE` and package metadata | 32 tests passed, including macOS Seatbelt isolation and rollback-related coverage | `REUSE_CANDIDATE`; defer immutable provenance and second-consumer evidence |

## Promotion Test Result

No candidate passes the full promotion test from the curiosity audit:

- Rung has strong contract, provenance, license, and determinism evidence, and
  `rungreport` is a separate local consumer pinned to an earlier engine commit.
  Compatibility with the current revision and owner-approved shared intake are
  still unverified.
- Rendit has deterministic rendering, provenance, and multiple internal consumer
  records. Its bundled asset/dependency licensing boundary is not yet suitable
  for shared-artifact intake, and the current source checkout is dirty even
  though the prior isolated probe was pinned.
- FLocal has a clear trust-boundary design and passing tests, but no immutable
  repository revision is available in the inspected path and its Rung benchmark
  is not evidence of an independently adopted FLocal consumer.

## Required Evidence Before Promotion

1. Owner-approved candidate intake with an immutable source revision.
2. Exact license, dependency, asset, and provenance review.
3. A domain-neutral contract and clean fixtures outside the originating project.
4. Two independently useful consumers, not merely examples or registry entries.
5. Positive and negative trust-boundary tests.
6. Maintenance and regression comparison against keeping local implementations.

Passing these checks would support a promotion decision; it would not by itself
authorize publication or external release.

## Human Queue

- Decide whether Rung should be evaluated as a future internal shared artifact.
- Provide or authorize an immutable FLocal source repository/revision if intake
  is desired.
- Authorize Rendit license/dependency review from a clean pinned checkout.
