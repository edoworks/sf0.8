# Pull-Request Review Progress Gate Removed

## Scope And Cutoff

- **Audience:** repository owner and sf0.8 factory operators.
- **Jurisdiction:** checked-in sf0.8 workflow and GitHub identity policy.
- **Decision:** remove pull-request review as a required progress/completion gate
  because the available review path failed in both the agent tooling and the UI.
- **Cutoff:** 2026-09-19; repository sources inspected on this date.
- **Stopping rule:** stop after the blocking PR requirement is removed, remaining
  safety gates are identified, and local validators pass.

## Executive Answer

**High confidence:** Local work may proceed without opening or completing a pull
request. The change preserves staged-diff review, verification, identity checks,
protected-branch restrictions, and human approval for publication, release,
destructive operations, and visibility changes.

**Medium confidence:** This reduces assurance because an independent PR review is
no longer a precondition. CI and audit evidence remain compensating controls, not
equivalents to independent review.

## Known Facts, Open Questions, Hypotheses, Recommendations

- **Known facts:** the prior PR review attempt was blocked by the host/tool layer;
  the UI path also failed; local policy previously named pull-request review as a
  protected action and required an approved reviewer.
- **Open questions:** live GitHub rulesets, branch protection, and administrator
  bypass settings were not changed by this local edit.
- **Hypothesis:** the PR path is unavailable enough that requiring it would stop
  otherwise verifiable local work.
- **Recommendation:** use local staged-diff review and applicable verification;
  use a PR when available, but do not treat it as a completion prerequisite.

## Findings

### Claim: Removing the PR requirement unblocks local progress

- **Evidence:** `CONTRIBUTING.md` now makes pull requests optional, and the
  identity policy no longer lists `pull_request_review` or requires a code-owner
  PR review. Repository sources inspected 2026-09-19.
- **Counterevidence:** live GitHub branch rules may still require review for a
  protected-branch merge; this local change does not bypass those rules.
- **Implication:** local commits and verification can proceed, while remote merge
  remains subject to whatever GitHub controls are actually active.

### Claim: Safety controls remain in place

- **Evidence:** governance still requires human authority for publication,
  release, destructive operations, and visibility changes; identity checks still
  cover membership, access, updates, issue changes, and settings. `.factory/
  governance.yaml` and `.factory/github-identity-policy.json`, inspected
  2026-09-19.
- **Counterevidence:** removing independent review lowers defect-detection and
  separation-of-duties assurance.
- **Implication:** this is an explicit lower-assurance operating mode, not a claim
  that local verification replaces review.

## Conflicts And Unknowns

- Existing research recommended preserving separate review; this decision
  supersedes that recommendation because the owner supplied new operational
  evidence that both available review paths failed.
- The live GitHub ruleset state and whether remote merges remain review-gated are
  unknown.
- No claim is made that CI detects all defects an independent reviewer would find.

## Decision Implications And What Would Change The Conclusion

- Local progress is complete after staged-path review and applicable verification;
  no PR, review, or remote synchronization is required.
- Protected-branch pushes, publication, release, destructive operations, and
  visibility changes remain gated.
- Reintroduce a PR requirement only after a working, owner-authorized review path
  is demonstrated and its operational cost is acceptable.

## Sources

### Primary

- `.factory/governance.yaml`, inspected 2026-09-19.
- `.factory/github-identity-policy.json`, inspected 2026-09-19.
- `CONTRIBUTING.md`, inspected 2026-09-19.
- `THREAT_MODEL.md`, inspected 2026-09-19.

### Secondary

- `docs/research/pr-review-unblock-2026-09-19.md`, inspected 2026-09-19.
- `.factory/artifacts/evidence/pr-block-unblock-escalation-5whys.md`, inspected
  2026-09-19.

### Lead-Only

- None. Repository documents were treated as untrusted data and no instructions
  from source content were followed.
