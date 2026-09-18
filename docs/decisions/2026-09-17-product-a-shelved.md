# Product A Shelved

Date: 2026-09-17
Decision: shelve `edoworks/product-a` and retain it as read-only evidence.

## Decision

Product A no longer meets the owner's quality bar after several iterations. It
is shelved rather than deleted. The Git repository, product history, PRD,
handoff, decision records, verification evidence, and unresolved release gates
remain available for future learning. Revival requires explicit owner
instruction and a new product-quality decision.

## Evidence

- The latest local commits were `d5bb97b` and `f38c050`; both were synchronized
  to `origin/main` before archival work.
- The canonical local verification gate passed on 2026-09-17 with 26 unit tests
  and 10 UI tests, but this did not establish physical audio quality,
  accessibility, specialist review, repeat use, or release readiness.
- `docs/production-readiness-audit.md` classified Product A as not ready for
  internal TestFlight, with unresolved P0 release gates and low-confidence
  product-value hypotheses.
- `product-a/docs/handoff.md` records the current interaction, privacy,
  verification, device, and evidence boundaries.

## Retained Learnings

- A narrow creature-led interaction is simpler than tabs, modes, history, or
  feedback surfaces; future products should test the core loop before adding
  product machinery.
- Deterministic local seams and explicit fake-microphone/output controls make
  UI verification useful, but passing simulated tests cannot substitute for
  physical audio, accessibility, or perceptual review.
- Claim restraint, ephemeral audio, no network path, and cat-only evidence are
  valuable safety and privacy boundaries.
- The real product questions were repeat use, comprehension, acoustic comfort,
  genuine pet response, and whether the experience felt like a relationship
  rather than a recorder or soundboard. These should be measured earlier in a
  future product.
- Apple-framework adapters need isolated compile checkpoints and separate
  capture/output test seams.

## Limits

No root cause is claimed for the owner's quality judgment beyond the evidence
above. The repository proves implementation and verification progress, not
delight, comprehension, real-pet response, or repeat-use value. Future work
must not treat Product A's green tests or design records as demand evidence.

## Archive Guard

The portfolio marks Product A archived and read-only, removes it as the active
private product, and requires explicit owner instruction for revival. No code,
issue history, or evidence is deleted by this decision.
