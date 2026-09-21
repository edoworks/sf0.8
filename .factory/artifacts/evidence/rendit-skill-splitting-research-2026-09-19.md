# Rendit Skill Splitting Research Brief

Status: `COMPLETE`
Date: 2026-09-19
Date cutoff: 2026-09-19 (inclusive)

## Scope and source plan

- Audience: Rendit maintainers and the sf0.8 factory owner deciding whether to
  split Rendit into multiple shareable skills.
- Jurisdiction: technical architecture and artifact portability; no legal,
  licensing, or publication authorization decision is made by this research.
- Decision to inform: whether to split Rendit into independently shareable
  skills now, and what boundary and validation conditions should govern that
  split.
- Primary sources: Rendit source and tests; Agent Skills/OpenCode
  specifications and documentation; repository-local contracts and validators.
- Secondary sources: maintainer documentation and independent engineering
  discussions about modular skills, when directly relevant.
- Lead-only sources: search snippets, rankings, generated summaries, and
  unverified third-party claims. Leads will not support material conclusions.
- Counterclaim search: test the strongest cases for keeping Rendit monolithic,
  including cross-skill coupling, duplicated context, discovery friction,
  versioning, and safety-boundary drift.
- Stopping rule: stop when the current Rendit seams, portability constraints,
  and principal counterclaims are directly evidenced, or when remaining
  questions require implementation experiments or an owner decision rather
  than more desk research.

## Known facts

- The sf0.8 portfolio records Rendit as a separate source-of-truth project.
- The local factory already has a reusable-skill increment with explicit
  validation and human-only publication gates.

## Open questions

- What are Rendit’s actual capabilities, dependency graph, and internal seams?
- Which seams can be packaged and discovered independently without hidden
  coupling?
- What does the target skill format require for metadata, layout, and
  portability?
- What tests or release controls are needed to prevent split artifacts from
  drifting or leaking private context?

## Hypotheses

- Rendit is likely splittable along independently triggered workflows, but not
  every source-module boundary is a valid shareable-skill boundary.
- A small number of cohesive skills plus shared non-skill libraries may be
  safer than one skill per feature.

## Recommendations status

Recommendation: pursue a staged split into shareable skill artifacts, but do
not split Rendit into one skill per Python package or backend. Keep Rendit as
the canonical runtime/core initially; expose a small number of workflow-level
skills whose scripts call explicit, tested interfaces. Start with recipe
validation/rendering because it has the clearest contract and the least
provider-specific coupling. Treat AI-character, factory/build, and any audio
workflow as later candidates after dependency and boundary tests pass.

## Executive answer

**Overall: feasible with conditions (high confidence).** The Agent Skills
format is explicitly a directory artifact with required metadata and optional
scripts, references, and assets, so Rendit workflows can be packaged as
separate discoverable artifacts. This does not require duplicating or
releasing Rendit's whole Python runtime. [Primary specification, retrieved
2026-09-19: https://agentskills.io/specification]

**Immediate independent packaging: not yet low-risk (high confidence).** The
current runtime has a broad, coupled dependency surface and an eagerly imported
backend registry. A split that merely copies directories would duplicate
hidden coupling and make installation and testing misleading. [Primary source
code, retrieved 2026-09-19: `setup.py`, `requirements.in`,
`rendit/backends/registry.py`]

**Best boundary: workflow and contract, not implementation directory (high
confidence).** Candidate boundaries are: recipe validate/render; character
generation; build manifest/provenance; and QA/determinism review. They should
share a versioned core contract rather than copy renderer internals. This is an
architecture recommendation derived from the source graph and the skill
format, not a fact asserted by an external standard.

## Findings

### Claim 1: Skills are independently shareable artifacts by format

