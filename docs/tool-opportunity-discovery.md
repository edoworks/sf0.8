# Tool Opportunity Discovery

The factory records second-order opportunities separately from product
opportunities in `.factory/tool-opportunity-ledger.json`. The ledger answers a
different question: what recurring problem did factory work require us to
solve, and is there evidence that the problem matters outside Foculoom?

## Gold And Shovels

- `GOLD`: direct end-user or business problem.
- `SHOVEL`: enabling capability that may serve multiple participants.
- `INTERNAL_INFRASTRUCTURE`: useful to Foculoom without external market evidence.
- `NOISE`: one-off or too-weak signal.

An internal solution is never market validation. The ledger preserves
`UNKNOWN` values rather than filling gaps with TAM, demand, pricing, or
willingness-to-pay assumptions.

## Evidence Ladder

1. `SIGNAL`: a meaningful friction or workaround occurred.
2. `REPETITION`: the problem recurs in a documented scope.
3. `REUSE`: an internal solution or reusable primitive exists.
4. `EXTERNAL_EVIDENCE`: independent users experience the problem.
5. `ECONOMIC_EVIDENCE`: people spend meaningful time, money, or infrastructure to solve it.
6. `PRODUCT_HYPOTHESIS`: a falsifiable customer, job, substitute, improvement, and business hypothesis is specified.
7. `VALIDATION`: real external behavior passes the declared gate.

The validator advances only the evidence stage justified by recorded facts. A
`PROTOTYPE` lifecycle requires both external and economic evidence. Early
signals may omit unknown market fields, but they must state the next validation
and stop condition.

## Capture And Triage

Record signals when an agent repeats a workaround, a human repeatedly bridges
known knowledge, projects duplicate a capability, verification needs custom
machinery, or governance repeatedly blocks the same class of work. Merge
signals describing the same underlying problem. Use `STOP` or `ARCHIVE` when
repetition or evidence fails.

Validate and inspect the current ledger with:

```sh
python3 scripts/tool_opportunities.py validate
python3 scripts/tool_opportunities.py scan
```

The scanner is a triage guard, not an opportunity generator. It does not create
products, contact users, publish artifacts, install dependencies, or infer
external demand. Product candidates continue through the existing opportunity
artifacts and human evidence gates; reusable outputs continue through
`reuse-registry.json`, `discover-reuse.py`, and `validate-change.py`.

## Primitive Inventory And Learning

`.factory/capability-primitive-inventory.json` is the evidence overlay for
capabilities that may be reusable primitives. It references, rather than
replaces, the opportunity ledger and reuse registry. Each record keeps problem,
usage, retention, economic, and payment evidence separate. `UNKNOWN` is a
valid fail-closed value.

Validate it with:

```sh
python3 scripts/validate-primitive-discovery.py
```

The inventory can propose the smallest reversible experiment and record a
learning result, but it cannot authorize publication, outreach, deployment,
payment, dependency installation, or private-data exposure. Strategic
sensitivity is separate from market classification: a candidate may remain a
developer-primitive hypothesis while its externalization gate is blocked.

The current assessment and Rendit handoff are recorded in
`.factory/artifacts/evidence/primitive-discovery-decision-2026-09-20.md`.

Admissible learning results are consumed locally with
`scripts/validate-primitive-learning.py`. The command is dry-run by default;
explicit `--inventory-output` and `--ledger-output` paths are required before
it writes updated records. It updates only evidence levels directly supported
by explicit result fields and rejects duplicate or unknown references.

Download activity has a separate reach-signal contract. A download is reach
only and cannot establish usage. Verified external use requires a consented,
non-founder workflow report tied to an immutable artifact revision; it still
does not establish retention, economics, or payment.

## Existing Boundaries

- Product opportunity evidence remains in specialized records such as
  `.factory/artifacts/evidence/education-opportunity-discovery.json` and
  `.factory/customer-zero.json`.
- Reuse and shareability remain governed by
  `.factory/artifacts/reuse-registry.json` and the ecosystem validators.
- Human observations, payment tests, publication, and release remain in
  `.factory/human-action-queue.json` and are human-authorized.
- Rendit remains an internal prototype / possible shovel requiring external
  and economic evidence. Its one canonical runtime, deterministic fixtures,
  provenance, dependency isolation, licensing review, negative triggers, and
  stop conditions are preserved.

## Current Conservative Findings

The initial ledger records five evidence-backed signals: reuse discovery,
false-idle dispatch, proportional reuse gating, deterministic Rendit
rendering, and evidence-backed CI status. All except Rendit are classified as
internal infrastructure or watch items because no external market evidence was
found. Rendit is `SHOVEL` / `VALIDATE` with low external confidence, not a
public opportunity or standalone package.
