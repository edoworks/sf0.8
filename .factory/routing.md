# Two-route routing policy — Factory v0.1 (rules now, learning later)

Deterministic classification. Learning is deferred until there is enough
homogeneous outcome data (design review: solo operator + heterogeneous tasks
means bandits fit noise). This file is policy, not heuristics.

## Routes

| Route | Executor | Use when | Hard constraints |
|---|---|---|---|
| **primary** | main agent (this session's route) | default for all well-bounded repo tasks | verification required before done |
| **fallback** | backup agent | primary fails twice on the same verification step, OR privacy/risk classification demands a different trust posture | max 2 harness switches per issue (governance envelope) |

## Classification (deterministic, audited)

1. **Privacy class** from `.factory/repo.yaml` + task content:
   - `personal-sensitive` or `secret` → never send to unapproved cloud; route = local-capable only
   - `public`/`private` → cloud-capable routes allowed
2. **Risk class**:
   - signing, publishing, repo visibility, deletion, deploy → **escalate human** (no route)
   - app logic + tests → normal
3. **Complexity class**:
   - single-file change, bounded → primary
   - cross-repo, new subsystem, unfamiliar API → primary with verification floor raised (extra unit/UI test required)

## Envelope (from .factory/governance.yaml)

- max_attempts_per_issue: 4
- max_harness_switches: 2
- Owner-set dollar ceilings govern; this file never mutates them.

## Evidence loop (when learning is revisited)

Every run is recorded via `scripts/ledger.sh` (outcome, attempts, verification).
When ≥30 comparable outcomes exist per route/task-kind, offline analysis may
recommend a rule change. Autonomous policy mutation remains forbidden.