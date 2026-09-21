# Scope

Add a local, deterministic ingestion path for admissible primitive-learning records. The path may update the capability inventory and linked tool-opportunity evidence, but it must not perform outreach, publish, deploy, request payment, or infer evidence from missing fields.

## Acceptance criteria

- Learning records require explicit problem observation, usage, retention, economic, payment, workflow, consent, and non-synthetic fields.
- Ingestion updates only evidence levels directly supported by the record.
- Payment stages remain distinct from usage, retention, and economic evidence.
- Linked tool-opportunity candidates are updated only through explicit capability mappings.
- Duplicate result IDs and unknown primitive/opportunity IDs are rejected.
- The command is local and deterministic; it does not contact external systems or mutate the source records unless an explicit output path is supplied.
- Existing human authorization boundaries remain unchanged.

## Verification

```text
python3 scripts/validate-primitive-learning.py
python3 -m unittest tests.test_primitive_learning tests.test_primitive_discovery
python3 -m unittest discover -s tests -p 'test_*.py'
```

## Safety boundary

External observation, outreach, consent collection, payment, publication, deployment, and private-data transfer remain human-authorized. This increment only consumes an already-admissible local evidence record.
