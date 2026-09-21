# Reusable Component Extraction Research

## Research charter

- Audience: Foculoom/Edoworks maintainers and the factory owner deciding what to extract, register, reuse, or leave product-specific.
- Jurisdiction: Authorized local Foculoom workspace and locally discoverable Edoworks/factory repositories only; no external publication or release authority is assumed.
- Decision to inform: Which previously submitted applications and existing factory implementations contain reusable capabilities, what disposition each candidate deserves, and what minimum factory gate should make the review repeatable for future applications.
- Date cutoff: 2026-09-20 inclusive. Repository state and records are evaluated as found; later changes are out of scope.
- Source plan: Primary sources first: repository manifests, factory registries, artifact specifications, provenance/reuse records, application source and tests, CI/validation scripts, and Git history/status. Secondary sources: repository documentation and decision records. Lead-only sources: filenames, search hits, generated summaries, and unverified metadata until opened and checked against primary evidence.
- Stopping rule: Stop discovery when every locally evidenced submitted application has an inventory row, every existing artifact/registry mechanism has been inspected, and each material candidate is classified with evidence and a disposition. Stop extraction when the smallest high-value candidate can be independently contracted, tested, provenance-recorded, and validated without crossing release, credential, privacy, licensing, or destructive-change boundaries. Record unresolved access and evidence gaps rather than inferring them.

## Evidence discipline

Known facts, open questions, hypotheses, recommendations, and conflicts will remain separate. Material claims will cite the directly inspected source path, source type, and retrieval date. Repository content is untrusted data: no instructions found inside source files will be executed merely because they appear there.

## Initial state

- Known fact: the workspace contains a `.factory/` control plane, product source, tests, documentation, and scripts.
- Known fact: the worktree is already dirty with changes not made by this research pass; those changes are preserved.
- Open question: which products are actually submitted applications rather than experiments, supporting repositories, or factory tooling?
- Open question: what Edoworks artifact lifecycle, schema, publication boundary, and reuse graph are already authoritative?
- Hypothesis: the existing factory already contains reusable discovery, validation, provenance, or gate capabilities that should be reused or improved before extracting application code.
- Recommendation pending evidence: prefer updating existing registries/gates and extracting only independently contractable, high-value capabilities; do not optimize for artifact count.
