# PR Policy CI Runner Failure: 5-Whys

Date: 2026-09-20

## Scope

- Audience: sf0.8 owner and maintainers.
- Decision: make the policy job pass on a clean runner without inventing
  telemetry or depending on private sibling workspaces.
- Evidence: PR #61 policy run `35486016644`, cutoff 2026-09-20.

## 5-Whys

1. **Why did the policy job fail after the changed-path gate passed?** Unit
   tests raised `sqlite3.OperationalError: no such table: runs` and the
   portfolio test could not find the Veilsort candidate.
2. **Why were those assumptions false?** A clean runner has no initialized
   disposable `.factory/factory.sqlite` schema and no private `/Users/hello`
   sibling repositories.
3. **Why did local verification miss this?** The developer workspace supplied
   both incidental state sources, while the tests used implicit defaults instead
   of hermetic fixtures.
4. **Why did the tests use implicit state?** The original tests were written
   as local archaeology checks and did not distinguish canonical evidence from
   optional workspace observations.
5. **Why was that distinction not enforced?** The policy job lacked a clean
   runner fixture contract for disposable telemetry and independent discovery.

## Corrections

- Return explicit `UNKNOWN` telemetry when the disposable ledger is absent or
  uninitialized; never fabricate zero cost or run counts.
- Make the portfolio discovery test construct its own history and product
  fixture, preserving the same bundle/provenance assertions without private
  absolute paths.
- Keep canonical external/sibling observations as optional evidence, not test
  prerequisites.

## Recurrence Guard

The unit suite now exercises the same code on clean, self-contained inputs. A
future test that depends on private workspace state will fail review because it
cannot construct its evidence within the test boundary.
