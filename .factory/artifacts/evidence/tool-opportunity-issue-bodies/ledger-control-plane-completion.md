Implemented and locally verified.

- Added `.factory/tool-opportunity-ledger.json`.
- Added `scripts/tool_opportunities.py` validation and scan commands.
- Bound capability `tool opportunity discovery` to this issue.
- Added `.factory/artifacts/ledger/issue-65.json` with reuse evidence.
- Integrated validation into `scripts/validate-ecosystem.py`.
- Verification: `validate-change.py --changed-ledgers` passed; ecosystem
  validation passed; full local suite passed with 208 tests.
- No publication, dependency installation, or external product action occurred.
