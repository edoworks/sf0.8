# Design Language PRD

Status: proposed
Issue: #26

## Executive summary

Define a shared design language for the factory's operator surfaces and the
iPhone/iPad products it helps ship. The language should make important state,
next actions, uncertainty, and accessibility obvious while allowing each
product to retain its own personality.

This is a documentation and reference-slice increment. It is not a request to
build a universal design-system platform or to make every product look alike.

## Problem

The factory needs two kinds of interface quality:

- Operator tools must make queue state, evidence, risk, ownership, and recovery
  legible and trustworthy.
- Generated products must provide calm, content-first, platform-native
  experiences on iPhone and iPad.

Without a shared language, these decisions are repeated inconsistently. With
too much abstraction, the factory becomes a second product and slows delivery.

## Users

- Factory operators reviewing work, evidence, failures, and approvals.
- Product users interacting with generated iPhone/iPad applications.
- Product designers and developers implementing product increments.
- Agents receiving design constraints and acceptance criteria.

## Goals

- Establish a small, reusable interaction and visual foundation.
- Make operator status and product intent understandable at a glance.
- Treat iPad as a distinct workspace, not a scaled-up iPhone.
- Make Dynamic Type, VoiceOver, Dark Mode, reduced motion, keyboard, pointer,
  and Apple Pencil support part of the baseline.
- Reduce repeated design decisions without flattening product identity.
- Prove value through one operator reference slice and one product reference
  slice before extracting reusable code.

## Non-goals

- A universal visual theme for every product.
- A web dashboard, design-token service, or component platform as a first step.
- Replacing product-specific UX judgment.
- Optimizing visual consistency above usability, safety, or accessibility.
- Adding factory infrastructure without a current product or reliability need.

## Design split

### Operator system

Purpose: help a trusted operator understand what happened, what is safe, and
what action is available next.

Character: calm control room.

Default qualities: high signal, explicit state, evidence-first, reversible
actions, restrained color, dense but readable information.

### Product system

Purpose: help an end user accomplish a meaningful task with low cognitive load.

Character: calm, tactile, human software.

Default qualities: content-first, obvious primary action, progressive
disclosure, direct manipulation, warmth, platform conventions, and product-
specific expression.

## Success criteria

- A reference operator workflow and a reference product workflow use the
  principles and checklist in this directory.
- Common states have a documented visual and interaction treatment.
- The product reference works on both iPhone and iPad without a desktop-style
  compression of the interface.
- Accessibility review occurs before a reference slice is accepted.
- Reusable code is extracted only after a pattern appears in at least two
  validated contexts or removes a measured repeated friction.
- Factory design work remains subject to the existing 10% steady-state effort
  cap and factory-change gate.

## Acceptance criteria

- `docs/design-language/principles.md` defines the shared principles and their
  deliberate operator/product differences.
- `docs/design-language/operator-system.md` defines the operator reference
  surfaces and state vocabulary.
- `docs/design-language/product-system.md` defines iPhone/iPad product rules.
- `docs/design-language/tokens.md`, `interaction-patterns.md`, and
  `accessibility.md` define the minimum foundation.
- `docs/design-language/review-checklist.md` can be used in a design review
  without relying on undocumented context.
- No UI framework or factory runtime is added by this increment.

## Rollout

1. Apply the language to one operator workflow: queue, run detail, evidence,
   blocked/failed state, and approval.
2. Apply the language to one `product-a` flow, including iPhone and iPad
   layouts plus empty, loading, error, and success states.
3. Record findings and extract only proven reusable primitives.

## Measures

- First-pass visual review rate.
- Design defects found before acceptance.
- Human minutes spent resolving repeated design decisions.
- Time to implement a common product flow.
- Accessibility issues found before device/TestFlight acceptance.
- Factory design effort share.

The primary objective remains the factory North Star: verified human value per
unit of human attention, risk, and cost.
