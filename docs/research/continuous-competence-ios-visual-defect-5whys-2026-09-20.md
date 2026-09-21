# 5-Whys: Native Experiment Dark-Mode Contrast Defect

Date: 2026-09-20
Scope: local simulator verification of the native experiment artifact.

## Observed failure

The iPhone simulator rendered a light card with nearly white primary text and
white segmented-control labels under the host's dark appearance. The initial
screen was difficult to read.

## Evidence-based chain

1. **Why** was the card text nearly invisible? The view inherited dark-mode
   foreground colors while its custom background remained light.
2. **Why** did it inherit those colors? The experiment set a light visual
   background but did not declare an explicit color-scheme policy.
3. **Why** was the policy absent? The first implementation verified structure
   and compilation before rendering under the simulator's active appearance.
4. **Why** did compilation pass despite the defect? Color contrast is a runtime
   presentation property, not a Swift compiler or unit-test property.
5. **Why** was it not caught earlier? The native artifact had no visual
   snapshot or simulator screenshot checkpoint before this session.

## Correction and recurrence guard

- Immediate correction: apply `.preferredColorScheme(.light)` to the experiment
  navigation surface so the intentionally light research canvas has readable
  system text.
- Root-cause correction: require simulator screenshot review for both iPhone
  and iPad before treating a SwiftUI experiment surface as verified.
- Mechanical guard: retain the `macos-screenshot` workflow as an explicit
  evidence step and add a static test requiring the experiment's explicit color
  scheme declaration.

## Boundary

This is an experiment-surface defect, not evidence about the learning
intervention or product demand. No external release or publication occurred.
