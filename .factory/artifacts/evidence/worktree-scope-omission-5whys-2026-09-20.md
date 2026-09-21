# Worktree Scope Omission 5-Whys

Date: 2026-09-20
Audience: repository owner, maintainers, and future continuation agents.
Jurisdiction: local Git metadata, sf0.8 portfolio/governance records, and
continuation behavior. No external lifecycle or deletion authority is inferred.
Decision: determine why prior sessions ignored registered worktrees and
seemingly unrelated portfolio checkouts, and define a recurrence guard.
Cutoff: 2026-09-20.

## Research Charter

- Known facts: `sf0.8` has one registered worktree; `sf0.5` has four additional
  temporary worktree records, all marked prunable; `sf0.5`, `sf0.7`, and Product
  A are dirty local checkouts; `.factory/portfolio.yaml` lists their paths and
  read-only dispositions.
- Open questions: which prior session made or abandoned each temporary worktree;
  whether any dirty path contains a currently needed change; whether all
  historical roots were intentionally excluded in each prior turn.
- Hypotheses: the active-repository mental model hid portfolio roots; the
  continuation sequence did not require cross-root enumeration; and the word
  "unrelated" was used as a disposition without recording a path-level check.
- Stopping rule: stop when the omission path is demonstrated by direct Git and
  instruction evidence, and do not infer authorship or safe cleanup.

## 5-Whys

1. **Why were previous worktrees or other changes ignored?** The session
   inspected the active `sf0.8` checkout and treated other paths as unrelated
   without first producing a complete path inventory.
2. **Why was the inventory incomplete?** The restart sequence required
   `git status` in `sf0.8` and a later portfolio disposition check, but did not
   require `git worktree list` or status checks for every existing portfolio
   checkout.
3. **Why did `git worktree list` in the active repository not catch the issue?**
   Git worktree metadata is repository-local. It cannot enumerate separate
   repositories such as `sf0.5`, `sf0.7`, or Product A; `sf0.5` in fact contains
   prunable linked worktree records that are invisible from `sf0.8`.
4. **Why was a prose portfolio reference insufficient?** The workflow had no
   required output that distinguished active, historical/read-only,
   unrelated-but-preserved, and blocked paths. "Unrelated" therefore became a
   silent exclusion rather than an evidence-backed classification.
5. **Root cause supported by evidence:** continuation scope was defined around
   the current checkout, while the repository's actual operating scope spans a
   portfolio of local roots and repository-local worktree metadata. No
   cross-root preflight contract enforced enumeration and classification.

## Counterevidence And Limits

- Product A, `sf0.7`, and `sf0.5` are explicitly read-only or shelved. Ignoring
  them for product implementation can be correct; ignoring them for scope
  discovery and preservation status is not supported by that disposition.
- The evidence does not establish who created the prunable worktrees or that
  their contents are safe to recover. No cleanup, pruning, reset, or checkout
  was performed.
- The user's report is lead-only historical evidence; the local Git and policy
  observations are direct evidence.

## Correction And Guard

- Immediate correction: add a mandatory read-only scope preflight to the
  continuation sequence. It enumerates active-repository worktrees and all
  existing local portfolio roots, records status and prunable/detached entries,
  and requires an explicit classification for each path.
- Root-cause correction: make cross-repository scope a first-class continuation
  input instead of relying on the current checkout plus conversational memory.
- Mechanical guard: `tests/test_continuation_contract.py` now fails if the
  continuation contract omits the preflight, portfolio path fields, or the
  no-silent-ignore rule.
- Verification: the guard is run as part of the focused continuation contract
  test after this change. The stale worktrees remain preserved and unresolved.
