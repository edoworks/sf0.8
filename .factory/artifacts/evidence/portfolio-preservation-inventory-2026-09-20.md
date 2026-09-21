# Approved Historical Portfolio Preservation Inventory

Date: 2026-09-20
Scope: `edoworks/product-a`, `foculoom/sf0.7`, and `foculoom/sf0.5`
Purpose: read-only preservation and metadata inventory after the C-suite review
Authority: no merge, relocation, unarchive, reactivation, deletion, or source
copying is authorized by this record

## Inventory

| Repository | Local/source evidence | Revision/state | Preservation finding |
|---|---|---|---|
| `edoworks/product-a` | Preserved checkout at `/Users/hello/actions-runner-producta/_work/product-a/product-a`; origin `https://github.com/edoworks/product-a` | `ef94f2492d3e73d98fb883320bad2902c64f3e15`; dirty with source, UI-test, and automation-document changes; local object check passed; `HEAD...origin/main` cached comparison `0/0`; remote archive, branch, release, consumer, and permission state were not queried | Keep separate and read-only; retain PRD, handoff, history, verification, and unresolved release gates |
| `foculoom/sf0.7` | `/Users/hello/sf0.7`; remote `https://github.com/foculoom/sf0.7.git` | `8d0066a3f1123b18097ee8d945c5bf9e96e6a413`; dirty worktree with source, queue, log, deployment, and TestFlight evidence changes; `HEAD...origin/main` cached comparison `43/0`; `git fsck` reported dangling commits/blobs | Keep separate as deprecated historical factory evidence; do not copy, normalize, prune, or garbage-collect before dangling objects are classified |
| `foculoom/sf0.5` | `/Users/hello/sf0.5`; remote `github https://github.com/foculoom/sf0.5.git`; no `origin` remote | `993bc553bc65b8cf5a51cc5a2b165d235052aedb`; dirty worktree with README and visual evidence changes; three local heads; `HEAD...github/main` cached comparison `0/0`; no Git LFS files observed; `git fsck` reported many dangling commits, trees, tags, and blobs | Keep separate as frozen legacy evidence; remote recoverability and history obligations remain unknown; do not prune or garbage-collect |

## Evidence Sources

- `.factory/portfolio.yaml` classifies Product A as `keep_read_only`, sf0.7 as
  deprecated `keep_read_only`, and sf0.5 as frozen legacy `keep_read_only`.
- `docs/decisions/2026-09-17-product-a-shelved.md` requires explicit owner
  instruction for revival and preserves Product A history and evidence.
- `.factory/artifacts/portfolio-archaeology/inventory.json`,
  `preservation-manifests.json`, and `portfolio-reconciliation.json` preserve
  source paths, lifecycle evidence, and unresolved remote blockers.
- `scripts/audit-portfolio.py` was run into an approved temporary output path;
  it performed metadata discovery only and did not modify the three source
  repositories.
- Local metadata checks observed no Git LFS files in sf0.7 or sf0.5. This is not
  evidence that remote LFS objects, release assets, or external references do
  not exist.
- Local `git fsck --full --no-progress` completed without fatal corruption for
  all three checkouts. Dangling objects were reported in sf0.7 and sf0.5;
  dangling objects are preserved evidence until their provenance is classified,
  not disposable garbage.

## Decision

Approval of these repositories is treated as approval to inspect and preserve
metadata, not as authorization to consolidate them. No same-governance atomic
change graph, shared release boundary, clean worktree, remote consumer map,
license/IP review, or rollback plan has been established. A future migration
would require an explicit preservation or active-consolidation decision and
must retain each original source repository until parity and rollback checks
pass.

## Integrity Blocker

The dangling-object findings are a preservation blocker. No `gc`, prune, reset,
checkout, branch deletion, or worktree normalization was performed. Before any
source migration, an owner-authorized preservation pass must classify dangling
objects, capture required refs and tags, and prove that no release, signing,
Apple-review, or recovery evidence is reachable only through those objects.
