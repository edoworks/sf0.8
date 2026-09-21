# OpenCode Model Routing

This directory contains the global, credential-free provider catalog and model
routing policy. It covers OpenAI, OpenCode Zen, OpenCode Go, Ollama Cloud,
local Ollama, and GitHub Copilot.

## Commands

```bash
npm --prefix ~/.config/opencode run models:refresh
npm --prefix ~/.config/opencode run models:audit
npm --prefix ~/.config/opencode run models:benchmark -- --model=openai/gpt-5.6-luna --tier=routine
npm --prefix ~/.config/opencode run models:promote
npm --prefix ~/.config/opencode run models:status
npm --prefix ~/.config/opencode test
```

`update.mjs` runs a bounded daily cycle: refresh, metadata-only history audit,
at most four candidate benchmarks, a second refresh to bind benchmark status,
and safe promotion. Routine and standard routes may auto-promote. Complex,
vision, and trust-boundary routes require operator approval.

Catalog discovery never reads or copies credential values. A model appearing in
a provider list only makes it a candidate; it does not make it approved.

The router persists only allowlisted model metadata and enforces a 48-hour
catalog maximum age. `startup_fallback` means selection during OpenCode startup
when the primary is absent from the refreshed catalog. OpenCode does not expose
a plugin hook for changing the selected model after a runtime request fails, so
this is not claimed as request-time retry or failover.

Global `small`, `explore`, `general`, `plan`, and `build` routes are never
auto-promoted. The updater may auto-promote only provider-specific routine and
standard comparison agents after current-suite benchmark evidence passes.

OpenCode loads configuration at startup. Restart OpenCode after a promotion.

## Cloud admission

Local routing does not block cloud dispatch because of spend, projected token
usage, session context, unknown pricing, or prior usage-limit responses. Provider
rate limits and provider-native context/output limits still apply to each
request. Process timeouts, finite benchmark work, route qualification, and the
routine-task/frontier-route coherence check remain enforced.

The trusted rate card in `provider-pricing.json` overrides misleading zero-cost
subscription catalog metadata. Cost is an advisory ordering signal among
otherwise qualified routes; it is never an admission gate.
