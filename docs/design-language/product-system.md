# Product System

The product system is the default language for generated iPhone/iPad products.
It provides a quality floor, not a mandatory brand identity.

## Product shell

- One primary task or destination should be visually dominant.
- Use standard navigation bars, tab bars, sheets, lists, and split views where
  they match the product's information structure.
- Keep important context visible on iPad through sidebars or columns.
- Preserve scroll position and selection context across navigation.
- Avoid hidden gestures for actions users must discover or use frequently.

## Core flow

Each reference flow should define:

- First meaningful action.
- Primary success state.
- Loading or processing state.
- Empty state.
- Error or recovery state.
- Offline or unavailable state when relevant.
- Confirmation or completion feedback.

## Visual direction

- Content-first layouts with strong typographic hierarchy.
- Generous spacing where it improves comprehension, not as decoration.
- Personality through type, illustration, sound, motion, or color used with
  purpose.
- Consistent semantic colors across light and dark appearances.
- Controls should be visually subordinate to the content they affect.

## Direct manipulation

Prefer manipulating the object itself when the metaphor is clear:

- Draw on the canvas.
- Reorder the task in the list.
- Annotate the page.
- Adjust the image in the preview.
- Move an item between visible groups.

Direct manipulation must have an accessible alternative and visible feedback.

## iPhone rules

- Prioritize one-handed reach for frequent actions.
- Keep primary actions within comfortable touch zones where possible.
- Use sheets and focused screens when additional context would create clutter.
- Avoid shrinking iPad multi-column layouts into unreadable stacks.

## iPad rules

- Treat landscape and portrait as supported compositions, not edge cases.
- Use extra width for context, comparison, and navigation reduction.
- Support hardware keyboard and pointer input when the product involves text,
  editing, or repeated workflows.
- Support Apple Pencil when the product involves writing, drawing, annotation,
  or precision selection.
- Use split views and sidebars when they reduce back-and-forth navigation.

## Product expression

The product may override the default palette, illustration style, sound, and
motion character. It should not casually override accessibility, state clarity,
platform conventions, or the primary-action rule.
