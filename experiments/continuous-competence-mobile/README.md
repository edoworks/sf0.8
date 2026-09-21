# Continuous Competence Mobile Experiment

Status: `EXPERIMENT_ARTIFACT`, local-only, issue #50.

This is a dependency-free mobile web instrument for Customer Zero feasibility
testing. It can be added to a phone or iPad home screen and caches its local
assets for offline use. It is not a product, tutor, assessment, credential, or
educational effectiveness claim.

## Run

Serve this directory locally, then open:

- `index.html?mode=intervention` for independent recall plus controlled defect inspection.
- `index.html?mode=control` for the ordinary-method comparison.

Example:

```bash
python3 -m http.server 8080 --directory experiments/continuous-competence-mobile
```

Results are stored in browser `localStorage` and can be exported manually.
There is no account, analytics, model call, or upload. The service worker only
caches the experiment's own static assets.

The bundled exercise bank includes Scala and SQL questions for general software
engineering plus financial transaction processing with Spark Structured
Streaming, Azure Synapse Analytics, Azure Event Hubs, and Azure Data Lake
Storage Gen2. Each question includes visible boundary cases, progressive hints,
an explanation, and a reference.

The local runner executes predefined exercise contracts in the page's
JavaScript harness; it does not compile arbitrary Scala or SQL source and does
not sandbox untrusted code. General compilation remains an out-of-scope
toolchain capability.

## Fixture

`fixture.json` is the source record for the question bank, defects, repairs,
test cases, and references. `app.js` embeds the same display-safe bank so the
experiment runs as a single local file set; changes must update both and be
checked by the static tests.

## Boundaries

- Use only non-confidential or synthetic code.
- Do not use children as participants in this pass.
- Do not interpret local results as population or payment evidence.
- Do not publish this artifact or add a dependency without human authorization.
