# 5-Whys: Native Experiment Generated Plist Failure

Date: 2026-09-20
Scope: first unsigned iOS simulator build of the native experiment.

## Observed failure

The SwiftUI target compiled but Xcode bundle validation failed because
`CompetenceCheck.app/Info.plist` was absent.

## Evidence-based chain

1. **Why** did validation fail? The app bundle did not contain `Info.plist`.
2. **Why** was it absent? The generated Xcode target did not produce an
   Info.plist output.
3. **Why** did the target omit it? `project.yml` declared plist keys but did
   not enable `GENERATE_INFOPLIST_FILE`.
4. **Why** was that omission not caught by the initial check? The first check
   reached compilation and did not require bundle validation as its terminal
   condition.
5. **Why** is this a recurrence risk? Future experiment scaffolds may repeat
   the same generated-project assumption unless the project contract and build
   command are tested together.

## Correction and recurrence guard

- Immediate correction: add `GENERATE_INFOPLIST_FILE: YES` to the generated
  target and regenerate the project.
- Root-cause correction: treat unsigned simulator bundle validation as part of
  the native experiment scaffold contract, not an optional release step.
- Mechanical guard: the README's canonical build command and the successful
  `xcodebuild build` verification are retained with this record; a future
  scaffold skill should reject a target without generated plist support.

## Boundary

This was a local build-contract defect. It does not change the product,
learning, market, or publication decision.
