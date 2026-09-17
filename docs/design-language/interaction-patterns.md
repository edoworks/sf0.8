# Interaction Patterns

## Primary action

One action is primary on a surface. It has a clear label or familiar symbol,
an accessible name, a sufficient target, and a visible result.

## Navigation

- Use hierarchical navigation for drilling into one item.
- Use tabs for peer destinations users switch between frequently.
- Use sidebars and split views on iPad when persistent context helps.
- Use sheets for focused, temporary tasks rather than arbitrary navigation.

## Feedback

Every meaningful action should provide at least one of:

- Visible state change
- Position or selection change
- Haptic feedback where appropriate
- Audio feedback where appropriate
- Status text or accessibility announcement

Feedback must not be the only indication for users who cannot perceive it.

## Forms and input

- Use labels that remain available after input begins.
- Validate near the relevant field and explain how to recover.
- Preserve entered data when validation fails.
- Use the correct keyboard and input type.
- Support keyboard focus order and submit actions where relevant.

## Lists and collections

- Make the primary content and selection state obvious.
- Keep swipe actions supplemental, not the only route to important behavior.
- Provide a visible alternative for drag, reorder, and delete actions.
- Explain empty, filtered-empty, loading, and unavailable states separately.

## Sheets and confirmation

Use a confirmation when an action is destructive, external-impacting, costly,
or difficult to reverse. Do not confirm routine, reversible actions merely to
add ceremony.

## Errors and uncertainty

State what happened, whether the user's work is safe, and what can happen next.
For uncertain product output, use calibrated language and a useful fallback;
do not imply confidence the system does not have.
