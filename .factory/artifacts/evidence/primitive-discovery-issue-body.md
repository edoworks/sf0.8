# Scope

Extend the existing evidence-first tool-opportunity system into a governed capability primitive inventory and externalization-learning gate. Reuse the tool opportunity ledger, reuse registry, ecosystem gates, evidence frontier, and human-action queue. Do not create a public API, billing system, telemetry pipeline, package, or autonomous outreach.

## Acceptance criteria

- Inventory records reference existing registry and opportunity records without duplicating their authority.
- Technical reuse, problem, usage, retention, economic, and payment evidence remain separate and UNKNOWN is fail-closed.
- Strategic classifications include internal advantage, open distribution, developer primitive, metered infrastructure, product candidate, and insufficient evidence.
- Externalization proposals require risk review, a measurable learning objective, the cheapest reversible experiment, and human authorization.
- Learning records can update a tool opportunity without treating usage as payment or internal recurrence as external demand.
- Existing capabilities, including Rendit, are assessed with evidence-backed classifications and a human-action request for the next authorized experiment.
- Targeted and full factory tests pass; no publication, outreach, payment, or external deployment occurs.

## Verification

```text
python3 scripts/validate-primitive-discovery.py
python3 -m unittest tests.test_primitive_discovery tests.test_tool_opportunities
python3 scripts/validate-ecosystem.py
python3 -m unittest discover -s tests -p 'test_*.py'
```

## Safety boundary

External publication, deployment, outreach, interviews, payment, pricing, dependency installation, and private-data exposure remain human-authorized. The implementation may only inspect, classify, prepare evidence, and queue a bounded action.
