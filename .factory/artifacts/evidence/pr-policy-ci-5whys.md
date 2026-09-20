# PR Policy CI Failure: 5-Whys

Date: 2026-09-20

## Scope

- Audience: sf0.8 owner and maintainers.
- Decision: explain and correct PR #61's changed-path policy failure without
  weakening fail-closed ledger coverage.
- Evidence cutoff: 2026-09-20; PR head `06ac7f9`; CI run `35485674028`.
- Stopping rule: stop when the complete PR range passes with every gated path
  claimed exactly once by a currently bound ledger and historical malformed
  ledgers no longer act as current authority.

## Evidence

- CI failed in `validate-ci-change.py` with unclaimed gated paths and malformed
  historical issue 31–33 records.
- The validator correctly computes the pull-request range as
  `1ae04bf...06ac7f9`; the failure is not a one-commit-range defect.
- Existing issue 31–33 ledger records lack current `issue`/`capability` and
  `changed_paths` fields, while issue 52 is superseded by issue 59's binding.
- The complete range contains verified paths from several earlier increments;
  no current checkpoint ledger claimed the remaining paths.

## 5-Whys

1. **Why did PR #61 fail policy CI?** The complete range contained gated paths
   that were unclaimed, and malformed historical ledgers were validated as if
   they were current records.
2. **Why were historical records treated as current?** The validator loaded
   every ledger file changed in the range without first checking whether its
   issue remained in the current capability binding.
3. **Why were remaining paths unclaimed?** The prior increments had individual
   ledgers, but the cumulative PR had no current checkpoint ledger for paths
   outside those ledgers.
4. **Why was this not detected on earlier pushes?** Push validation examined
   each incremental event range; the pull-request gate is the first control
   that evaluates the full merge-base range.
5. **Why did the workflow lack a cumulative checkpoint contract?** The design
   specified complete event ranges but did not specify how superseded ledgers
   and a multi-increment checkpoint compose. Evidence ends here.

## Corrections

- Immediate: add issue-56's current binding and checkpoint ledger for every
  remaining gated path, with no wildcard claims.
- Root cause: filter ledger records to issues present in the current capability
  binding before validation; superseded historical records remain preserved but
  are not authority.
- Recurrence guard: test that an unbound malformed historical ledger is ignored,
  a current record claims the path, and the complete PR range fails if any gated
  path is still unclaimed or multiply claimed.

## Counterevidence And Unknowns

- The PR's policy job may expose additional failures after this gate passes;
  those would be separate findings.
- This correction does not authorize merge, review bypass, or direct protected
  branch mutation.
