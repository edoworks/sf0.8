# Repository inventory root-cause analysis

Date: 2026-09-23
Tracker: edoworks/factory#50

## Defect

The obligation manifest queried `edoworks/sf0.7` and `edoworks/sf0.5`, then interpreted inaccessible or absent results as proof that no predecessor obligations existed. The portfolio also lacked most public repositories and contradicted documented lifecycle state.

## Why chain

1. Predecessor obligations were reported as zero because the manifest queried repository identifiers with the wrong organization owner.
2. The wrong identifiers persisted because no validator cross-checked the manifest against the canonical portfolio predecessor records.
3. The failed lookups became `non-existent` because inaccessible, absent, and empty states were collapsed into one classification.
4. That classification was accepted because repository coverage had no checked-in source record with completeness and access-boundary fields.
5. Portfolio contradictions persisted because lifecycle checks enforced factory authority but not repository-inventory coverage or field agreement.

## Corrections

- Immediate: use the canonical `foculoom/*` predecessor identifiers, mark remote issue counts `UNKNOWN`, and mark the manifest incomplete.
- Root cause: add a checked-in public/private inventory boundary and cross-check it against the portfolio and obligation manifest.
- Recurrence guard: `scripts/validate-repository-inventory.py` rejects wrong owners, false private completeness, stale or future-dated snapshots, public count drift, portfolio disagreement, contradictory lifecycle fields, inaccurate obligation totals, and numeric counts for blocked predecessors. Its negative tests exercise each failure class.

Private repository completeness remains blocked by authenticated organization-wide enumeration policy. No claim is made beyond known local repositories.

## Failed verification analysis

PR #121 initially failed the changed-path ecosystem gate.

1. The gate failed because three changed policy paths were not claimed by an increment ledger.
2. They were unclaimed because factory issue #50 had no sf0.8 control-plane capability binding or ledger.
3. The binding was absent because creating the cross-repository tracker did not automatically update this repository's local control plane.
4. The omission reached CI because local verification ran content validators but not the exact committed PR revision-range gate.
5. Evidence stops there; no claim is made about why the established pre-push checklist did not include that command.

Immediate correction: bind issue #50 and add its changed-path ledger. Root-cause correction: run `validate-ci-change.py` against the exact base and committed head before every retry. The existing CI guard detected the failure class and remains the recurrence control.
