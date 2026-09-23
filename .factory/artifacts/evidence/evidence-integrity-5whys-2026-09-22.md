# Evidence Integrity Guard: 5-Whys

Date: 2026-09-22
Issue: edoworks/factory#47
Status: corrective guard implemented; local verification passed

## Defect

The repository had typed PRD contracts for timeout outcomes, tracked evidence,
qualification dates, and cross-system state, but no single executable check
reconciled those records. A progressing timeout could be mistaken for a hang,
an untracked receipt could be cited as a gate input, and the qualification
ledger accepted a weekday label that contradicted its ISO date.

## Evidence-Based 5-Whys

1. Why could an invalid completion claim survive? The existing checks validated
   individual files and commands but did not reconcile their semantic state.
2. Why were the states not reconciled? Timeout receipts, evidence references,
   continuation text, and qualification entries had no shared validator.
3. Why was there no shared validator? Each contract was introduced as a local
   correction, so cross-system synchronization remained prose.
4. Why did prose not prevent drift? Passing tests and artifact existence were
   treated as sufficient without checking provenance, derived dates, or state
   transitions.
5. Evidence ends at the missing cross-system guard; no deeper organizational
   cause is established.

## Corrections

- Immediate: add `scripts/evidence_integrity.py` and the repository entrypoint
  `scripts/validate-evidence-integrity.py`.
- Root cause: derive weekdays from ISO dates, require tracked evidence and an
  explicit revision, classify timeouts from progress/process evidence, and
  reconcile continuation, control-plane, lifecycle, queue, and gate state.
- Recurrence guard: focused fixtures fail for progressing/no-progress timeout
  confusion, untracked evidence, continuation drift, and wrong weekday data;
  CI runs the canonical validator.

## Verification

- `python3 -m unittest tests.test_evidence_integrity` — 6 tests passed
- `python3 -m unittest discover -s tests -p 'test_*.py'` — 259 tests passed
- `python3 scripts/validate-evidence-integrity.py` — passed
- `python3 scripts/validate-lifecycle.py` — passed
- `python3 scripts/validate-control-plane-contract.py .factory/control-plane-requirements.json` — passed
