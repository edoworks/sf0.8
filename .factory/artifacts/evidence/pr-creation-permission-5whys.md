# PR Creation Permission Root-Cause Review

Date: 2026-09-19

## Scope And Cutoff

- Audience: sf0.8 owner and operators.
- Jurisdiction: OpenCode 1.18.19 permission evaluation and the local
  `edoworks/sf0.8` GitHub workflow.
- Decision: determine why PR creation was denied after a purported permission
  fix and restore repository-scoped PR creation without broadening review,
  merge, close, API, or cross-repository authority.
- Source plan: inspect the effective config and denial log, verify matcher
  semantics in OpenCode's official permissions documentation, reproduce the
  exact glob resolution in the checked-in fixture, and test the corrected
  effective config.
- Stopping rule: stop when the observed denial is explained by primary evidence,
  the exact command resolves to the intended action, unsafe variants remain
  denied, and the real PR creation command succeeds or exposes a different
  evidenced blocker.

## Evidence

- OpenCode's official permissions documentation says granular rules use simple
  wildcards and the last matching rule wins. Primary source, retrieved
  2026-09-19: <https://opencode.ai/docs/permissions/>.
- The execution log records the real command resolving to `gh pr *` with action
  `deny`, not to the intended scoped rule. Primary local source, observed at
  `/Users/hello/.local/share/opencode/log/opencode.log:2213738`.
- The malformed rule was `gh pr create * --repo edoworks/sf0.8 *`, while the
  mandated command shape starts `gh pr create --repo edoworks/sf0.8 ...`.
  With simple glob semantics, the rule contains two literal spaces around `*`;
  it therefore does not match the repository-first command when `*` is empty.
- The fixture classified the exact repository-first PR command as `deny`, so
  its green test confirmed the defect instead of preventing it.

## 5-Whys

1. **Why was PR creation blocked after restart?** The command matched the broad
   `gh pr *` deny and did not match the scoped creation exception.
2. **Why did the scoped exception not match?** Its glob required content between
   `create` and `--repo`, but policy requires `--repo` immediately after
   `create`.
3. **Why was the malformed rule accepted as fixed?** Validation checked config
   syntax and a model fixture, not the exact production command against the
   effective GitHub-rule set.
4. **Why did the model fixture not expose the defect?** It explicitly listed
   the real sf0.8 creation command under expected denials and had no positive PR
   creation case.
5. **Why did the prior diagnosis blame a second host layer?** It inferred a new
   enforcement plane from the denial response without first checking the
   resolver's logged winning pattern. Evidence stops here; no separate host
   policy is needed to explain this PR-creation failure.

## Corrections

- Immediate correction: use the exact repository-first glob
  `gh pr create --repo edoworks/sf0.8 *`.
- Authority correction: allow only that repository-scoped creation operation;
  keep the broad deny, cross-repository creation, review, merge, close, and API
  paths unchanged.
- Root-cause correction: make the drift test compare all effective GitHub rules,
  not only issue/API rules.
- Recurrence guard: test the exact production command as allowed, a foreign
  repository as denied, and a non-repository-first sf0.8 command as denied.

## Counterevidence And Unknowns

- A separate execution layer can exist, but no such layer is needed to explain
  this event because the OpenCode log identifies the broad deny as the winning
  rule.
- Historical sessions created PRs under more permissive configurations; that
  proves GitHub and `gh` can create PRs, but does not prove the current rule was
  valid.
- PR review and merge are separate operations and remain outside this fix.

## What Would Change The Conclusion

The conclusion changes only if the corrected exact command logs a different
winning rule or reaches GitHub and receives an independent authentication,
authorization, ruleset, or validation error.
