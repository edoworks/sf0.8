# Executive Decision Brief Effectiveness Correction

## Problem

The Executive Council MVP validates evidence structure but does not prove
decision usefulness. Its five lenses are predetermined, its rendered view can
drift from JSON, CI accepts a stale dated artifact, and there is no supported
path to record founder decisions or outcomes.

## Scope

- Keep one evidence-backed founder decision brief; do not add agents, services,
  schedules, feeds, personas, or autonomous authority.
- Require one concrete decision, alternatives including no action, a deadline,
  owner, ceiling, success threshold, and stop rule.
- Require each lens to contribute one distinct concern or explicitly abstain.
- Render values from the payload rather than hard-coded status prose.
- Add deterministic recording of founder decisions and later outcomes.
- Reject stale checked-in evidence and incomplete effectiveness tracking.

## Acceptance

- Focused tests prove render fidelity, freshness enforcement, distinct lens
  contributions, complete action criteria, and outcome recording.
- Historical evidence remains preserved.
- The full repository suite and relevant validators pass.
- No external action, publication, product revival, or spending is authorized.

## Effectiveness Gate

The mechanism remains experimental until three real founder decisions record
time-to-read, decision effect, missed facts, prevented work, cognitive load,
and actual outcome. If it does not change or accelerate a decision, prevent
unjustified work, or reduce decision time, retain only the conflict detector
and compact evidence brief.

## Verification Record

- Schema-v2 brief generated at `.factory/artifacts/executive-council/2026-09-19-decision-brief.{json,md}`.
- `python3 scripts/executive_council.py validate`: passed.
- Focused Executive Council tests: 12 passed.
- Full repository tests: 177 passed.
- Relevant lifecycle, automation, portfolio, reuse, human-action queue,
  education, Apple distribution, review, ecosystem, control-plane, and safety
  checks passed.
- CI run `35295186391`: success.
- The brief remains `PENDING_HUMAN`; no founder decision or empirical result is
  claimed by this implementation.
