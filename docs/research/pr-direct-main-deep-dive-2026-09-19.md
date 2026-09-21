# Direct-to-Main Workflow Deep Dive

## Scope and Cutoff

- Audience: repository owner and maintainers of `edoworks/sf0.8`.
- Jurisdiction: this repository's local contribution policy and the public GitHub state of `edoworks/sf0.8`; not a legal or organizational policy determination.
- Decision to inform: whether pull-request requirements should be removed in favor of direct commits on `main`, and whether PR `#1` can be closed as part of that change.
- Date cutoff: 2026-09-19 (current date); repository state and public GitHub records are evaluated as retrieved.
- Source plan: inspect repository policy and validation code first; verify the live PR and branch state using read-only GitHub pages/API where permitted; search the strongest counterclaim that review gates are still mandatory; prefer primary sources and record retrieval dates.
- Stopping rule: stop when the local rule is identified, the live PR state is independently verified or access is blocked, and every material conclusion has evidence plus its strongest counterclaim. Do not infer authorization for an external mutation from research.

## Evidence Classification Before Search

### Known facts

- `CONTRIBUTING.md` currently states that a pull request is optional and must not block local progress.
- The same file says remote synchronization is optional and must not block local completion.
- The worktree contains pre-existing modifications unrelated to this request.

### Open questions

- Is PR `#1` open, merged, or already closed?
- Does any other local validator or branch protection document still require a pull request?
- Is direct-to-main operation authorized by the repository's live GitHub ruleset?

### Hypotheses

- The requested removal has already been implemented locally, or only redundant wording remains.
- Closing PR `#1` would be an external repository mutation requiring an owner-authorized GitHub action, not a documentation edit.

### Recommendations pending evidence

- Preserve the existing optional-PR language unless a contradictory mandatory gate is found.
- Do not claim PR `#1` was closed unless a permitted, successful mutation and postcondition check exist.

## Findings

### Claim 1: The local contribution policy does not require pull requests

**Evidence:** Primary repository source, `CONTRIBUTING.md`, retrieved 2026-09-19, states: “A pull request is optional and must not block local progress.” It also states remote synchronization is optional and must not block local completion.

**Counterevidence:** The repository contains governance controls for protected-branch pushes, releases, deletion, visibility changes, and bypass operations. Those are not equivalent to a pull-request requirement but may still constrain direct pushes.

**Implication:** No local contribution-policy removal is justified from the currently inspected text.

### Claim 2: Closing PR `#1` is a separate external mutation

**Evidence:** Primary local governance source, `.factory/governance.yaml`, retrieved 2026-09-19, classifies destructive repository operations and protected actions as human-controlled. The active tool policy denies `gh pr` mutation commands. Direct read-only requests to both `https://github.com/edoworks/sf0.8/pull/1` and the GitHub REST endpoint for pull request `#1` returned `404` on 2026-09-19; this does not distinguish a nonexistent, private, or inaccessible PR.

**Counterevidence:** The user explicitly requested closing PR `#1`, which is evidence of intent but does not change the active execution permission boundary or prove the PR's current state.

**Implication:** This task can establish whether closure is appropriate, but cannot honestly report closure without an authorized mutation and verification.

### Claim 3: No remaining local file inspected here requires a pull request

**Evidence:** Primary repository sources, `.github/workflows/checks.yml` and `scripts/validate-review-contract.py`, retrieved 2026-09-19. The workflow triggers on both pull requests and pushes to `main`; the validator checks evidence, challenge, findings, concrete actions, and an implementation prompt, with no PR-presence requirement. Targeted repository search found no pull-request requirement in `.github/` or `scripts/`.

**Counterevidence:** GitHub branch protection or rulesets are external live state and were not readable through the permitted tool path. Local governance still protects sensitive branch and bypass operations.

**Implication:** No code or policy edit is warranted to “remove” a local PR requirement based on current evidence. Direct-to-main remains conditional on live GitHub branch controls and owner authorization.

## Conflicts and Unknowns

- Local policy favors optional PRs, while governance still preserves protected-branch and bypass safeguards. The documents are compatible but do not prove that direct pushes are currently allowed by GitHub.
- Live PR state and branch-protection state remain unknown. The public PR page and REST endpoint both returned `404`; the branches page returned `410`, so no positive state claim is made.

## Decision Implications

- Keep the current optional-PR and optional-sync wording unless another validator proves a contradiction.
- Treat PR `#1` closure as blocked external work under the current tool boundary; do not simulate or imply success.
- A conclusion would change if a local mandatory-review validator is found, if GitHub reports PR `#1` already closed/merged, or if an authorized mutation path becomes available and the postcondition is verified.

## Blocker 5-Whys

1. Why was PR `#1` not closed? The permitted execution path denies pull-request mutation commands.
2. Why does that prevent closure? Closing a PR changes external repository state and requires an authorized GitHub write.
3. Why is authorization not inferred from the request? The repository's governance requires owner-controlled protected actions and the live PR state was not positively established.
4. Why was live state not established? The permitted read-only public endpoints returned `404`/`410`, which is ambiguous without authenticated repository access.
5. Evidence stops here: the remaining cause is an authorization and visibility gap, not a demonstrated repository defect. Immediate correction is to preserve the accurate blocked status; root-cause correction requires an owner-authorized, identity-checked GitHub read/write path plus postcondition verification.

## Sources

### Primary

- Repository contribution policy: `CONTRIBUTING.md`, retrieved 2026-09-19.
- Repository governance policy: `.factory/governance.yaml`, retrieved 2026-09-19.
- Repository review command contract: `.opencode/commands/deepdive.md`, retrieved 2026-09-19.

### Secondary

- None used.

### Lead-only

- None used.
