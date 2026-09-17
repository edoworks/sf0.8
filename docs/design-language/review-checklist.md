# Design Review Checklist

Use this checklist for the operator and product reference slices. A failed item
is either fixed, explicitly deferred with a reason, or recorded as a product
decision before acceptance.

## Intent

- [ ] The user and primary task are stated.
- [ ] The primary action is obvious.
- [ ] The surface has a clear information hierarchy.
- [ ] Product-specific personality is distinguishable from shared foundation.

## State and behavior

- [ ] Loading, empty, success, error, blocked, and unavailable states are
      defined where relevant.
- [ ] The user can tell whether work was saved or completed.
- [ ] Error recovery explains what happened and what to do next.
- [ ] Important actions have visible feedback.
- [ ] Destructive or external-impact actions are explicit and reversible where
      possible.

## Platform fit

- [ ] iPhone layout is usable without relying on an iPad layout being scaled
      down.
- [ ] iPad uses additional space to preserve context or reduce navigation.
- [ ] Standard platform navigation and input behavior is used unless a reason
      for deviation is documented.
- [ ] Keyboard, pointer, Pencil, or drag-and-drop support is included when the
      product's task calls for it.

## Accessibility

- [ ] Dynamic Type does not clip or hide essential content.
- [ ] VoiceOver labels and focus order are meaningful.
- [ ] State is not communicated by color alone.
- [ ] Touch targets are usable.
- [ ] Reduced motion has been checked.
- [ ] Light and dark appearances have been checked.

## Operator-specific

- [ ] Current state, evidence, timestamp, and source are distinguishable.
- [ ] The next safe action is visible.
- [ ] Unknown, stale, blocked, and failed states are not conflated.
- [ ] Audit or recovery context is reachable without losing the current item.

## Evidence

- [ ] Screenshots or simulator/device evidence cover the reference states.
- [ ] Findings are recorded in the relevant product handoff or decision file.
- [ ] Any reusable abstraction has a measured or repeated reason to exist.
- [ ] The change remains within the factory effort and change gates.
