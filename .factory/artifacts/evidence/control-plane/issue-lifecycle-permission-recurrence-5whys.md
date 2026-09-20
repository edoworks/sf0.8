# Issue Lifecycle Permission Recurrence 5-Whys

## Observed Failures

- Issue 52 and 53 completion writes were denied after local verification passed.
- The close command combined identity and mutation with `&&`, which the final
  separator rule denies.
- A standalone close would still have been denied because only issue 50 was
  exempted from the default `gh issue *` denial.
- Issue 54 creation attempts with a multiline body and then an inline semicolon
  were denied by the newline and semicolon rules. A separator-free body passed.

## Analysis

1. Why were the completion writes blocked? Their commands matched final deny
   rules: the compound close contained `&&`, and standalone writes for issues
   52 and 53 had no matching exception.
2. Why was there no matching exception? The global policy encoded comment and
   close permission for literal issue 50 and one command ordering.
3. Why did the previous correction hardcode one issue? It represented the
   observed reconciliation command rather than the repository-scoped issue
   lifecycle authority boundary.
4. Why did regression testing accept that design? The portable fixture copied
   the issue-50 rules and asserted that another issue must be denied.
5. Why did the fixture not expose the drift? It tested only synthetic strings
   in its own data and never compared security-relevant rules with the resolved
   OpenCode configuration or a future canonical issue.

Evidence ends here. The surviving records do not establish why issue 50 was
selected as a permanent global permission boundary.

## Corrections

- Immediate: keep issues 52 and 53 open until a fresh session can perform each
  owner identity check and repository-scoped mutation separately.
- Root cause: replace issue-number exceptions with repository-first, repo-scoped
  `ask` rules for create, comment, and close. Keep other issue writes and every
  compound command denied.
- Alias boundary: deny generic `gh api` commands and allow only the exact owner
  identity query, preventing REST or GraphQL mutation from bypassing the issue,
  pull-request, and repository command rules.
- Workflow: never chain identity and mutation. Use `--body-file` for structured
  text so body content cannot collide with shell separator rules.
- Mechanical guard: reject issue-number literals and mutation `allow` rules,
  exercise arbitrary future issue numbers, deny wrong repositories and
  same-prefix repositories, reject noncanonical argument order, and compare the
  fixture against fresh resolved OpenCode configuration when it is available.

## Residual Boundary

OpenCode `--auto` approves `ask` rules. An auto-mode session therefore cannot
treat an issue mutation as human-authorized. Issue writes must remain disabled
in auto mode until a mode-sensitive hard boundary exists.
