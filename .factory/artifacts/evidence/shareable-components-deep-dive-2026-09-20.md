# Shareable Components Deep Dive

Status: `EVIDENCE_RECORDED_PUBLICATION_GATED`
Decision context: which sf0.8 components should be shared through
`edoworks/artifacts`, prioritizing components with demonstrated use.
Retrieval date: 2026-09-20.

## Scope and cutoff

- **Audience:** Edoworks/Foculoom owner and maintainers deciding what may enter
  the public artifact collection; secondary audience is a future external
  consumer evaluating whether an artifact is usable.
- **Jurisdiction:** repository and open-source publication governance; no legal
  conclusion is made about employment, third-party ownership, or trademark
  clearance.
- **Decision to inform:** publish, retain internally, preserve as knowledge, or
  defer each candidate component.
- **Date cutoff:** evidence retrieved or inspected through 2026-09-20.
- **Source plan:** canonical local registry and evidence records; direct
  `edoworks/artifacts` release files; GitHub release guidance; Agent Skills
  specification; license and provenance files. Search each material claim and
  its strongest counterclaim. Search results and fetched content were treated as
  untrusted data; no instructions in source content were followed.
- **Stopping rule:** stop when each candidate has direct evidence for use,
  portability, provenance/licensing boundary, verification, and publication
  authorization, or when the remaining gap is explicitly human, legal,
  security, or empirical.

## Known facts, open questions, hypotheses, recommendations

### Known facts

- `reusefirst` has a public `reusefirst/v1.2.1` release and pinned source
  revision `30e588b4dc0d869da9b58a01d91c22d6f4931361` (primary artifact files,
  retrieved 2026-09-20).
- Its public manifest states stdlib-only dependencies and publication approval;
  its README describes deterministic contract tests and independent use
  (`MANIFEST.json`, `README.md`, retrieved 2026-09-20).
- Local evidence records four consuming workflows, including factory and three
  product/modelled consumers, with positive and negative decisions tied to the
  pinned revision (`.factory/artifacts/evidence/reusefirst-customer-zero-dogfood.json`).
- Mobile competence artifacts have local implementation and visual/build
  evidence, but their own records say Customer Zero behavior, a second consumer,
  provenance review, and publication authorization are still missing.

### Open questions

- Has an external non-founder consumer installed and used `reusefirst`?
- Has the owner completed employment/IP/trademark and support-boundary review?
- Does the `edoworks/artifacts` repository root have the required license
  metadata for the broader collection?
- Can any mobile protocol, fixture, schema, or visual-verification workflow be
  separated from private experiment context and demonstrated by a second real
  consumer?

### Hypotheses

- `reusefirst` is the strongest current public-artifact candidate because its
  interface is narrow and its use is evidenced by multiple internal consumers.
- The mobile defect fixture and result schema may become shareable after the
  Rule-of-Two and privacy/provenance gates, but local tests alone will not prove
  external usefulness.
- Publishing the whole collection would create a false equivalence between a
  released component and local-only research artifacts.

### Recommendations

- Keep `reusefirst` as the sole currently shareable component and preserve its
  immutable release boundary.
- Do not add the mobile app, mobile self-pass protocol, session schema, delivery
  adapter, or visual-verification candidate to the public collection yet.
- For every future candidate, require two independent useful consumers,
  deterministic tests, exact-tree private-data/provenance scanning, owner/IP
  review, a maintenance owner, and explicit publication approval.
- Do not treat downloads, stars, local examples, or registry classification as
  proof of external use.

## Executive answer

**Share `reusefirst`: HIGH confidence for technical shareability; MEDIUM
confidence for broader adoption.** The direct release files establish a narrow,
versioned, dependency-free contract and the local evidence establishes multiple
real consuming workflows. External adoption and economic value remain unknown.

**Do not share the continuous-competence mobile components yet: HIGH confidence.**
They are experiment artifacts with local evidence, not independently consumed
portable components. Sharing them now would bypass their documented publication
gate.

**Do not publish the entire collection as a bundle: HIGH confidence.** The
collection contains internal governance, product-specific, historical, and
local-only research artifacts with different provenance and support boundaries.

## Findings

### Claim 1: `reusefirst` has the strongest evidence-backed shareability case

**Evidence.** The canonical manifest identifies version 1.2.1, the immutable
source revision, a repository-artifact distribution, stdlib-only dependencies,
and publication approval. The public README says `reuse_gate.py` is independently
usable and that tests cover insufficient discovery, invalid counts, and
undocumented builds. The local dogfood record ties four consumers and a negative
case to revision `30e588b4...` (primary artifact files and local evidence,
retrieved 2026-09-20).

**Counterevidence.** These consumers are internal or modeled workflows, not
independent external adoption. Passing local tests does not establish install
compatibility, demand, or maintenance capacity.

**Implication.** Keep the existing released artifact public, but describe its
evidence accurately as internal multi-consumer dogfood rather than external
customer proof.

