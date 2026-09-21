# FocusGate Permission Fixture Drift 5-Whys

Date: 2026-09-21

Failure: PR #89's policy check failed after unrelated local permission changes
were removed from its diff because the effective global policy contained
FocusGate and factory PR rules absent from sf0.8's canonical fixture.

1. **Why did policy validation fail?** The effective rule list and checked-in
   fixture differed by eight repo-scoped PR rules.
2. **Why did the fixture lack those rules?** The global policy was updated for
   the new factory and reference app before its fixture synchronization commit
   was integrated.
3. **Why did the drift block another change?** Every sf0.8 policy run validates
   the live effective configuration, so an unrelated PR cannot pass while the
   canonical fixture is stale.
4. **Why was the stale fixture not corrected earlier?** The local correction
   existed as commit `7c681af` on an unpushed branch ancestry and was not tracked
   through a dedicated issue and PR.
5. **Root cause supported by evidence:** permission-policy changes and fixture
   synchronization were not integrated atomically through the repository's
   reviewed PR path.

Immediate correction: integrate the existing repo-scoped fixture rules and
FocusGate negative-scope test under issue #90.

Root-cause correction: treat the effective policy and portable fixture as one
atomic increment; run the exact permission suite before completing any global
policy update.

Mechanical recurrence guard: `tests/test_permission_policy.py` compares the
effective rules with the fixture and verifies FocusGate commands remain denied
for other repositories.
