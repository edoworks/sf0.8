# False Idle Work Harvesting

Date: 2026-09-19
Issue: #51

## Finding

The prior claim that no safe autonomous work existed is disproved. The
repository contained two `READY` portfolio lanes, three reusable-component
candidate records, report-only hygiene classifications, and a runnable
portfolio-audit validator. Product A and Apple lanes were blocked, but those
blocks were incorrectly treated as factory-wide idleness in the BRB response.

## Causal Chain

1. Work was recorded in separate lane, reuse, hygiene, and evidence artifacts.
2. `scripts/select-lanes.py` inspected only a supplied static lane document and
   had no contract with BRB or a factory-wide dispatcher.
3. No generalized provider harvested non-lane work or produced an exhaustion
   report.
4. BRB had no executable discovery step and treated the human-action queue as
   the autonomous-work universe.
5. The conversational response collapsed blocked human work and undiscovered
   safe work into `WAITING_DEPENDENCY`.

## 5-Whys

1. Why did the factory wait? The BRB path found no directly executable human
   action and returned a global waiting state.
2. Why did it not choose archaeology, reuse, hygiene, or validation? Those
   sources were not connected to a dispatcher.
3. Why was there no dispatcher contract? Existing controls proved that known
   lanes were independent, but discovery and scheduling remained separate
   reports and entrypoint-specific helpers.
4. Why could a report be mistaken for exhaustion? `WAITING_DEPENDENCY` had no
   required machine evidence for sources searched, provider health, candidates,
   rejection reasons, or eligible count.
5. Root cause: factory idleness was a conversational assumption rather than an
   executable, extensible exhaustion decision.

## Correction

`scripts/idle_work.py` defines provider-based discovery and classification.
Every candidate records value, urgency, reversibility, risk, cost, authority,
dependencies, scope, evidence, expected validation, and category. Blocked work
is retained as blocked; eligible bounded work is selected independently.

`WAITING_DEPENDENCY` is legal only when every configured provider succeeds and
the eligible candidate count is zero. Provider failure is `DISCOVERY_FAILED`,
not idle. No provider performs deletion, publication, Product A resumption, or
external mutation.

Immediate correction: the away-for-hours path now runs discovery and dispatches
the highest-priority eligible local task instead of inferring idleness from the
human-action queue. Root-cause correction: provider registration, candidate
classification, and the exhaustion rule are now executable contracts shared by
the CLI, completion gate, tests, and CI.

Recurrence guard: `scripts/validate-idle-work.py` rejects missing providers,
failed-provider exhaustion, incomplete candidate classifications, and any
`WAITING_DEPENDENCY` report with an eligible candidate. The completion gate
applies the same fail-closed rule to completion records.

## Dogfood Evidence

The exact away-for-hours scenario was replayed with Product A still shelved and
human/external blockers unchanged. The provider manifest searched eight sources,
found 11 eligible bounded candidates, selected the local portfolio audit
validator, and executed it successfully. Evidence is recorded in
`.factory/artifacts/evidence/idle-work-dogfood.json`; the discovery report is
`.factory/artifacts/evidence/idle-work-discovery.json`.

The full local suite passed with 145 tests. Existing remote CI run
`35295186391` remains green; the new workflow step is covered by the local
equivalent command and must run on the next authorized CI update.

## Preservation And Reuse

Historical candidates remain read-only and non-disposable. Reuse candidates are
discovered from the canonical registry and evaluated before build; unknown
license/source candidates remain blocked rather than extracted. The existing
registry, preservation manifests, and provenance remain authoritative.
