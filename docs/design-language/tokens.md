# Foundation Tokens

Tokens describe roles and relationships. They are not a promise that every
product uses the same literal values.

## Color roles

Define semantic roles rather than component-specific colors:

- `background.primary`
- `background.secondary`
- `surface.primary`
- `surface.grouped`
- `content.primary`
- `content.secondary`
- `content.muted`
- `accent.primary`
- `state.success`
- `state.warning`
- `state.danger`
- `state.info`
- `focus.indicator`

Every state color requires a non-color cue such as text, icon, shape, or
position. Light and dark values must be tested for contrast.

## Typography roles

Use semantic roles that map to Dynamic Type:

- Display or hero value
- Screen title
- Section title
- Body primary
- Body secondary
- Label
- Caption
- Monospaced evidence or identifier

Do not hard-code text sizes where a Dynamic Type style is appropriate.

## Spacing roles

Use a small base rhythm and named roles:

- Inline gap
- Control gap
- Group gap
- Section gap
- Screen inset
- Minimum touch target

The exact rhythm may vary by product, but ad hoc values should not become a
second undocumented system.

## Shape and elevation

- Use corner radius to communicate grouping and touchability, not as universal
  decoration.
- Use borders, grouping, and typography before shadows to establish hierarchy.
- Motion and elevation must not be required to understand state.

## Motion roles

- `motion.confirm`: short feedback after a completed action.
- `motion.transition`: preserves spatial continuity.
- `motion.progress`: communicates ongoing work.
- `motion.delight`: optional product expression, never required for meaning.

Every nonessential motion has a reduced-motion behavior.
