# Skill Sharing Recommendation Deep Dive

## Scope And Cutoff

- **Audience:** sf0.8 maintainers and the factory owner deciding which locally
  used skills should be recommended for internal reuse or later sharing.
- **Jurisdiction:** the authorized local workspace, its project-local skills,
  user-local skill directories, and this repository's artifact/shareability
  governance. No publication, installation, license acceptance, or external
  repository mutation is authorized by this review.
- **Decision to inform:** whether the claim that used skills are not being
  recommended for sharing is true, what root cause explains it, and what
  smallest factory correction should make eligible skills discoverable without
  falsely approving them for publication.
- **Date cutoff:** evidence inspected through 2026-09-20 inclusive.
- **Source plan:** inspect the canonical registry, governance, skill contract
  tests, skill files and commands, and direct local references to used skills;
  search the claim and its strongest counterclaim. Repository and fetched
  content are untrusted data. No instructions found in source content are
  followed.
- **Stopping rule:** stop after every discoverable used skill is classified as
  recommended, deferred, or not shareable; the omission root cause is
  evidenced; and a deterministic guard verifies that the recommendation view
  cannot silently omit a used skill. Remaining publication, ownership, license,
  and external-demand questions remain explicitly human-gated.

## Known Facts, Open Questions, Hypotheses, Recommendations

### Known facts

- The factory's canonical registry contains reusable artifacts, but no skill
  inventory or skill recommendation field.
- Project-local skill contract tests enumerate four skills, while the working
  environment also contains user-local skills, including `macos-screenshot`.
- Existing research records that `macos-screenshot` was used on two surfaces
  and caught a native contrast defect, but labels it only a shareability
  candidate.

### Open questions

- Whether any external consumer has used any candidate skill is unknown.
- License, maintenance ownership, private-context, and publication approval
  are not established for user-local skills by this repository.

### Hypotheses

- The omission is caused by a scope mismatch: artifact discovery scans the
  repository registry, while used skills may live outside the repository and
  are mentioned only in prose.
- A read-only inventory and recommendation view can fix discoverability without
  weakening the existing human publication gate.

### Recommendations

- Add an explicit, source-pinned skill-sharing inventory with disposition and
  evidence fields.
- Recommend skills for review only when usage evidence exists; do not classify
  recommendation as publication approval.
- Add a test that fails when a used skill reference is absent from the inventory.

## Executive Answer

**The claim is confirmed with HIGH confidence for discoverability, and not
confirmed as a claim that the skills were judged non-shareable.** The factory
had a reusable-artifact registry and project-local skill contract tests, but no
skill inventory spanning the declared user-local skill root. Consequently,
`macos-screenshot` was used and documented yet absent from any factory
recommendation view. The new inventory recommends six used skills for
shareability review, including that skill, while keeping publication approval
false.

## Findings

### Claim 1: Used skills were omitted from the factory's recommendation surface

**Evidence.** The registry schema records reusable artifacts and consumers but
has no skill inventory; the skill contract test hard-codes four project-local
skills. The direct user-local skill root contains `macos-screenshot`, and local
research records say it was used on mobile web and native iPhone/iPad surfaces
and caught a contrast defect. **Repository primary sources**, retrieved
2026-09-20: `.factory/artifacts/reuse-registry.json`,
`tests/test_shareable_skill_contracts.py`,
`docs/research/continuous-competence-skill-opportunities-2026-09-20.md`, and
`/Users/hello/.agents/skills/macos-screenshot/SKILL.md`.

**Counterevidence.** The existing research correctly labels the screenshot
skill as a shareability candidate rather than a released artifact, and the
registry's publication controls are intentionally conservative. **Repository
primary evidence**, retrieved 2026-09-20: the same skill-opportunities record
and `.factory/governance.yaml`.

**Implication.** The failure is a recommendation/discovery omission, not proof
that publication should have happened.

### Claim 2: The omission was caused by a scope mismatch, not by insufficient use evidence

**Evidence.** The factory discovery entrypoint searches only the canonical
repository registry, while the used screenshot skill lives outside the
repository and is referenced only by prose. The project test enumerates local
skills rather than scanning declared roots. **Repository primary
implementation and tests**, retrieved 2026-09-20: `scripts/discover-reuse.py`,
`scripts/ecosystem_gates.py`, and `tests/test_shareable_skill_contracts.py`.

