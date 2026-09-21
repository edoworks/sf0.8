# Tool Opportunity Ledger Validator 5-Whys

Date: 2026-09-19
Scope: local implementation verification
Status: corrected and guarded

## Observed failure

The first ledger validation run reported errors for valid list-shaped
provenance and for a valid `HYPOTHESIS` evidence item. The CLI also returned
`status: OK` while returning validation errors.

## 5-Whys

1. **Why did validation reject the initial evidence ledger?** The validator
   applied a string-only helper to list-shaped provenance and omitted
   `HYPOTHESIS` from the evidence vocabulary.
2. **Why did the validator use the wrong shape and vocabulary?** The initial
   implementation modeled provenance as a scalar and copied the narrower
   constitution vocabulary without accounting for opportunity hypotheses.
3. **Why was that not caught before the first run?** The initial fixture was
   authored from the schema design and had no passing-ledger test executed
   before the CLI validation.
4. **Why could the CLI appear successful despite errors?** The validation
   command constructed an unconditional `OK` status instead of deriving status
   from the error list.
5. **Root cause:** The new schema and validator were introduced together
   without a minimal valid fixture test and without fail-closed CLI status
   handling. No broader architectural cause is established by this single
   implementation failure.

## Correction and recurrence guard

- Immediate correction: accept non-empty provenance lists, add `HYPOTHESIS` to
  the evidence vocabulary, and return `INVALID` when errors exist.
- Root-cause correction: make the checked-in ledger the first validator
  fixture and exercise malformed provenance, repeated signals, missing
  external evidence, and prototype gating in `tests/test_tool_opportunities.py`.
- Mechanical guard: `python3 scripts/tool_opportunities.py validate` now fails
  closed, `scan` refuses invalid ledgers, and `validate-ecosystem.py` invokes
  the same validator in the existing CI ecosystem gate.

## Evidence

- Initial failure: local validator output during this increment.
- Corrected validation: `python3 scripts/tool_opportunities.py validate`.
- Scanner validation: `python3 scripts/tool_opportunities.py scan`.
- Targeted tests: `python3 -m unittest tests.test_tool_opportunities`.
- Full local suite: `python3 -m unittest discover -s tests -p 'test_*.py'` (208
  tests passed).

## Schema evolution guard

When Rendit gained externally sourced problem-category evidence, the prototype
gate test still expected the earlier missing-external-evidence error. The
validator was correct: economic evidence remained absent. The test now asserts
the economic gate directly, so future evidence-stage advancement cannot weaken
the no-prototype-without-economic-evidence rule.
