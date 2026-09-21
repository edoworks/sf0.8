# Host Audio Replay Result Semantics 5-Whys

Date: 2026-09-20
Issue: #75

## Defect

The first replay contract used `ABSTAIN` as a fixture status and the Python
validator accepted `PASS`, `FAIL`, or `ABSTAIN` without failing a report that
contained `FAIL`. A structurally valid report therefore did not mechanically
establish that fixtures met their declared expectations.

## Evidence-Based 5-Whys

1. Why could an unmet fixture expectation pass report validation? The validator
   checked shape, hashes, and allowed status values but did not reject `FAIL`.
2. Why was `FAIL` not rejected? The report field represented the classifier
   outcome and the fixture test outcome at the same time.
3. Why were those concepts conflated? The original manifest declared target
   labels but did not declare whether each fixture should produce target,
   non-target, or abstention behavior.
4. Why did tests not catch the ambiguity? They covered label matching and report
   structure independently, not an end-to-end expected-decision comparison.
5. Evidence ends at the initial contract and test design; no deeper cause is
   established.

## Corrections

- Immediate correction: reports now separate classifier `decision` from
  fixture `status`.
- Root-cause correction: every fixture declares an `expected_decision` of
  `TARGET`, `NON_TARGET`, or `ABSTAIN`; status is only `PASS` or `FAIL`.
- Recurrence guard: Swift tests cover decision/expectation mismatch and the
  Python validator rejects every failed fixture.

## Verification

- Nine Swift tests pass.
- The generated non-target speech smoke fixture produced `ABSTAIN`, matched its
  declared expectation, emitted `PASS`, and passed hash/report validation.
- The approved real-meow fixture gate remains open and human-authorized; this
  smoke result is not cat-detection evidence.
