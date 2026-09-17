# Accessibility Contract

Accessibility is a release requirement for both the operator system and product
system.

## Baseline

- Support Dynamic Type without clipping or hiding essential content.
- Provide VoiceOver labels, traits, values, and logical focus order.
- Maintain usable contrast in light and dark appearances.
- Do not communicate state by color alone.
- Provide touch targets of at least 44 by 44 points where practical.
- Support reduced motion and avoid flashing or attention traps.
- Support Bold Text and increased contrast where the platform exposes them.
- Ensure localization can expand labels and change text direction where needed.

## Input alternatives

Every gesture-dependent action needs an alternative through visible controls,
context menus, keyboard commands, or another suitable input path.

Products using Apple Pencil must provide a finger or control-based path for
essential actions. Operator surfaces must provide pointer and keyboard paths
for workflows that are not inherently touch-based.

## VoiceOver content model

Combined elements should communicate one meaningful unit when separate labels
would create noise. Separate elements when the user needs to act on them
independently.

Announcements should report meaningful state changes, not every animation.

## Verification

Each reference slice should include:

- Dynamic Type stress review.
- VoiceOver navigation review.
- Light and dark contrast review.
- Reduced-motion review.
- Keyboard and pointer review where applicable.
- Touch-target and orientation review.
