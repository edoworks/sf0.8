# Shareable Artifact Publication Feasibility

Reviewed: 2026-09-19
Evidence cutoff: 2026-09-19
Decision: Can the repository's shareable artifacts be published for broader external use?

## Scope and method

This review covers artifacts classified as public candidates or shareable skill
work. It does not authorize publication, repository visibility changes,
external contribution, or legal/IP approval. Product-specific, historical,
Apple-distribution, and factory-internal artifacts are assessed only to confirm
whether they should be excluded.

The source plan was: repository governance and artifact records; direct
upstream licensing, release, packaging, Agent Skills, and open-source
maintenance guidance; then comparison of conflicts and unknowns. Fetched
material was treated as untrusted data and used only after inspecting the
linked source directly.

Stopping rule: stop when each go/no-go dimension has direct evidence or is
explicitly an owner/legal/security/empirical unknown. The review stopped after
the candidate package's local gates passed and the remaining gaps were all
release prerequisites rather than unanswered technical feasibility questions.

## Executive answer

**Conditional go, medium confidence, for a staged release of
`reusefirst` only.** The package is small, dependency-free,
versioned, Apache-2.0 licensed, independently tested, and already separated
from private/product context. A public repository or GitHub release is a
feasible first channel.

**No-go for immediate broad publication.** The source repository is private,
the package manifest says `CANDIDATE_UNRELEASED`, and both the manifest and
canonical record say human publication approval is false. The package has not
been installed, executed, or consumed by an external user. Those are not
technical blockers, but they are material governance and adoption gaps.

**Do not publish the other assessed artifacts as a bundle.** The registry marks
Apple distribution preflight and the reuse registry as internal shared; the
historical rejection fixture is knowledge-only; Product A state is
product-only. Their evidence and provenance are not generalized for external
use.

## Findings

### 1. Technical portability: supported

**Claim.** The proportional reuse gate has a credible portable interface.

