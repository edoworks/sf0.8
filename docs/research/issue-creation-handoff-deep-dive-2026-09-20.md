# Issue-Creation Handoff Deep Dive

## Research Charter

- Audience: the sf0.8 owner and maintainers of the shared OpenCode issue-tracking workflow.
- Jurisdiction: local OpenCode configuration and the private `edoworks/sf0.8` GitHub issue workflow; provider behavior is considered only where directly evidenced.
- Decision to inform: whether incomplete issue creation is caused by a model-quality difference, an underspecified planner-to-writer handoff, or another control-plane defect, and what permanent fix permits high-quality planning with lower-cost write execution.
- Date cutoff: evidence available through 2026-09-20.
- Source plan: prefer direct session/tool records, created GitHub issue bodies, repository policies, skills, tests, and official OpenCode/OpenAI documentation; use secondary sources only for independent counterclaims and treat search snippets or generated summaries as leads only.
- Stopping rule: stop when the observed Sol and Luna runs can be compared at the handoff, command, and resulting-issue levels; the strongest alternative explanations have been tested; and a mechanical guard is implemented and verified, or the missing empirical evidence is explicitly identified.

## Initial Evidence Classes

### Known Facts

- The shared issue-tracking skill requires scope, acceptance criteria, and verification in a new issue body.
- Repository-first issue mutations are interactive `ask` operations and must use `--body-file` for multiline text.
- A prior local incident found that delegation omitted decision-critical context and recommended required-field validation before dispatch.

### Open Questions

- Which Sol recommendation, Luna handoff, GitHub mutation, and resulting issue constitute the reported incident?
- Did Luna receive the full planned issue body or only a conversational reference to it?
- Was content lost before model invocation, in model output, in command construction, or after GitHub accepted the write?
- Does any current schema or validator reject an incomplete issue body before mutation?

### Hypotheses

- H1: the writer was asked to reconstruct the issue from conversational context rather than execute a self-contained, immutable handoff.
- H2: Luna omitted fields despite receiving a complete structured handoff.
- H3: command permission or quoting truncated the body rather than the model omitting it.
- H4: the perceived model-quality difference is confounded by different prompts, context windows, agent instructions, or tool permissions.

### Preliminary Recommendation

- Do not depend on writer-model inference. Have the planning step produce a validated issue-intent artifact containing repository, title, complete body, acceptance criteria, verification, dependencies, authority constraints, and an integrity digest; make the write step a deterministic transport that refuses incomplete or changed input.

## Findings

### Executive Answer

