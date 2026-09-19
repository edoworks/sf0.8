# Product Identity Reviewer Failure 5-Whys

## Question

Why did an app named `Product A` get this far through distribution and App
Review preflight?

1. Distribution evidence was evaluated independently from customer-facing
   identity, so a real archive could advance without a resolved public name.
2. The preflight contract represented metadata as fields and required values,
   but did not model internal codename versus authorized public identity.
3. No deterministic semantic rules detected placeholder, generic, or internal
   terminology, and no reviewer layer compared metadata with product purpose.
4. Customer Zero was linked as evidence presence, not as a recognition and
   purpose test for the public product page.
5. The factory had no adversarial App Review dogfood gate that asks whether a
   skeptical reviewer would regard the submission as finished, intentional,
   customer-facing, and discoverable.

## Root cause

The reusable root cause is a missing product-identity and semantic-review
contract, not a missing string check. Structural metadata validation was
allowed to stand in for reviewer judgment.

## Correction

- Add an authoritative internal/public identity object with explicit human
  authorization and evidence.
- Add deterministic placeholder and technical-terminology signals.
- Add semantic product-purpose and Customer Zero checks.
- Add reviewer validation for screenshots, public copy, URLs, discoverability,
  and internal leakage.
- Make unresolved identity a direct `APP_REVIEW_READY` blocker.

## Recurrence guard

`tests/test_apple_distribution.py::test_internal_codename_cannot_reach_app_review_ready`
proves that a Product A-equivalent public name cannot silently pass readiness.
