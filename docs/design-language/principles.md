# Design Principles

These principles apply to both systems. The examples show where the emphasis
differs.

## 1. Make the next action obvious

Every important surface should have one visually primary action or a clearly
stated reason that no action is available.

- Operator: show the next safe review or recovery action.
- Product: show the next useful user action.

## 2. Let content and evidence dominate controls

Controls frame the work. They should not compete with the artifact, evidence,
canvas, recording, document, or timeline being viewed.

## 3. Reveal complexity progressively

Start with the minimum needed for the current decision. Advanced controls,
diagnostics, and configuration should be available without becoming the first
thing every user must understand.

## 4. Preserve spatial context

Transitions, sidebars, breadcrumbs, and persistent context should explain where
the user came from and where an item belongs. Do not make users reconstruct
context after every navigation step.

## 5. Prefer platform conventions over novelty

Use familiar navigation, sheets, lists, search, system pickers, keyboard
shortcuts, pointer behavior, Apple Pencil behavior, and drag and drop unless a
custom interaction provides a clear benefit.

## 6. Make state visible

Saved, syncing, running, blocked, failed, unavailable, partial, and verified
must be distinguishable without relying on color alone.

- Operator: state must be auditable and evidence-linked.
- Product: state should be reassuring and understandable without jargon.

## 7. Use motion to explain, not decorate

Animation should preserve continuity, confirm an action, or communicate state.
It must not delay routine work or replace text and structure.

## 8. Design iPad as a workspace

Use sidebars, columns, persistent context, keyboard, pointer, Pencil, and
resizable layouts where they reduce navigation or improve understanding. Do
not simply stretch an iPhone screen.

## 9. Accessibility is part of the design

Semantics, focus order, target size, contrast, Dynamic Type, reduced motion, and
input alternatives are acceptance criteria, not polish work.

## 10. Add abstraction only after evidence

Prefer deletion, consolidation, and platform capability before a new shared
component or factory mechanism. A reusable pattern must pay rent through
repeated use, reduced friction, or a safety/reliability improvement.
