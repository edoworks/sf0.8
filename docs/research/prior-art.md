# Prior art: what reputable practitioners have already concluded, and what edoworks.ai builds on

Date: 2026-09-13. All URLs verified at fetch time. This document anchors the positions in [`../factory-v0.1-design-review.md`](../factory-v0.1-design-review.md) to external literature so future design debates argue from evidence rather than recall.

## 1. The v0.1 thesis is corroborated by the strongest public evidence

Every core correction in the design review was independently reached by reputable practitioners:

| Expert / org | Source | Conclusion | v0.1 mapping |
|---|---|---|---|
| Anthropic | "Building effective agents"[^1] | The most successful implementations use **simple, composable patterns rather than complex frameworks**; workflows before agents; routing as static classification | One primary + one fallback agent, deterministic rule-based routing, no bandits |
| OpenAI (Codex team) | "Harness engineering: leveraging Codex in an agent-first world"[^2] | Shipped ~1M LOC with 0 hand-written lines, 3→7 engineers: **repository knowledge as the system of record**, architecture enforced by deterministic linters/structural tests, agent legibility as the goal, entropy "garbage collection" agents | Git-not-SQLite for durable cognition; deterministic verification outranks AI review; every artifact pays rent |
| Mitchell Hashimoto | "My AI Adoption Journey", Step 5[^3] | Coined **harness engineering**: every time an agent fails, engineer it so it never fails that way again — (1) AGENTS.md lines earned from observed bad behavior, (2) programmed verification tools. Harnesses are *grown*, not designed up front. | The factory-change gate (`repeated_friction_count_gte_3`) is his process formalized |
| Birgitta Böckeler / Thoughtworks | "Harness engineering for coding agent users"[^4] | Agent = model + harness; user-side harness = **guides (feedforward) + sensors (feedback)**, computational vs inferential; a good harness **directs human input to where it matters most, not eliminates it**; harness templates risk the same forking/versioning pain as service templates | Governor/verification/escalation = guides + sensors with a policy layer |
| Kief Morris / Thoughtworks | "Humans and Agents in Software Engineering Loops"[^5] | "Why loop" (idea→software) vs "how loop" (artefacts); humans belong **on the loop**, neither micromanaging inside it nor vibe-coding outside it | Human approval at external-impact gates, not every internal change |
| Simon Willison | "The lethal trifecta"[^6] | **Private data + untrusted content + external communication = exploitable, always.** Guardrail products claiming ~95% detection fail security math; only structural capability removal works. Dozens of documented exfiltration attacks against production systems. | Names the untrusted-contributor threat model; see §3 |
| Cross-vendor community | agents.md[^7] | AGENTS.md is the de-facto agent-instruction standard, adopted by 60k+ projects and by Codex, Jules, Zed, Devin, Amp, Cursor, Copilot coding agent, opencode — and by the commercial vendor **Factory.ai** | AGENTS.md-as-map is adopted unchanged; nothing to invent |
| Zed-led ecosystem | Agent Client Protocol[^8] | ACP decouples agents from editors the way LSP did for language servers; reuses MCP JSON types | "Use native interfaces, don't invent a protocol" |

## 2. Adopted unchanged (do not reinvent)

1. **AGENTS.md** as the agent-instruction contract format.
2. **MCP and ACP** for tool/editor interop.
3. **Guides + sensors** vocabulary (Thoughtworks) for the harness: feedforward guides (AGENTS.md, PRD, policy) and feedback sensors (compile, tests, linters, simulator).
4. **Deterministic-over-inferential verification** (OpenAI, Thoughtworks, NIST): a second LLM is a sensor, not a proof.
5. **Repository as system of record** (OpenAI): durable product intent lives in Git.

## 3. The lethal trifecta — applied to this factory

Willison's framing sharpens the design review's publication firewall:

> Private data × untrusted content × external communication = exploitable.

Two places in the roadmap must never combine all three:

1. **Untrusted contributor content** (public issues/PRs) × private-repo access × agent with push/deploy capability → structural rule stands: contributor input is untrusted data, processed by sandboxed/read-only agents, gated by deterministic checks, never flows to a privileged agent with secrets.
2. **Publication/blog automation** × private operational knowledge × external publishing channel → the public-writing path must have private credentials structurally *absent*, not merely policy-denied.

No "guardrail" prompt or classifier is accepted as a control for these boundaries; the control is capability removal (sandboxing, credential isolation, ephemeral runners).

## 4. Where this project must NOT tread

- **factory.ai is an existing commercial vendor** in exactly this space (listed among AGENTS.md adopters). The internal codename "Factory" collides publicly. **Public brand: edoworks.ai.**
- **Learned routing/budgets:** no public evidence that adaptive routing pays off at solo/small-team scale; Anthropic's routing pattern is static classification. Keep the design review's "rules now, learning later" position.
- **Harness templates as a product:** Thoughtworks explicitly warns they inherit the service-template forking/versioning problem. If the harness is ever published as a template, document "fork and own it" as the intended consumption model.

