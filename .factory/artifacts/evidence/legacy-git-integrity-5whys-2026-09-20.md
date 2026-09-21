# Legacy Git Integrity Preservation 5-Whys

Date: 2026-09-20
Finding: read-only integrity checks reported dangling Git objects in sf0.7 and
sf0.5 before any proposed consolidation.

## Analysis

1. **Why is consolidation blocked?** Some historical commits, trees, tags, and
   blobs are not reachable from the currently advertised refs, so a migration
   could omit recoverable evidence.
2. **Why could migration omit them?** A normal ref-based mirror or directory
   copy preserves reachable history, not necessarily dangling objects.
3. **Why are dangling objects present?** The local check proves their presence,
   but does not establish whether they came from rebases, abandoned worktrees,
   checkpoints, or prior recovery operations.
4. **Why is the cause unresolved?** No owner-authorized object classification,
   reflog review, remote comparison, or release/evidence reachability audit has
   been performed.
5. **Stopping point:** Evidence is insufficient to claim corruption or loss.
   The supported conclusion is a preservation-risk blocker requiring
   classification before pruning, garbage collection, or migration.

## Correction And Guard

- Immediate correction: stop all cleanup and consolidation operations; retain
  the original repositories and record the `git fsck` result.
- Root-cause correction: before any migration, create an owner-approved object
  preservation manifest covering refs, reflogs where available, tags, LFS,
  release evidence, and dangling-object reachability.
- Mechanical guard: migration readiness must fail closed when `git fsck` reports
  dangling objects unless an explicit classification and preservation receipt is
  present.
