---
name: model-routing
description: Onboard new models and providers into the OpenCode cost-routing stack, repair dead routes or fallbacks, and keep skills current after completed work. Use when a new model or provider appears in a catalog, when a route needs benchmarking or promotion, when startup fallbacks need repair, or after any completed work chunk to decide whether a repeatable flow should become or update a skill.
---

# Model Routing Onboarding And Skill Currency

Onboard new models and providers through the deterministic routing pipeline,
and keep automation current so future sessions never hand-write onboarding
prompts or re-derive the routing procedure.

## When To Use

- A new model or provider appears in `catalog.json` or a provider announcement.
- A route loses benchmark currency or its startup fallback becomes dead or
  unqualified.
- After completing any non-trivial work chunk, to decide whether the flow
  should be captured as (or folded into) a skill.

## Procedure: New Model Or Provider

1. Refresh the catalog: `npm --prefix ~/.config/opencode run models:refresh`.
   Providers are declared in `model-routing/policy.json` under `providers`;
   adding a provider is a config change there, never a code change.
2. Inspect capabilities in the catalog record: `capabilities` (toolcall,
   reasoning, text, image, attachment) and `variants`. Tiers map as: routine
   needs toolcall + text; standard, complex, and trust_boundary additionally
   need reasoning; vision needs image + attachment.
3. Benchmark before any promotion:
   `npm --prefix ~/.config/opencode run models:benchmark -- --model=<provider>/<model> --tier=<tier>`.
   Prices must be comparable via `provider-pricing.json`; unknown-price
   models never auto-promote.
4. Promote through the pipeline, never by hand-editing live routes:
   `npm --prefix ~/.config/opencode run models:promote`. `routine`,
   `standard`, and `vision` auto-promote; `complex` and `trust_boundary`
   require explicit owner approval recorded in `approved.json` with a
   `basis`. Vision auto-invocation is scoped to screenshot-only assertion
   inputs per owner approval 2026-09-21; release, upload, submission, and
   external-write authority remain separately gated.
5. Verify: `npm --prefix ~/.config/opencode run models:status` shows the new
   route qualified; run `npm --prefix ~/.config/opencode test`, and a
   cost-router hook smoke test when routes or fallbacks changed.

## Procedure: Repairing Routes And Fallbacks

1. A fallback is dead when its target lacks current benchmark evidence for
   the route tier, or is missing or inactive in the catalog.
2. Repoint `startup_fallback` in `approved.json` to a qualified cheaper route
   (benchmark-passed, lowest comparable cost for the tier) and bump
   `updated_at`. Never point routine or standard fallbacks at premium
   frontier models.
3. Re-run the test suite and `models:status`; confirm the cost-router config
   hook still resolves every built-in agent (small, explore, general, plan,
   build).

## Procedure: Post-Work Skill Currency

1. After verification passes on a work chunk, ask whether the session
   repeated a manual flow (commands, checks, edits) that a future session
   would otherwise re-prompt.
2. If yes, add or update a skill under `~/.config/opencode/skills/` (user
   tooling) or `.opencode/skills/` (repo workflow) encoding the steps as a
   Procedure with When To Use and Constraints sections, so future sessions
   invoke it by name without new prompts.
3. Update pointer docs (`model-routing/instructions.md`, `.clinerules`,
   `AGENTS.md`) only when the skill changes an observable workflow rule.

## Procedure: Trivial-Task Demotion

Trivial and mechanical operations must not consume standard or complex route
budgets. Apply this procedure before dispatching any subagent or tool call
whose work is purely mechanical.

1. **Classify the turn:** If the work is screenshots, file reads, `git status`,
   `ls`, `plutil -lint`, `security find-identity`, JSON validation, identity
   checks, issue bookkeeping, notifications, or any single read-only command,
   it is routine.
2. **Dispatch to the cheapest route:** Use `explore` (local granite, zero
   marginal cost) for routine subagent work. If the work is a single read-only
   command, run it directly without a subagent at all.
3. **Never use `general` (OpenAI Luna) or `frontier-build` for mechanical
   turns.** The cost router rejects routine-class turns on standard and complex
   routes, but within a single agent session the model is fixed — enforce the
   demotion at dispatch time, not mid-turn.
4. **Audit after sessions:** Review
   `~/.local/state/opencode/routing/tool-attribution.jsonl` for routine turns
   that ran on standard or complex routes. Flag and document each escape.
5. **Mechanical guard:** The `deepdive`, `news`, and `curiosity` commands use
   `agent: general` (correct — they need reasoning). The `brb` and `timebox`
   commands use `agent: explore` (correct — they are routine). Any new command
   that is purely mechanical must use `agent: explore`, not `agent: general`.

## Constraints

- `approved.json` is the only route registry and `policy.json` the only
  provider list; do not add provider or model defaults or cloud fallbacks
  elsewhere.
- No promotion without passing the current benchmark-suite digest; evidence
  lives in `benchmarks.json`.
- Benchmark digests and fixture hashes are integrity evidence; never edit
  them to force a promotion.
- Routine-class work stays on routine routes; the cost router rejects
  routine-class turns on standard and complex routes.
- Trivial-task demotion is enforced at dispatch time; a running `general`
  agent cannot demote itself mid-turn.
- The GitHub identity boundary applies to any write performed under this
  skill: `gh api user --jq .login` must return exactly `hellofoculoom`.
