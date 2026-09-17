#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-$(pwd)}"
REMOTE="${REMOTE:-origin}"
BRANCH="${BRANCH:-main}"

cd "$ROOT"

if [[ -n "$(git status --porcelain)" ]]; then
  echo "sync check failed: worktree is not clean: $ROOT" >&2
  exit 1
fi

git show-ref --verify --quiet "refs/remotes/$REMOTE/$BRANCH" || {
  echo "sync check failed: missing $REMOTE/$BRANCH" >&2
  exit 1
}

local_head="$(git rev-parse HEAD)"
remote_head="$(git rev-parse "$REMOTE/$BRANCH")"
if [[ "$local_head" != "$remote_head" ]]; then
  echo "sync check failed: HEAD $local_head != $REMOTE/$BRANCH $remote_head" >&2
  exit 1
fi

echo "sync check passed: $ROOT HEAD matches $REMOTE/$BRANCH ($local_head)"
