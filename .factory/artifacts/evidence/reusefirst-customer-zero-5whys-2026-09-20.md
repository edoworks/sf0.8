# ReuseFirst Customer Zero Gap

Date: 2026-09-20
Status: `EXTERNAL_METADATA_RECONCILIATION_REQUIRED`

## Finding

The factory has not demonstrated that it is consuming the released public
`reusefirst` artifact as a customer. Its internal `scripts/ecosystem_gates.py`
contains a richer, separately maintained evaluator, while the public artifact
contains an independent `reuse_gate.py` contract. The public README explicitly
describes those as separate implementations. The public manifest retrieved at
the pinned tag also reports `CANDIDATE_UNRELEASED` and
`publication_approved: false`, which conflicts with the local release records.

The first review found no product consumer. A subsequent bounded dogfood run
executed the pinned public entrypoint for the factory and all three listed
Customer Zero products, including a blocking negative case. The remaining
blocker is the contradictory canonical manifest metadata, not missing dogfood
evidence.

## 5-Whys

1. **Why is duplicate-artifact risk real?** Normal factory workflows import the
   internal evaluator, while the public `reusefirst` contract is not imported,
   pinned, or executed by those workflows.
2. **Why did the registry say the artifact had consumers?** It counted scripts
   that implement or consume the related internal capability as consumers of
   the public artifact.
3. **Why was that accepted?** Consumer evidence checked path existence but not
   whether the evidence exercised the canonical public entrypoint and revision.
4. **Why was release approval not blocked?** Publication validation checked
   provenance, license, safety, and approval, but had no Customer Zero gate
   requiring factory and product dogfood evidence.
5. **Root cause:** the lifecycle treated capability equivalence as artifact
   consumption and had no machine-checked customer-zero contract.

## Correction And Guard

- Immediate correction: keep ReuseFirst locally as `PUBLIC_CANDIDATE` with
  approval false until the canonical manifest and release metadata agree; do
  not claim publication approval from dogfood alone.
- Root correction: public release records now require verified factory use,
  at least one product consumer, and evidence for both.
- Recurrence guard: `PUBLIC_RELEASED` registry records fail validation unless
  `customer_zero.status` is `VERIFIED`, `factory_consumed` is true, and at
  least one product consumer is named.
- Completed dogfood work: consume the pinned public entrypoint in the factory
  and all three product workflows, run the contract fixtures, and record the
  verified result in `reusefirst-customer-zero-dogfood.json`.
- Remaining next action: reconcile the canonical manifest's
  `CANDIDATE_UNRELEASED` and `publication_approved: false` values with the
  externally visible release before changing local publication state.

## Sources

- Public entrypoint: `https://github.com/edoworks/artifacts/blob/reusefirst/v1.2.1/artifacts/reusefirst/reuse_gate.py`
- Public manifest: `https://github.com/edoworks/artifacts/blob/reusefirst/v1.2.1/artifacts/reusefirst/MANIFEST.json`
- Public README: `https://github.com/edoworks/artifacts/blob/reusefirst/v1.2.1/artifacts/reusefirst/README.md`
- Local registry: `.factory/artifacts/reuse-registry.json`
- Local release record: `.factory/artifacts/records/reuse-gate.json`