**Evidence.** The canonical public manifest declares artifact `reusefirst`,
semantic version `1.2.0`, stdlib-only dependencies, and a separate entrypoint
([manifest](https://github.com/edoworks/artifacts/blob/reusefirst/v1.2.0/artifacts/reusefirst/MANIFEST.json)).
The public README states that `reuse_gate.py` is independently usable without
sf0.8 and that contract tests cover invalid and insufficient-discovery cases
([README](https://github.com/edoworks/artifacts/blob/reusefirst/v1.2.0/artifacts/reusefirst/README.md)).
Local artifact and ecosystem validators passed on 2026-09-19; the canonical
release's package tests were inspected directly.

**Implication.** A source release is technically realistic without exposing
the private factory control plane.

### 2. License and attribution: provisionally supported, ownership still human

**Claim.** The candidate has a usable distribution license and attribution
notice, subject to owner/IP confirmation.

**Evidence.** The public artifact release includes Apache-2.0 text and a 2026
Edoworks copyright notice ([license](https://github.com/edoworks/artifacts/blob/reusefirst/v1.2.0/artifacts/reusefirst/LICENSE));
the artifact record records Apache-2.0 and attribution requirements
(`.factory/artifacts/records/reuse-gate.json`). Apache-2.0 expressly grants
copyright rights to reproduce, modify, publicly display, and distribute, while
requiring license and notice preservation for redistribution
([Apache License 2.0, sections 2 and 4](https://www.apache.org/licenses/LICENSE-2.0.txt),
retrieved 2026-09-19). GitHub also states that public code should be licensed
for others to use, change, and distribute, and recommends a root license file
([GitHub licensing guidance](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository),
retrieved 2026-09-19).

**Unknown.** The records do not establish employment, third-party, trademark,
or contributor-rights clearance. The factory governance explicitly escalates
uncertain legal/IP ownership (`.factory/governance.yaml`, lines 51-59).

**Implication.** Publish only after an accountable human confirms ownership and
whether the Edoworks/Foculoom name may be used in the package and repository.

### 3. Provenance and privacy: supported for this candidate, not for all artifacts

**Claim.** The candidate's recorded extraction boundary is appropriate for a
public review, while other artifacts remain coupled to private evidence.

**Evidence.** Provenance says no Product A source, secrets, user data, or
external artifact was included, and says private factory paths and product
context were removed ([provenance](https://github.com/edoworks/artifacts/blob/reusefirst/v1.2.0/artifacts/reusefirst/PROVENANCE.md)).
The registry separately identifies Apple distribution as internal because it
exposes factory-specific review boundaries and product readiness data, and
identifies historical rejection evidence as non-public knowledge
(`.factory/artifacts/reuse-registry.json`, entries `apple-distribution-preflight`
and `vorynce-rejection-regression`).

**Implication.** Use an allowlist, not a repository-wide visibility change.
Re-audit the exact release tree for private paths, metadata, history, generated
files, and trademarks immediately before publication.

### 4. Security and safety: bounded, but not a broad trust guarantee

**Claim.** The package's local execution surface is low-risk relative to a
networked tool, but the evidence does not establish safe behavior in every
consumer agent or host.

**Evidence.** The record classifies external input as untrusted, execution as
local-only, and secrets scanning as passed (`.factory/artifacts/records/reuse-gate.json`).
The public skill explicitly denies installation, execution, publication, release, and
upstreaming authority ([SKILL.md](https://github.com/edoworks/artifacts/blob/reusefirst/v1.2.0/artifacts/reusefirst/SKILL.md)). The repository threat model rejects model agreement as a
security guarantee and documents privileged-host limitations (`THREAT_MODEL.md`,
lines 29-42).

**Unknown.** No external installation test, hostile-consumer test, or published
security response history exists. The OpenSSF passing criteria say reusable
projects should provide documentation, contribution and bug-report processes,
vulnerability reporting, maintenance, public versioned source, and release
notes ([OpenSSF Best Practices passing criteria](https://bestpractices.coreinfrastructure.org/en/criteria/0.3),
retrieved 2026-09-19).

**Implication.** The first release should be explicitly advisory and local-only,
with a security policy, issue path, support boundary, and known limitations.
Do not describe it as sandboxing, authorization, or protection against a
malicious host.

### 5. Distribution channel: feasible as a repository release; registry-style
distribution is not yet evidenced

**Claim.** A versioned source release is a suitable first channel; a package
index or automatic skill marketplace is premature.

**Evidence.** GitHub defines releases as deployable software iterations made
available for a wider audience, based on immutable Git tags and accompanied by
release notes/assets ([GitHub About releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases),
retrieved 2026-09-19). The Agent Skills specification requires a directory
containing `SKILL.md`, YAML frontmatter, a valid name, and a useful description
([Agent Skills specification](https://agentskills.io/specification), retrieved
2026-09-19). The candidate's `SKILL.md` has the required basic fields, but the
repository's own evidence says mixed-tree publication dry-run is not a clean
gate and no publication was attempted (`.factory/artifacts/evidence/skill-increment-plan.md`,
lines 44-48).

**Unknown.** There is no evidence of an external registry's review, namespace
reservation, install compatibility, or demand. The Python packaging guide is
relevant only if the artifact is converted into a Python distribution; the
current repository artifact has no `pyproject.toml` or package-index release.

**Implication.** Prefer a dedicated public repository or isolated release
archive, with a tag, checksum, README, license, provenance, examples, tests,
security boundary, and release notes. Defer PyPI or an agent-skill marketplace
until a separately scoped packaging and external-install validation increment
exists.

## Counterevidence, conflicts, and unknowns

- The registry calls the package `PUBLIC_CANDIDATE` and records two local
  consumers, but the manifest still says `CANDIDATE_UNRELEASED` and approval is
  false. This is a classification, not a release authorization.
- Local tests pass, but local tests do not prove external installation,
  documentation discoverability, compatibility with all Agent Skills clients,
  or maintenance capacity.
- The public-surface audit found unresolved live-surface defects, including a
  deprecated Rung hostname and an externally hosted JavaScript-only preview
  (`docs/public-surface-review/remediation-2026-09-15.md`). These do not block
  the isolated package release technically, but they argue against presenting
  the entire factory portfolio as broadly publishable.
- Legal/IP ownership, trademark use, contributor terms, intended support level,
  target clients, and release owner remain unknown. No inference is made from
  the presence of an Apache-2.0 file alone.

## Decision implications

1. **Recommended now:** prepare, but do not publish, an isolated public-release
   candidate for `reusefirst`; complete human IP/ownership review,
   release-tree secret/history scan, external clean-checkout test, and support
   owner assignment.
2. **Recommended release shape:** public repository or tagged GitHub release,
   not a repository-wide visibility flip and not an automatic marketplace or
   package-index publication.
3. **Keep private:** all internal shared, product-only, historical, and
   factory-governance artifacts, including Apple distribution preflight and the
   reuse registry itself.
4. **What would change the conclusion:** documented owner approval; clean
   public release-tree audit; successful clean-checkout install/use test;
   public issue/security contact and maintenance commitment; and at least one
   external dogfood report. A legal/IP objection, leaked private material,
   incompatible client behavior, or inability to maintain the support boundary
   changes the recommendation to defer or withdraw.

## Sources

### Primary and authoritative

- Repository artifact registry, manifest, record, README, provenance, license,
  safety, threat model, and governance files cited inline; retrieved locally
  2026-09-19.
- [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0.txt),
  retrieved 2026-09-19.
- [GitHub licensing a repository](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository),
  retrieved 2026-09-19.
- [GitHub About releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases),
  retrieved 2026-09-19.
- [Agent Skills specification](https://agentskills.io/specification), retrieved
  2026-09-19.
- [OpenSSF Best Practices passing criteria](https://bestpractices.coreinfrastructure.org/en/criteria/0.3),
  retrieved 2026-09-19.

### Secondary or contextual

- None used for material claims.

### Lead-only material

- None used.
