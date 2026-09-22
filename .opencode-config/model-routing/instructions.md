# Cost-Aware Model Routing

## Operating rule while ollama-cloud quota ≥ 90% (2026-09-14, owner direction)

Default interactive work order for the rest of the month:
1. Routine/mechanical turns → `small`/`explore` (local `granite4.1:3b`, zero marginal cost).
2. Bounded standard work → `general`/`plan`/`build` on OpenAI `gpt-5.6-luna` (separate OpenAI subscription budget).
3. Interactive ollama-cloud only where kimi-k3's 1M context or vision is materially needed; if the ollama-cloud cap trips, the proven interactive fallback is `ollama-cloud/glm-5.3-flash` — passed the standard benchmark suite 2026-09-14 (3/3, suite v2). It is also the routine startup fallback; use it interactively only when the cap forces it, not as a habit.
4. Local standard-tier attempt closed 2026-09-14: `ollama/qwen3.5:9b` benchmark errored at the harness level (opencode run stalls against the local provider — infrastructure, not quality). Retrying local standard requires fixing that harness path first.
- Do not launch a model for commit creation, command execution, formatting, or deterministic state edits.
- Use `explore` for routine repository discovery and `general` for normal bounded work.
- Routine-class requests are refused on standard and complex routes; retry them with `small` or `explore` instead of escalating.
- Tool attribution records provider/model, agent, session hash, and tool name at `~/.local/state/opencode/routing/tool-attribution.jsonl`; command text is intentionally excluded.
- Use `trust-review` only for authentication, authorization, isolation, signing, release, or other trust-boundary analysis.
- Use `frontier-build` only for complex construction or after the standard route fails explicit acceptance criteria.
- Use the `vision` route (`ollama/qwen3.5:4b`, fallback `ollama-cloud/gemma4:31b`) for screenshot-only assertion inputs: rendered UI verification, visual regression checks, and accessibility-relevant layout inspection from captured images. Vision auto-invocation is limited to screenshot assertion and does not authorize release, upload, submission, or any external write.
- Use at most one construction subagent and one independent review subagent for a normal increment. Add `trust-review` only when authentication, authorization, isolation, signing, release, or another trust boundary is materially involved.
- Start a fresh session when context quality degrades; local routing does not impose a cloud context or spending admission cap.
- Treat provider usage-limit and rate-limit responses as request outcomes. Honor provider-native retry guidance, but do not create an additional local quarantine.
- Provider-specific agents exist for controlled comparison and fallback. Do not round-robin merely to consume every provider.
- Prefer the cheapest approved route that meets the task's quality threshold. Escalation must have a concrete reason.
- Routine and mechanical turns (screenshots, crops, resizes, OCR, renames, status checks, issue bookkeeping, notifications) must run on `small`, `explore`, or an approved routine route. The cost router rejects such turns dispatched to standard or complex routes; premium models stay reserved for complex construction and trust-boundary review.
- A newly discovered model is not approved merely because it is newer or cheaper. Routine and standard routes require passing benchmark evidence; complex and trust-boundary promotions also require operator approval. Vision is auto-invokable for screenshot-only assertion inputs per owner approval 2026-09-21; release, upload, submission, and external-write authority remain separately gated.
- The active route registry is `~/.config/opencode/model-routing/approved.json`. Catalog and audit artifacts contain no credentials.
- Onboarding a new model or provider, or repairing routes and fallbacks, follows the `model-routing` skill at `~/.config/opencode/skills/model-routing/SKILL.md`; do not improvise onboarding prompts or hand-edit live routes.
