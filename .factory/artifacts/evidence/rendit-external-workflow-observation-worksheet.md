# Rendit External Workflow Observation Worksheet

Status: `PREPARED_NOT_AUTHORIZED`
Related action: `rendit-external-workflow-observation`
Primitive: `primitive:rendit-deterministic-workflow`
Opportunity: `shovel:deterministic-rendering-workflow`

This worksheet prepares one human-authorized observation. It is not permission
to recruit, contact, collect data, publish, deploy, install dependencies, or
request payment.

## Authority Gate

- Participant selected by human: `UNKNOWN`
- Consent obtained and recorded: `UNKNOWN`
- Privacy scope approved: `UNKNOWN`
- Private code, assets, credentials, or source data transferred: `NO`
- Rendit published or installed externally: `NO`
- Payment requested: `NO`

Stop before observation if any required authority value remains `UNKNOWN`.

## Observation Record

Use one stable `result_id`. Do not infer a value from silence or stated praise.

```text
result_id: UNKNOWN
primitive_id: primitive:rendit-deterministic-workflow
opportunity_ids: [shovel:deterministic-rendering-workflow]
user: UNKNOWN
workflow: UNKNOWN
job_to_be_done: UNKNOWN
frequency: UNKNOWN
friction: UNKNOWN
combinations: []
problem_observed: UNKNOWN
usage_observed: UNKNOWN
repeated_use: UNKNOWN
economic_value_observed: UNKNOWN
value_created: UNKNOWN
payment_signal.stage: NONE
payment_signal.raw_action: UNKNOWN
consent.status: UNKNOWN
synthetic: false
```

## Capture Prompts

- What concrete job was the participant trying to complete?
- What substitute or manual workflow did they use before Rendit?
- Was the problem observed directly, or merely described?
- What was the frequency and measurable friction or rework?
- Did the participant actually use the workflow?
- Did they return or request it again after the first use?
- Was time, money, risk, or other economic value measured?
- What payment-ladder stage was actually reached, if any?
- What other tools or primitives were combined with the workflow?

## Ingestion Gate

Only after human review and consent confirmation, convert the record into the
learning-result shape and run:

```sh
python3 scripts/validate-primitive-learning.py RESULT.json
```

Review the dry-run output. Write updated inventory and opportunity records only
with paired explicit output paths after the observation evidence is accepted.

## Stop Conditions

- Stop if consent, privacy, participant identity, or source provenance is unclear.
- Stop if the observation would require publication, deployment, dependency installation, or private-data transfer.
- Stop if a compliment, interest statement, or request for access is being treated as payment evidence.
- Stop if a single observation is being treated as retention or recurring demand.
