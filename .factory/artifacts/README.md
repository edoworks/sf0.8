# Artifact Registry

This directory is the Git-visible registry for reusable factory artifacts. A
record describes what may be evaluated; it does not authorize installation,
execution, publication, or a change to repository visibility.

## Record contract

Each `records/*.json` file follows `schema.json`. Records must include a
source revision, SPDX license and compatibility check, provenance, test and
documentation evidence, secrets-scan status, and the human-only publication
flag. External material is metadata only until a human separately approves a
reviewed intake path.

## Gates

Run `python3 scripts/validate-ecosystem.py`. The reuse gate requires a search
effort proportional to the requested change before `BUILD_NEW` is accepted.
The contribution gate classifies product-specific work separately from
generalized internal, public, or upstream candidates. Neither gate publishes
or executes an artifact.

The Product A ledger at `ledger/product-a-candidates.json` is dogfood evidence,
not an authorization to revive, publish, or install Product A code.