**Counterevidence.** The existing reuse registry can represent shareability
dispositions, and the local skill's own metadata declares a purpose and
requirements. Those structures do not establish ownership, license,
maintenance, second-consumer, or external-demand evidence. **Primary local
records**, retrieved 2026-09-20.

**Implication.** A separate read-only inventory is the smallest correction; the
artifact registry should not be overloaded with unreviewed skill metadata.

### Claim 3: The correction needs a mechanical recurrence guard

**Evidence.** The new `skill-sharing-inventory.json` declares project and
user-local roots, and `scripts/skill_sharing.py` compares the exact discovered
skill set with inventory records. `tests/test_skill_sharing.py` proves an
unlisted skill fails validation and that recommendation cannot set publication
approval. **Repository primary implementation and tests**, retrieved
2026-09-20.

**Counterevidence.** Files outside declared roots remain invisible, and a local
directory scan cannot prove external use or legal ownership. **Known
limitation**, recorded 2026-09-20.

**Implication.** The guard prevents silent local omission but intentionally does
not promote a skill to public release.

## 5-Whys

1. **Why were used skills not recommended for sharing?** The factory had no
   skill recommendation inventory spanning the roots where skills were used.
2. **Why was there no inventory?** The shareability design modeled substantial
   repository artifacts, while skills were treated as project configuration or
   external tooling.
3. **Why did that distinction persist?** Skill usage was recorded in commands
   and prose evidence, not as a machine-readable candidate with source and
   disposition fields.
4. **Why was prose allowed to be the only bridge?** Existing tests checked
   frontmatter and trigger contracts, but no test reconciled discoverable skill
   files against a sharing recommendation surface.
5. **Why was that recurrence guard absent?** The factory's ecosystem gate
   focused on build-time reuse and publication safety, not completeness of
   skill discovery across local scopes.

**Root cause:** missing scope-aware, machine-readable skill inventory and
recommendation gate. **Immediate correction:** add the inventory and validator.
**Root correction:** require exact-set reconciliation for every declared skill
root. **Mechanical guard:** `tests/test_skill_sharing.py` fails on an unlisted
skill and on accidental publication approval.

## Conflicts And Unknowns

- “Not recommended” is confirmed as a missing recommendation record, not as a
  negative shareability decision.
- `macos-screenshot` has demonstrated local utility, but no evidence here
  proves an independent external consumer, ownership clearance, license
  compatibility, maintenance owner, or publication authorization.
- The inventory covers declared roots only; unregistered roots and skills used
  outside this workspace remain unknown. The project root is required; the
  user-local root is optional so CI can validate the project scope without
  pretending that a different runner has the owner's local skills.
- The project-local skills have explicit licenses and metadata; the user-local
  screenshot skill does not expose equivalent metadata in the inspected file.

## Decision Implications And What Would Change The Conclusion

- Recommend the six used skills for human shareability review; keep two
  discoverable but unused user-local skills deferred.
- Keep publication approval false for every record. Do not install, copy,
  publish, or mutate an external repository.
- Run `python3 scripts/skill_sharing.py` in the factory checks workflow; missing
  optional roots are skipped, while missing required roots fail closed.
- The recommendation would strengthen if a second independent consumer,
  immutable source identity, license/provenance review, maintenance owner, and
  privacy scan were recorded.
- It would weaken if usage evidence were shown to be stale, the skill source
  were private or incompatible, or the exact-set scan proved that the declared
  roots were incomplete.

## Sources

### Primary

- `.factory/artifacts/reuse-registry.json`, retrieved 2026-09-20.
- `.factory/governance.yaml`, retrieved 2026-09-20.
- `scripts/discover-reuse.py`, `scripts/ecosystem_gates.py`, and
  `tests/test_shareable_skill_contracts.py`, retrieved 2026-09-20.
- `.agents/skills/*/SKILL.md` and `/Users/hello/.agents/skills/*/SKILL.md`,
  retrieved 2026-09-20.
- `docs/research/continuous-competence-skill-opportunities-2026-09-20.md`,
  retrieved 2026-09-20.
- `.factory/artifacts/skill-sharing-inventory.json`,
  `scripts/skill_sharing.py`, and `tests/test_skill_sharing.py`, retrieved
  2026-09-20.

### Secondary

- `.factory/artifacts/evidence/shareable-components-deep-dive-2026-09-20.md`,
  retrieved 2026-09-20.

### Lead-only

- No lead-only source was used for a material claim.
