# OpenCode Config Backup

This directory tracks the opencode runtime configuration so it survives
machine loss. It is committed to `edoworks/sf0.8` and is available to any
fresh `git clone`.

## What is tracked

- `opencode.jsonc` — permission policy, provider config, plugin binding
- `factory-progress.md` — governance instructions (incremental completion,
  identity boundary, notifications, branch cleanup)
- `commands/` — continuation and bounded-work commands
- `plugins/` — cost-router plugin and library
- `scripts/` — issue-intent validation, completion notification, tests
- `skills/` — brb, issue-tracking, model-routing skills
- `model-routing/` — routing library, benchmarks, incidents, policy

## What is NOT tracked (regenerate or restore manually)

- `node_modules/` — run `npm install` in the restored directory
- `model-routing/catalog.json`, `candidates.json`, `benchmarks.json`,
  `history-audit.json`, `approved.json` — regenerate with
  `model-routing/update.mjs`
- `~/factory-secrets/ntfy_topic` — restore manually (mode 0400, owner-only)
- Apple signing credentials — re-provision via Apple Developer portal + Xcode
- `gh auth login` — re-authenticate GitHub CLI

## Restore on a fresh machine

```bash
git clone https://github.com/edoworks/sf0.8.git
cd sf0.8
bash .opencode-config/restore.sh
gh auth login
opencode debug config --pure  # verify config resolution
python3 -m unittest tests/test_permission_policy.py  # verify permissions
```

Then read `~/.config/opencode/commands/continue-sf08.md` for the restart
sequence to resume NowNest qualification and sf0.8 evidence work.