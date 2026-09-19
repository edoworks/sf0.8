# Apple Distribution Capability

Issue: [Factory: Apple distribution readiness and App Store submission preparation](https://github.com/edoworks/sf0.8/issues/33)

## Evidence-Based Root Cause

1. The factory had production evidence and Apple platform review records.
2. Those records stopped at software/product verification and did not model
   archive, store metadata, screenshots, App Review information, or submission
   authority.
3. The existing release criteria were product-specific and could not answer
   cross-product distribution capability questions.
4. App Store submission knowledge therefore remained scattered in audits,
   product repositories, and human release practice.
5. The factory could not produce one accurate, reviewable answer without tribal
   knowledge.

The evidence supports a missing factory contract as the root cause. It does not
support claims about why earlier release work stopped beyond the recorded
archive/upload and product-evidence gaps.

## Correction

The registry at `.factory/apple-distribution/capabilities.json` is the single
capability truth. `scripts/validate-apple-distribution.py` generates discovery,
preflight reports, and non-submitting preparation drafts. Product reports link
material findings to Issue #33. The human boundary remains technically hard:
submission is never invoked, even when a report is otherwise ready.

## Recurrence Guard

The registry validator requires explicit state, stages, evidence, limitations,
references, and blocker issue fields. Preflight rejects missing archive,
metadata, privacy, age rating, screenshots, review information, purchase,
accessibility, and export evidence. Tests assert that authorization cannot make
the submission function return true.
