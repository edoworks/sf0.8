# Shareable Skill Increment

Status: `INTERNAL_REUSABLE_CANDIDATE`
Date: 2026-09-19

## Scope

Create portable project-local contracts for bounded work, evidence research,
and prose editing. Expose explicit command adapters for timebox, BRB,
deep-dive, news, humanize, and no-fluff workflows.

## Provenance

- Agent Skills format: https://agentskills.io/specification
- OpenCode discovery: https://opencode.ai/docs/skills/
- Research guidance: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- UI/reduced-motion material is intentionally out of this increment.
- `humanizer` was inspected as an MIT-licensed external candidate; no external
  content was installed or copied.

## Acceptance criteria

- All skill names and command files use valid OpenCode/Agent Skills structure.
- Positive and negative trigger fixtures exist before promotion.
- Safety tests prove no automatic publication, release, external write, or
  unsupported factual addition.
- `python3 scripts/validate-ecosystem.py` and repository tests pass.
- No publication or external contribution occurs without a separate owner
  decision.

## Next evidence

Dogfood each workflow in two real contexts, record false-positive and
false-negative triggers, then decide whether to keep project-local, promote to
global internal shared, or prepare a separately authorized public package.

## Verification

- `python3 -m unittest discover -s tests`: 170 passed.
- `python3 scripts/validate-ecosystem.py`: passed.
- `git diff --check`: passed.
- Contract tests cover all three skills, six command adapters, safety wording,
  and positive/negative trigger fixtures.
- `gh skill publish .agents/skills --dry-run` is not a clean publication gate
  for this mixed project tree: it also validates the pre-existing
  `executive-council` skill, which lacks required `description` frontmatter.
  No publication was attempted. Public packaging remains a separate,
  human-authorized follow-up.