- **High confidence:** the apparent issue #73 through #79 incident does not
  confirm the model attribution in the claim. OpenCode's direct session and
  message records identify `gpt-5.6-sol` medium for the body-file creation and
  GitHub issue-create calls. The GitHub bodies match the local files used by
  those calls. [Primary operational records: local OpenCode SQLite database,
  local body files, and GitHub issues #73-#79; retrieved 2026-09-20.]
- **High confidence:** the durable defect is an underspecified handoff contract,
  not a demonstrated Luna transport failure. Completeness was decided while
  writing free-form Markdown; the mutation step had no required schema, digest,
  or post-write equality gate. [Primary source: shared `issue-tracking` skill
  before this correction; retrieved 2026-09-20.]
- **Medium confidence:** Sol may produce more complete plans than Luna on some
  prompts, but this dataset cannot establish that causal claim. The existing
  benchmark gives both models passing standard scores yet contains no issue-
  handoff fixture, and the observed run was not a controlled comparison.
  [Primary test records: `~/.config/opencode/model-routing/benchmarks.json` and
  `benchmark-suite.mjs`; retrieved 2026-09-20.]
- **High confidence recommendation:** keep high-quality planning on the chosen
  stronger model, but make the lower-cost writer transport a validated,
  immutable issue artifact. This has now been implemented in the shared
  issue-tracking skill and validator. [Primary implementation and tests:
  `~/.config/opencode/scripts/issue-intent.mjs` and
  `issue-intent.test.mjs`; verified 2026-09-20.]

### Claim 1: Luna Medium Created the Incomplete Issues

**Evidence for the claim**

- The owner reports observing better behavior from Sol medium and incomplete
  issue creation when Luna medium performed a write. This is direct human
  testimony but does not identify the exact session, prompt, issue, or body.
  [Primary testimony: user report; received 2026-09-20.]
- Numerous Luna sessions on 2026-09-19 and 2026-09-20 contain issue-creation
  language or tool records, so a different unisolated incident remains
  possible. [Primary operational record: local OpenCode SQLite database;
  retrieved 2026-09-20.]

**Counterevidence**

- For the temporally adjacent issues #73 through #79, the session record,
  assistant message records, and tool-call metadata all identify Sol medium.
  The child issues were created from
  `.factory/artifacts/evidence/host-audio-validation-issue-bodies/*.md`.
  [Primary operational records: local OpenCode SQLite database and tool-call
  records; retrieved 2026-09-20.]
- Direct GitHub reads show the issue bodies contain the same headings and text
  as those local source files. There is no observed truncation or mutation at
  the CLI/GitHub transport layer. [Primary records: GitHub issues #73-#79 and
  local source files; retrieved 2026-09-20.]

**Implication**

- The specific attribution is **not confirmed** and is contradicted for the
  most likely incident. A different incident can be evaluated if its issue URL
  or session is supplied, but routing policy should not be changed on this
  evidence.

### Claim 2: The Handoff Was Not Strong Enough for a Lower-Capability Writer

**Evidence**

- Before correction, the skill asked for scope, acceptance criteria, and
  verification but supplied no schema, canonical section set, integrity digest,
  or equality check. A writer could omit, summarize, or faithfully transport an
  already incomplete body without a failing signal. [Primary policy source:
  `~/.config/opencode/skills/issue-tracking/SKILL.md`; retrieved 2026-09-20.]
- A prior repository incident independently found the same class of failure:
  delegated research omitted decision-critical context because it relied on
  surrounding conversation, and recommended required-field validation before
  dispatch. [Primary incident record:
  `.factory/artifacts/evidence/research-scope-failure-5whys-2026-09-20.md`;
  retrieved 2026-09-20.]
- GitHub CLI supports explicit body files for creation and structured JSON for
  readback, so exact transport and comparison are available without asking a
  model to rewrite content. [Primary vendor documentation: GitHub CLI
  [`issue create`](https://cli.github.com/manual/gh_issue_create) and
  [`issue view`](https://cli.github.com/manual/gh_issue_view); retrieved
  2026-09-20.]

**Counterevidence**

- The inspected writer did faithfully use `--body-file`; therefore the defect
  is not evidence that every lower-capability writer will alter content. It is
  evidence that faithful transport alone cannot repair an incomplete plan.
- OpenAI documents that schema-constrained structured outputs can prevent
  required-key omissions, supporting a structured planner artifact, but schema
  conformance alone does not prove the semantic content is sufficient for the
  real decision. [Primary vendor documentation: OpenAI
  [Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs);
  retrieved 2026-09-20.]

**Implication**

- Use the stronger model for semantic planning, then freeze its result. Do not
  ask the writer to infer or improve semantics; deterministic validation should
  reject incomplete input before mutation.

### Claim 3: Existing Model Benchmarks Justify the Current Writer Route

**Evidence**

- Luna and Sol both passed the local standard benchmark suite. The active route
  registry selects Luna for standard work and reserves Sol for trust review.
  [Primary test/config records: `benchmarks.json`, `approved.json`; retrieved
  2026-09-20.]

**Counterevidence**

- The standard suite tests a missing `await`, an authorization-default change,
  and a Docker-socket policy. It does not test planner-to-writer fidelity,
  required issue fields, or readback equality. Equal scores therefore do not
  falsify the owner's broader quality observation. [Primary test definition:
  `benchmark-suite.mjs`; retrieved 2026-09-20.]
- OpenAI's eval guidance says evaluations should encode the actual task and its
  specified content criteria. The current benchmark is not task-valid for this
  claim. [Primary vendor documentation: OpenAI
  [Working with evals](https://platform.openai.com/docs/guides/evals);
  retrieved 2026-09-20.]

**Implication**

- Do not infer issue-handoff parity from the generic benchmark. If model-level
  comparison remains decision-relevant after the deterministic fix, add a
  repeated, blinded issue-intent eval rather than relying on one anecdote.

## Conflicts and Unknowns

- The owner's recollection attributes an incomplete write to Luna, while the
  likely incident's direct records attribute all seven issue creates to Sol.
  Both are preserved; the direct record controls the scoped conclusion.
- The exact content the owner expected but found missing is unknown. The child
  issues include outcome, acceptance criteria, dependencies, and verification,
  but omit explicit non-goals, authority/privacy, and source provenance as
  standardized sections.
- No controlled Sol-versus-Luna trial exists with identical context, prompt,
  tools, and scoring. General relative model quality remains an untested
  hypothesis here.
- Local OpenCode records are direct operational evidence but are mutable local
  state, not an independently attested audit log.
- OpenAI's public documentation does not provide decision-relevant comparative
  evidence for these local `gpt-5.6-sol` and `gpt-5.6-luna` routes.

## Decision Implications

- Keep high-capability planning if it provides value, but require it to emit a
  complete body plus JSON intent and SHA-256 digest.
- Use a routine, lower-cost writer only for validation, the separately approved
  exact `gh issue create --body-file` call, and remote equality verification.
- Do not let the writer summarize or reconstruct the planner's result from chat.
- Keep GitHub `ask` authorization visible. OpenCode documents that `--auto`
  automatically approves `ask`, so issue mutation remains prohibited in auto
  mode. [Primary vendor documentation: OpenCode
  [Permissions](https://opencode.ai/docs/permissions/); retrieved 2026-09-20.]
- The correction is implemented in the global skill and validator. Five focused
  tests and all 38 shared OpenCode tests pass.

### What Would Change the Conclusion

- A specific Luna-created issue and session showing that Luna received a valid,
  digest-matching complete intent but created a different remote title/body
  would move the root cause toward writer/tool execution.
- Repeated blinded trials in which Luna fails the same complete issue-intent
  task materially more often than Sol would support a model-specific routing or
  qualification decision.
- Evidence that GitHub or `gh` changed a supplied body file would invalidate the
  current transport-layer conclusion.
- Failures that pass the new negative fixtures would show the mechanical guard
  is incomplete and require expanding the schema or parser.

## Final Evidence Classes

### Known Facts

- Issues #73 through #79 were created from local body files under a Sol-medium
  session and match those source files.
- The prior workflow had no machine-enforced semantic completeness or readback
  equality contract.
- The new validator rejects missing sections, digest drift, path escape, and
  remote drift in tests.

### Open Questions

- Which exact missing details triggered the owner's observation?
- Was there a separate Luna incident outside issues #73 through #79?
- Does either model differ materially on a controlled issue-planning eval?

### Hypotheses

- A stronger planner may create richer semantic content.
- Conversation-dependent delegation increases omissions regardless of model.
- Deterministic transport should make writer model capability largely
  irrelevant once a complete artifact exists.

### Recommendations

- Adopt the planner artifact plus deterministic writer workflow now.
- Do not change model routing based on this incident alone.
- Add a model comparison only if omissions recur after validator adoption.

## Sources

### Primary

- User incident report, received 2026-09-20.
- Local OpenCode SQLite session/message/tool records, retrieved 2026-09-20.
- GitHub issues #73-#80 and their local body artifacts, retrieved 2026-09-20.
- Shared issue-tracking skill, route registry, benchmark results, and benchmark
  fixtures, retrieved 2026-09-20.
- Repository 5-Whys records, retrieved 2026-09-20.
- [GitHub CLI issue create](https://cli.github.com/manual/gh_issue_create),
  retrieved 2026-09-20.
- [GitHub CLI issue view](https://cli.github.com/manual/gh_issue_view), retrieved
  2026-09-20.
- [OpenAI Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs),
  retrieved 2026-09-20.
- [OpenAI Working with evals](https://platform.openai.com/docs/guides/evals),
  retrieved 2026-09-20.
- [OpenCode Permissions](https://opencode.ai/docs/permissions/), retrieved
  2026-09-20.
- [OpenCode Agent Skills](https://opencode.ai/docs/skills/), retrieved
  2026-09-20.

### Secondary

- None used. The decision was answerable from direct records and official
  documentation.

### Lead-Only

- None relied upon. Search snippets and generated summaries were excluded.
