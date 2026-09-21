---
name: product-art-direction
description: Create a visual-language brief, define palette, typography, shape, illustration, and motion tokens, establish mascot rules, and produce anti-generic-design reviews for a product that needs a distinctive but restrained identity. Use when a product has a sound interaction model but an underdeveloped or generic visual identity.
license: Apache-2.0
compatibility: Local, advisory; never copy commercial mascots or fetch art at runtime.
metadata:
  version: "0.1.0"
  disposition: INTERNAL_REUSABLE_CANDIDATE
---

# Product Art Direction

Give a product a recognizable visual language without weakening its
interaction model. The goal is calm expressiveness, not visual noise.

## When to use

- A product is functional but visually generic: standard framework surfaces,
  system typography, default controls, and no distinctive identity.
- A mascot or character is proposed and needs guardrails and a design contract.
- A team needs semantic design tokens, component states, and motion rules.
- A design needs an anti-generic review before implementation.

## Visual-language brief structure

1. **Product metaphor.** Name the central metaphor that ties identity to
   function (e.g., a nest that safely holds parked thoughts).
2. **Palette.** Define semantic tokens with light and dark appearances:
   canvas, surface, surfaceRaised, ink, inkMuted, accent, warm accent, success,
   danger. Never use accent colors for body copy.
3. **Typography.** Preserve system typography and Dynamic Type. Identity comes
   from hierarchy, spacing, and weight, not custom fonts.
4. **Shape.** Define corner radii, surface boundaries, and shadow rules.
   Shadows are subtle, optional in dark mode, and never the only boundary.
5. **Iconography.** Define custom or system icon conventions and where
   decorative art is allowed.
6. **Motion.** Define when motion is permitted (transitions only), its maximum
   duration, Reduce Motion replacement, and what is prohibited (loops, sound,
  decorative animation).
7. **Voice.** Define confirmation, error, and empty-state copy tone.

## Mascot contract

If a character is proposed, define:

- **Role:** transition helper, not a virtual pet.
- **Personality:** warm, observant, quiet, competent.
- **Resting state:** small, static, secondary to the primary task.
- **Active states:** brief transition poses, no loops, no sound.
- **Prohibitions:** no care demands, hunger, mood, disappointment, urgency,
  punishment, diagnostic language, blocking controls, or required-state
  carriage.
- **Quiet Mode:** removes character imagery, copy, and decorative motion
  while preserving all functionality.
- **Accessibility:** decorative when not interactive; hidden from VoiceOver;
  never the only success or state signal.

## Anti-generic design review

Review a design against these failure signs:

- Standard framework surfaces with no product-specific treatment.
- Default system gradient or color as the only background.
- No semantic color tokens; raw colors hard-coded in feature views.
- No dark-mode treatment or unreadable dark-mode pairings.
- No custom iconography or motif tied to the product metaphor.
- No motion contract or Reduce Motion fallback.
- No voice or copy distinction from framework defaults.
- Mascot that is decorative clutter, demanding, or infantilizing.

## Token implementation rules

- Implement tokens centrally, not scattered in feature views.
- Support light and dark appearances in the asset catalog or an equivalent
  centralized theme.
- Confirm contrast against actual paired backgrounds, not assumed values.
- Target WCAG AA: 4.5:1 for normal text, 3:1 for large text.
- Use system red and native destructive semantics for destructive actions.
- Combine color with text, icon, or shape for every state.

## Skill boundaries

- This skill produces briefs, tokens, contracts, and reviews. It does not
  produce final illustrations or certify clinical effectiveness.
- All art must be local, original, and checked in. No commercial mascot
  copying, no runtime asset fetching, no third-party packages.
- A mascot system should not be promoted to a reusable skill until it reaches
  more than one product.