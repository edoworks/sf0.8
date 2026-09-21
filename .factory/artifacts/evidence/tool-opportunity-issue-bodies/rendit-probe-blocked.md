Probe completed to the safe boundary; issue remains open as `BLOCKED_DEPENDENCY`.

- Source: clean detached worktree at `b00549fcab43e9d3d1ee9ec3a0222ffb446807a5`.
- `make validate`: 59 recipe files passed.
- Selected deterministic/provenance/no-network/no-AI/validation tests: 44 passed.
- Actual PNG render was not run because the pinned `resvg` binary is unavailable.
- No dependencies were installed and the dirty source checkout was untouched.
- Evidence: `.factory/artifacts/evidence/rendit-workflow-probe-2026-09-19.json`.
- 5-Whys: `.factory/artifacts/evidence/rendit-probe-blocker-5whys.md`.
- Next step requires human-authorized provision of the exact pinned binary, then
  two renders with PNG/meta/hash comparison and a genuine second consumer.
