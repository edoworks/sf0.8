# Public Identity State Claim Case-Sensitivity 5-Whys

## Trigger

The focused scanner test did not detect `SKIPLET trademark status: REGISTERED`.

## Analysis

1. The state-claim regular expression returned no match because the canonical
   lookup key was lowercase while the surface used uppercase.
2. The expression interpolated the case-folded key but enabled case-insensitive
   matching only on the registered-symbol and registration-claim expressions.
3. State-claim parsing was added after those expressions and did not reuse a
   shared canonical-name matcher.
4. The initial scanner tests covered uppercase names for symbol and registration
   claims but not for an explicit state claim.

Evidence does not establish a deeper organizational cause.

## Corrections

- Immediate: make canonical-name/state matching case-insensitive and normalize
  the observed state before comparison.
- Recurrence guard: `test_textual_trademark_state_claim_is_checked` exercises an
  uppercase canonical name and state and must fail if matching becomes
  case-sensitive again.