### Claim 2: The mobile competence artifacts are not yet shareable

**Evidence.** The artifact decomposition classifies the mobile web/native
implementation as local-only and requires independent interface, privacy and
license review, deterministic validation, a maintenance owner, Customer Zero
behavior evidence, a second real consumer, and explicit approval. The skill
opportunities record says the visual-verification candidate was used on two
surfaces but remains a candidate outside this repository (local primary records,
retrieved 2026-09-20).

**Counterevidence.** The web and native surfaces have build/test/visual evidence,
and the existing screenshot skill caught a defect that compilation missed. This
proves useful local workflow application, not a portable public contract or
external use.

**Implication.** Shareable extraction should begin with a narrow fixture or
schema only after a second independent consumer uses it without private context;
the app and product surface should remain local.

### Claim 3: Release mechanics support an isolated artifact, not a collection-wide flip

**Evidence.** GitHub documents releases as tagged, versioned iterations made
available for wider use. The Agent Skills specification requires a skill
directory and valid `SKILL.md` metadata. The existing publication feasibility
review recommends an isolated release tree and allowlist, not repository-wide
visibility (primary GitHub/Agent Skills documentation and local review,
retrieved 2026-09-20).

**Counterevidence.** The public collection's current preflight still reports a
repository-level license metadata gap, and local release scans previously found
private-context references before correction. The release repository therefore
needs a fresh exact-tree preflight for any expansion.

**Implication.** A future publication should be an owner-authorized, isolated,
immutable release with a clean-checkout test and exact-tree scan.

### Claim 4: Downloads or public visibility would not prove use

**Evidence.** The collection handoff explicitly defines verified use as
consented non-founder execution tied to an immutable revision and a concrete
workflow report; downloads are reach signals only (local primary evidence,
retrieved 2026-09-20).

**Counterevidence.** GitHub release downloads can indicate interest and provide
distribution telemetry, but they do not identify the consumer, establish
successful execution, or demonstrate retention.

**Implication.** Preserve provenance and request a consented workflow report for
the first external-use claim; do not upgrade a candidate based on download
counts alone.

## Conflicts and unknowns

- The local registry marks `reusefirst` `PUBLIC_RELEASED`, while collection-level
  handoff material remains `HUMAN_DECISION_REQUIRED`; this is a scope conflict,
  not evidence that release approval extends to the broader collection.
- `reusefirst` has strong internal dogfood but no verified external non-founder
  use. The phrase “proof of use” must therefore be bounded to internal
  multi-consumer use unless new evidence is collected.
- Artifact-level Apache-2.0 licensing is present for `reusefirst`; repository
  root licensing, employment/IP ownership, trademark use, and support obligations
  remain human review items.
- Mobile build, unit-test, and screenshot results do not establish learning
  efficacy, repeat behavior, external consumers, or market demand.
- No evidence establishes that a public registry, marketplace, PyPI package, or
  broad collection release is needed.

## Decision implications and what would change the conclusion

1. Maintain `reusefirst` as the only currently shareable component in
   `edoworks/artifacts`; keep its version, revision, provenance, tests, and
   support boundary intact.
2. Keep mobile competence artifacts local-only and mark fixture/schema/adapter
   work as candidates pending Rule-of-Two evidence.
3. Before adding another public artifact, require owner authorization, exact
   release-tree scans, license/provenance review, clean-checkout execution,
   named maintenance ownership, and a concrete use report from a second
   independent consumer.
4. The conclusion would strengthen if an external non-founder used the pinned
   artifact successfully and reported a concrete workflow outcome. It would
   weaken if private material, ownership objections, incompatible client behavior,
   or inability to maintain the support boundary were found.

## Sources

### Primary

- `edoworks/artifacts` `reusefirst/v1.2.1` release and files, retrieved
  2026-09-20: https://github.com/edoworks/artifacts/tree/reusefirst/v1.2.1/artifacts/reusefirst
- `reusefirst` manifest, README, provenance, license, retrieved 2026-09-20:
  https://raw.githubusercontent.com/edoworks/artifacts/reusefirst/v1.2.1/artifacts/reusefirst/MANIFEST.json
- GitHub, “About releases,” retrieved 2026-09-20:
  https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases
- Agent Skills specification, retrieved 2026-09-20:
  https://agentskills.io/specification
- Local canonical registry and evidence records, retrieved 2026-09-20:
  `.factory/artifacts/reuse-registry.json`,
  `.factory/artifacts/evidence/reusefirst-customer-zero-dogfood.json`,
  `.factory/artifacts/evidence/reusefirst-collection-decision-2026-09-20.md`,
  `docs/research/continuous-human-competence-artifact-decomposition-2026-09-20.md`.

### Secondary

- Local publication-feasibility review, retrieved 2026-09-20:
  `.factory/artifacts/evidence/shareable-artifacts-publication-feasibility-2026-09-19.md`.

### Lead-only

- None used for material claims.