## 5. The defensible gaps (what edoworks.ai actually contributes)

The literature converges on single-repo harnesses for teams. Under-served spaces this project addresses:

1. **Portfolio-level lifecycle governance** — repo classification, legacy-issue quarantine, KEEP/SIMPLIFY/REFACTOR/REBUILD/KILL dispositions — published playbooks exist for services, not for a personal/small-team repo portfolio.
2. **Constitution-as-code** — the entropy budget, factory-change gate, and immutable/learnable policy split written down as enforceable YAML rather than implicit habit.
3. **Apple/Xcode execution-plane playbook** — nearly all published harness work is web/backend-centric. iOS-specific gates (Simulator, device, TestFlight, signing, pinned Xcode) are a genuine gap.
4. **Solo-operator disaster recovery** — account recovery, signing credentials, SQLite-disposability drills for a one-maintainer agent operation.

Everything else must be adopted from prior art.

## 6. IP protection and public availability (feasibility: yes)

Public availability and IP protection are compatible via layered, industry-standard mechanisms:

| Layer | Decision | Precedent / reference |
|---|---|---|
| Code license | **Apache-2.0** (permissive + explicit patent grant) | .NET, Swift, Kubernetes; see choosealicense.com[^9] |
| Documentation | **CC BY 4.0** | choosealicense.com non-software guidance[^9] |
| Contributions | **DCO** (`Signed-off-by` trailers) — not a CLA | Linux kernel model; trivial for a solo maintainer |
| Brand | **Trademark on `edoworks.ai`**, kept out of the code license + trademark policy at publication | Linux Foundation model |
| Secrets / private portfolio | **Structural exclusion**: private control plane never enters public repos | Non-negotiable control per §3 |
| Third-party / employer IP | Pre-publication provenance scan + human IP clearance (already gated in the design review) | — |
| AI-generated code | No jurisdiction grants copyright to the model; agent output is published as the operator's work product under the project license; DCO covers contributor-agent output | Document the stance in CONTRIBUTING at publication |

**Timing:** LICENSE/DCO/trademark-policy files are added when a repo crosses the publication gate — not before. Until then, `edoworks/sf0.8` stays **private**, which is itself the default classification per the repo-lifecycle invariant.

### License pattern evidence (deep dive 2026-09-13)

The industry has converged on layered protection; the license is never the sole control:

| Pattern | Mechanism | Practitioners | Fit |
|---|---|---|---|
| Open core | MIT/BSD/Apache code | GitLab, Docker, pre-2023 HashiCorp, VS Code | factory template |
| Copyleft | AGPLv3 → proprietary dual | Grafana Labs, early MongoDB | products only if cloud-resale feared |
| BUSL-1.1 (source-available) | non-production free; converts to GPL-compatible ≤4 yrs/version | **MariaDB (author), HashiCorp, CockroachDB, Sentry (2019–2023)** | alternative if commercial exclusivity needed; not OSI-open; expect community debate (OpenTofu fork precedent) |
| Fair Source (FSL-1.1) | BUSL variant, 2-yr change delay | **Sentry (current), Codecov** | cleaner optics than BUSL |
| Trademark-only moat | registered mark + policy, code stays permissive | Linux Foundation projects, Red Hat, Python | **the real moat for iOS products** — App Store naming is trademark-gated |

Sources: mariadb.com/bsl11, fair.io, Sentry's open-source-values series (BSD→Apache→BUSL→FSL trajectory), Wikipedia FOSS history, HashiCorp/OpenTofu fork record. Decision unchanged: Apache-2.0 + CC BY 4.0 + DCO + trademark; this table exists so the publication-gate flip is informed, not improvised.

**The moat is never the code.** It is the judgment encoded in the harness, the shipped products, and the brand.

## 7. Standing reference list

[^1]: Anthropic, "Building effective agents", Dec 2024. https://www.anthropic.com/engineering/building-effective-agents
[^2]: Ryan Lopopolo / OpenAI, "Harness engineering: leveraging Codex in an agent-first world", Feb 2026. https://openai.com/index/harness-engineering/
[^3]: Mitchell Hashimoto, "My AI Adoption Journey", Feb 2026. https://mitchellh.com/writing/my-ai-adoption-journey
[^4]: Birgitta Böckeler / Thoughtworks, "Harness engineering for coding agent users", Apr 2026. https://martinfowler.com/articles/harness-engineering.html
[^5]: Kief Morris / Thoughtworks, "Humans and Agents in Software Engineering Loops", Mar 2026. https://martinfowler.com/articles/exploring-gen-ai/humans-and-agents.html
[^6]: Simon Willison, "The lethal trifecta for AI agents: private data, untrusted content, and external communication", Jun 2025. https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/
[^7]: agents.md — a simple, open format for guiding coding agents. https://agents.md/
[^8]: Agent Client Protocol. https://agentclientprotocol.com/
[^9]: Choose a License (GitHub). https://choosealicense.com/ and the OSI Open Source AI Definition for AI-artifact licensing context. https://opensource.org/ai/open-source-ai-definition
