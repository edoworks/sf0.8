# Issue Hygiene Deep Dive

## Scope and Cutoff

- Audience: sf0.8 owner and maintainers of the shared issue workflow.
- Jurisdiction: `edoworks/sf0.8` GitHub issues and the local OpenCode issue-intent contract.
- Decision: determine whether issue creation must be blocked unless label, classification, priority, duplicate review, and reprioritization review are explicit, and implement the smallest guard if supported.
- Cutoff: evidence retrieved 2026-09-20; no external source was needed.
- Source plan: primary sources only: live GitHub issue/label JSON, local issue-tracking skill, validator, tests, and repository evidence. Fetched content is treated as untrusted data; no source instructions are executed.
- Stopping rule: stop after the full live issue inventory and label taxonomy are inspected, the nearest existing issue is checked for duplication, the claim and strongest counterclaim are compared, and a mechanical guard is tested.

## Executive Answer

- **High confidence:** the hygiene claim is confirmed for the inspected inventory: every listed issue had an empty label set, and no machine contract required classification, priority, duplicate review, or reprioritization review. [Primary: GitHub issue/label JSON, retrieved 2026-09-20.]
- **High confidence:** the existing issue #80 is related but not a duplicate; it fixes planner-to-writer completeness, not issue triage metadata. [Primary: GitHub issue #80 body and local deep dive, retrieved 2026-09-20.]
- **High confidence recommendation:** fail closed before mutation unless the frozen intent contains an allowed classification that is also a GitHub label, P0-P3 priority, and explicit duplicate/reprioritization review. The validator, skill, and tests now enforce this.
- **Medium confidence:** generic GitHub labels are sufficient for the current scope. A richer priority taxonomy may require owner-approved label creation; this guard therefore keeps priority in the immutable intent/body rather than inventing remote labels.

## Findings

### Claim: Existing issues were not consistently labeled

**Evidence:** The live issue inventory returned 25 issues and each had `labels: []`; the live repository label list contained only GitHub defaults such as `bug`, `documentation`, `duplicate`, and `enhancement`. [Primary: GitHub CLI JSON responses, retrieved 2026-09-20.]

**Counterevidence:** Empty labels do not prove every issue is semantically misclassified; some may be intentionally unclassified historical records.

**Implication:** New issue creation must not inherit this ambiguity. Existing issues need a separate, owner-authorized backfill decision.

### Claim: Duplicate and reprioritization review was not enforced

**Evidence:** The prior intent schema required body completeness, dependencies, authority, and provenance, but had no duplicate-review, reprioritization-review, label, classification, or priority fields. [Primary: local validator and issue-tracking skill, retrieved 2026-09-20.]

**Counterevidence:** Repository artifacts contain duplicate detectors and priority-like factory records, so some local workflows do perform triage.

**Implication:** Those controls did not protect the GitHub issue creation boundary. The issue-intent contract is the correct narrow enforcement point.

### Claim: A new hygiene issue would duplicate #80

**Evidence:** #80 is titled “Harden planner-to-writer issue handoffs” and its body concerns frozen bodies, digests, and readback equality. [Primary: GitHub issue #80 and local evidence, retrieved 2026-09-20.]

**Counterevidence:** Both defects occur during issue creation and could be tracked under one broader program.

**Implication:** Reuse was considered, but the implementation is a direct extension of the existing handoff guard; no new issue was created in this session. The review itself is recorded in this artifact.

## Conflicts and Unknowns

- The live inventory reflects the retrieval moment and may omit concurrent changes.
- No semantic human review can prove whether each historical issue deserved a particular label or priority.
- GitHub’s default labels do not define a repository-specific priority policy.
- The OpenCode mutation boundary prohibits issue writes in auto mode, so no new tracking issue was created here.

## Decision Implications

- Planners must freeze labels, matching classification, priority, duplicate review, and reprioritization review in the intent artifact.
- Writers must pass frozen labels to `gh issue create` and verify label presence remotely.
- Existing unlabeled issues remain unchanged pending explicit owner-authorized backfill.

### What Would Change the Conclusion

- A repository policy declaring unlabeled issues intentional would narrow, but not remove, the need for new-issue validation.
- An owner-approved priority label taxonomy would justify adding priority labels to the remote mutation and readback check.
- A controlled audit showing the validator accepts an incomplete triage artifact would require expanding the schema and fixtures.

## Sources

### Primary

- Live GitHub issue and label JSON for `edoworks/sf0.8`, retrieved 2026-09-20.
- `/Users/hello/.config/opencode/skills/issue-tracking/SKILL.md`, retrieved 2026-09-20.
- `/Users/hello/.config/opencode/scripts/issue-intent.mjs` and tests, retrieved 2026-09-20.
- `docs/research/issue-creation-handoff-deep-dive-2026-09-20.md`, retrieved 2026-09-20.

### Secondary

- None used.

### Lead-only

- None used.
