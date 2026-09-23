# Now

Status: `IN_PROGRESS`

This is a visibility aid. `.factory/continuation-state.json` and
`.factory/portfolio.yaml` are authoritative.

## Now

- Active map: issue #48, organization repository and public-state
  reconciliation.
- Active increment: issue #51, website state-claim corrections.
- Issue #50 is integrated and closed. Public inventory is freshness-bounded;
  inaccessible private completeness remains `UNKNOWN`.
- Corrected Edoworks website source is merged and deployed. Corrected Foculoom
  source is committed, pushed, independently approved, and blocked by an
  unidentified `master` branch requirement.

## Next

- Inspect and satisfy the effective Foculoom `master` branch requirement without
  policy bypass, then merge PR #184 normally.
- Verify deployed Foculoom URLs against the merged revision, then close issue
  #51.
- Continue to repository metadata and release claims (#52), then final
  cross-surface review (#53).

## Blocked

- Foculoom PR #184 is mergeable, green, and approved at `00a9458`, but normal
  merge, squash, and rebase remain blocked by the organization-wide `Restrict
  updates` rule. Auto-merge is enabled and queued, but normal merge requires an
  explicit bypass prohibited by this lane. A permanent policy design is needed.
- Private predecessor issue inventories remain unauthenticated and `UNKNOWN`;
  issue #16 remains effectively `BLOCKED`.
- Apple credentials, upload, submission, and physical-device validation remain
  outside this lane.

## Preserved Work

- Existing dirty Edoworks website logo/contact changes were not modified or
  included in the issue #51 branch.
- Product A remains shelved and predecessor factories remain read-only.