**Evidence:** The Agent Skills specification requires one directory and one
`SKILL.md`, with optional `scripts/`, `references/`, and `assets/`. It imposes
portable metadata constraints on `name` and `description`; it does not require
that a skill contain an entire application runtime. OpenCode separately
discovers skills from project or global skill directories and loads them on
demand. [Primary specifications, retrieved 2026-09-19:
https://agentskills.io/specification;
https://opencode.ai/docs/skills/]

**Counterevidence:** A valid directory is not proof of operational
independence. A skill can still depend on private paths, undisclosed tools,
network access, credentials, or an unavailable application package.

**Implication:** Split at the artifact/agent-workflow layer first. “Shareable”
must include dependency declaration, isolated validation, provenance, and
public-surface review, not just a valid `SKILL.md`.

### Claim 2: Rendit has several plausible workflow seams

**Evidence:** The repository contains distinct CLI areas for rendering,
AI-specific operations, and factory/build operations (`cli_render.py`,
`cli_ai.py`, `cli_factory.py`), plus recipe validation, registry/provenance,
quality checks, layouts, backends, and renderer modules. Its tests cover these
areas separately, including `test_validate.py`, `test_ai_character.py`,
`test_factory_build.py`, `test_provenance.py`, `test_no_ai.py`, and
`test_determinism.py`. [Primary source tree and tests, retrieved 2026-09-19:
`/Users/hello/foculoom/tools/rendit`]

**Counterevidence:** The seams are not clean package boundaries. The main
render path imports validation, preprocessors, renderer modules, backend
registry, audio/video export, and shared configuration. The registry eagerly
imports all backend classes. [Primary source code, retrieved 2026-09-19:
`rendit/render.py:54-66`; `rendit/backends/registry.py:32-49`]

**Implication:** The candidate split is real at the user-task level, but each
candidate needs an explicit interface and dependency closure before becoming a
separately installable or publicly shareable runtime.

### Claim 3: The current install surface prevents a clean “one skill = one
capability” split

**Evidence:** `setup.py` installs image, schema, YAML, numerical, background
removal, Fal, Anthropic, and CLI dependencies together. `requirements.in`
similarly mixes core, AI, and test dependencies. [Primary source code,
retrieved 2026-09-19: `setup.py:10-27`; `requirements.in:1-10`]

**Counterevidence:** Skills can invoke an existing Rendit checkout rather than
ship separate Python packages. That makes an initial instruction/script split
possible without solving packaging immediately.

**Implication:** First release should be “multiple skill wrappers over one
canonical Rendit runtime” or a monorepo bundle, not independent distributions.
Optional extras and lazy imports are prerequisites for later standalone
runtime artifacts.

### Claim 4: Smaller, high-signal skills are likely better for agent use

**Evidence:** Anthropic's context-engineering guidance recommends curating the
smallest possible set of high-signal context and describes progressive
disclosure as a way to avoid loading everything at once. OpenCode's skill
documentation says skills are loaded on demand and descriptions drive
selection. [Secondary/maintainer guidance, retrieved 2026-09-19:
https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents;
https://opencode.ai/docs/skills/]

**Counterevidence:** Excessive splitting increases discovery ambiguity,
cross-skill coordination, duplicate instructions, release/version overhead,
and the chance that a workflow loads only half its safety contract.

**Implication:** Use a small bounded set of skills with sharply different
triggers. Put shared safety rules and interfaces in references or a common
contract; do not create skills for every backend, layout, or helper module.

### Claim 5: Rendit's existing determinism and provenance controls must travel
with any split

**Evidence:** Rendit documents fixed hash seed/locale, pinned renderer hashes,
vendored fonts and ICC data, offline rendering, output provenance metadata,
schema validation, lockfiles, golden fixtures, and visual-review gates. CI has
blocking Ubuntu render/manifest/canary checks and advisory macOS checks.
[Primary source documentation and CI, retrieved 2026-09-19: `README.md:60-80`,
`README.md:104-118`, `CONTRIBUTING.md:19-29`, `.github/workflows/ci.yml:15-74`]

**Counterevidence:** The repository is currently dirty and ahead/behind its
remote, so the inspected tree is not a clean immutable release snapshot. The
README says audio output is deferred while the source tree contains audio
backends/export modules and audio tests. [Primary repository state and source,
retrieved 2026-09-19: `git status`, `README.md:136-147`,
`rendit/backends/`, `tests/test_audio_*.py`]

**Implication:** Any split decision must pin a clean source revision and first
resolve the audio capability/documentation conflict. A shareable artifact must
carry the exact tests, lockfiles, fixtures, and no-auto-promotion rules needed
for its stated capability.

## Conflicts and unknowns

- The source tree and README disagree about audio support; this research does
  not determine whether the code is production-ready or merely partial.
- The working tree has uncommitted output and test changes; capability claims
  should not be treated as release evidence until a clean revision is chosen.
- It is unknown whether external consumers need Rendit as an executable
  application, a Python library, an agent skill, or all three. That decision
  changes the required packaging work substantially.
- It is unknown whether all bundled assets, fonts, binaries, model adapters,
  and prompts have licenses and provenance suitable for sharing.
- No installation-size, cold-start, or cross-platform measurements were run;
  those require an implementation experiment.
- The Agent Skills specification defines artifact structure, not a dependency
  manager, trust model, quality bar, or semantic versioning policy for a
  multi-skill suite.

## Decision implications and change conditions

Proceed with a design increment, not public publication. A practical first
layout is:

1. `rendit-render`: validate a recipe and render deterministic still/sprite
   outputs, including provenance and lock checks.
2. `rendit-character`: invoke the character workflow only when AI/provider
   dependencies and founder-gated boundaries are explicitly available.
3. `rendit-build`: validate manifests, build/clean/diff/report, and write
   provenance/lock artifacts.
4. `rendit-review`: run deterministic, no-network, manifest, fixture, and
   visual-review checks; keep this internal until its policy surface is
   generalized.

Before promotion, require: clean pinned source revision; a skill contract and
negative trigger fixtures for each artifact; no private paths or unsupported
provenance claims; explicit optional dependency behavior; lazy provider
imports; isolated tests; license/asset review; and a second real consumer or
an explicit exception to the repository's Rule of Two. Do not auto-publish or
auto-promote outputs.

The conclusion would change toward “keep monolithic” if an end-to-end trace
shows every intended consumer needs the full renderer, if isolated execution
cannot preserve determinism/provenance, or if skill selection causes unsafe
partial workflows. It would change toward “standalone packages now” if a clean
experiment demonstrates independent dependency closures, stable public
interfaces, reproducible outputs, and two real consumers per candidate.

## Sources

### Primary

- Agent Skills specification, standard/artifact format, retrieved 2026-09-19:
  https://agentskills.io/specification
- OpenCode Agent Skills documentation, discovery and loading behavior,
  retrieved 2026-09-19: https://opencode.ai/docs/skills/
- Rendit source, tests, README, CI, and contributor contract, source revision
  `b00549fcab43e9d3d1ee9ec3a0222ffb446807a5`, retrieved 2026-09-19:
  `/Users/hello/foculoom/tools/rendit`
- sf0.8 portfolio and artifact registry, retrieved 2026-09-19:
  `.factory/portfolio.yaml`; `.factory/artifacts/reuse-registry.json`

### Secondary

- Anthropic Engineering, “Effective context engineering for AI agents,”
  published 2025-09-29, retrieved 2026-09-19:
  https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- Twelve-Factor App, dependency/configuration and portability principles,
  retrieved 2026-09-19: https://12factor.net/

### Lead-only

- Search-result snippets and generated summaries were not used as evidence.
- No social posts, rankings, or unverified package descriptions were used to
  support a material claim.
