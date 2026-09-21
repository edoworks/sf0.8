# Primitive Discovery Classification 5-Whys

Status: corrected during targeted verification

1. **Why did the Rendit classification test fail?** The classifier returned `INTERNAL_ADVANTAGE` instead of `DEVELOPER_PRIMITIVE`.
2. **Why?** It treated medium strategic sensitivity as an automatic internal classification.
3. **Why?** Classification and externalization risk were coupled in one shortcut.
4. **Why was that unsafe?** Strategic sensitivity should constrain the experiment gate, but it does not erase a distinct evidence-backed primitive hypothesis.
5. **Why could this recur?** Future candidates could be silently misclassified whenever a risk field was used as a market/evidence judgment.

Root cause: the classifier conflated strategic sensitivity with strategic surface classification.

Immediate correction: only `HIGH` sensitivity forces `INTERNAL_ADVANTAGE`; medium sensitivity remains separately visible while the externalization gate stays blocked or human-authorized as required.

Root-cause correction: keep evidence classification, strategic sensitivity, and externalization authorization as separate fields and validation paths.

Recurrence guard: `tests/test_primitive_discovery.py::test_problem_evidence_does_not_become_payment_evidence` asserts Rendit remains a developer-primitive hypothesis while payment remains `UNKNOWN`; the sensitive-capability test separately asserts authorization remains blocked.
