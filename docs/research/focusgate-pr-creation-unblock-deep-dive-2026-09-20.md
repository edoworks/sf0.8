# FocusGate PR Creation Unblock Deep Dive

## Scope And Cutoff

- Audience: repository owner and operators responsible for the FocusGate
  reference-app PR.
- Jurisdiction: the local OpenCode permission configuration, GitHub CLI PR
  creation workflow, and `edoworks/focusgate` repository state.
- Decision: determine the smallest safe change that permits creation of the
  FocusGate PR without broadening unrelated GitHub mutations.
- Cutoff: 2026-09-20. Sources were retrieved or inspected on 2026-09-20.
- Source plan: inspect the FocusGate checkout and remote branch; verify the
  authenticated GitHub identity; read the official `gh pr create`, GitHub Flow,
  and OpenCode permission documentation; inspect the effective local rule set;
  then test the exact command after the narrow rule change.
- Stopping rule: stop when the branch is clean and pushed, identity is verified,
  the exact command has a repository-scoped allow rule, and PR creation either
  succeeds or produces an independent GitHub error. Do not broaden permissions
  or attempt review/merge operations in this increment.

## Evidence Classification

### Known Facts

- The FocusGate checkout is clean on `feature/focusgate-v0`, tracking the same
  remote branch at commit `50c906f`. Local primary source, inspected
  2026-09-20.
- `.factory-verify-result.json` records five passed gates: iPhone build, unit
  tests, iPad build, static analysis, and unsigned archive. Local primary
  artifact, inspected 2026-09-20.
- The authenticated GitHub identity is `hellofoculoom`. GitHub API primary
  observation, retrieved 2026-09-20.
- The effective permission set had `gh pr *` denied and no FocusGate-specific
  exception. Local configuration primary source, inspected 2026-09-20.
- The exact allow rule was added:
  `gh pr create --repo edoworks/focusgate *`.
  Local configuration primary source, changed 2026-09-20.

### Open Questions

- Whether GitHub will accept the PR under the repository's live rules, issue
  linkage, or required checks is unknown until the command reaches GitHub.
- Whether a PR already exists for this branch is unknown until a permitted PR
  list/view operation is available or creation is attempted.

### Hypotheses

- The blocker is local policy matching rather than branch or build readiness.
  Confidence: high, because the branch is pushed and the deny/allow rule set
  directly explains the blocked command.
- A draft PR is the safest first publication state. Confidence: medium,
  because GitHub Flow recommends PRs for collaboration and notes that drafts
  support early feedback, but the repository's live settings are not yet
  observed.

## Findings

### Claim 1: A narrow repository-scoped exception is sufficient

**Evidence:** OpenCode documents that permissions resolve to `allow`, `ask`, or
`deny`; patterns use simple wildcards; and the last matching rule wins. Primary
tool documentation, retrieved 2026-09-20:
<https://opencode.ai/docs/permissions/>. The current config places the new
FocusGate rule after the broad `gh pr *` deny. Local primary configuration,
inspected 2026-09-20.

**Counterevidence:** The config change alone cannot prove GitHub authorization,
repository rules, or duplicate-PR state. Those remain live external unknowns.

**Implication:** Do not allow general `gh pr`, `gh repo`, `gh api`, review,
merge, or cross-repository operations for this unblock.

### Claim 2: The branch is ready for PR creation at the local publication gate

**Evidence:** GitHub Flow describes creating a separate branch, committing and
pushing it, then creating a pull request for feedback. Primary GitHub
documentation, retrieved 2026-09-20:
<https://docs.github.com/en/get-started/using-github/github-flow>. The branch is
clean and pushed, and the factory verification receipt records five passes.
Local primary sources, inspected 2026-09-20.

**Counterevidence:** A passing local verification receipt does not establish
review approval, required checks, merge eligibility, or release readiness.

**Implication:** PR creation may proceed; review and merge remain separate
increments.

### Claim 3: The canonical CLI operation should be repository-explicit

**Evidence:** GitHub CLI's `gh pr create` documentation is the primary command
reference, retrieved 2026-09-20:
<https://cli.github.com/manual/gh_pr_create>. The local workflow policy and
prior root-cause record require repository-first command matching so the scoped
rule can be evaluated deterministically. Local primary evidence:
`.factory/artifacts/evidence/pr-creation-permission-5whys.md`, inspected
2026-09-20.

**Counterevidence:** CLI syntax does not guarantee the remote branch has a
compatible base or that GitHub accepts the request.

**Implication:** Use `gh pr create --repo edoworks/focusgate --base main
--head feature/focusgate-v0` with a concise body and draft status; treat any
GitHub response as new evidence.

## Conflicts And Unknowns

- Local evidence says the branch and verification gate are ready; live GitHub
  PR existence, repository settings, required checks, and issue linkage remain
  unobserved.
- GitHub Flow recommends review through a PR, while the current increment only
  authorizes creation. This is a sequencing boundary, not a contradiction.
- The FocusGate PRD states GitHub synchronization is outside the app's product
  scope. That product constraint does not prohibit using GitHub's development
  workflow for the repository itself.

## Decision Implications And What Would Change The Conclusion

- Proceed with the exact repository-scoped PR creation action after restarting
  OpenCode so the config change is loaded.
- If creation succeeds, record the PR URL and stop this increment; do not merge
  or claim completion until review and checks are separately verified.
- If creation reaches GitHub and fails, classify the new failure as
  authentication, authorization, repository state, duplicate PR, or validation
  evidence rather than expanding local permissions.
- The conclusion changes if the exact command still resolves to a deny, the
  authenticated identity differs from `hellofoculoom`, or GitHub reports a
  repository-specific requirement that requires a separate authorized action.

## Sources

### Primary

- OpenCode, “Permissions,” https://opencode.ai/docs/permissions/, retrieved
  2026-09-20. Source type: official tool documentation.
- GitHub, “GitHub flow,” https://docs.github.com/en/get-started/using-github/github-flow,
  retrieved 2026-09-20. Source type: official platform documentation.
- GitHub CLI, “gh pr create,” https://cli.github.com/manual/gh_pr_create,
  retrieved 2026-09-20. Source type: official CLI documentation.
- FocusGate checkout, branch state and `.factory-verify-result.json`, inspected
  2026-09-20. Source type: local primary repository evidence.
- `/Users/hello/.config/opencode/opencode.jsonc`, inspected and narrowly updated
  2026-09-20. Source type: local effective configuration.

### Secondary

- `.factory/artifacts/evidence/pr-creation-permission-5whys.md`, inspected
  2026-09-20. Source type: local root-cause analysis.
- `docs/research/pr-branch-merge-unblock-deep-dive-2026-09-19.md`, inspected
  2026-09-20. Source type: prior local research.

### Lead-Only

- None used. Search results and generated summaries were not treated as
  evidence.
