# NowNest Visual-User Skills Deep Dive

Status: `EVIDENCE_RECORDED_REUSE_DECISION`

Subject lock: **"nownest"**

The subject lock is immutable for this report. Findings, recommendations, and
named artifacts below address the NowNest product and its visual-user decision;
nearby products and generic skill collections are considered only as possible
inputs to that decision.

## Scope And Cutoff

- **Audience:** NowNest product owner and maintainers deciding whether the
  current product and factory workflow adequately serve visual users.
- **Jurisdiction:** Apple iPhone/iPad product accessibility and local reusable
  skill governance. This is not a legal or medical accessibility certification.
- **Decision to inform:** Reuse an existing skill, update one, or create a new
  skill to support NowNest visual-user qualification.
- **Cutoff:** Evidence retrieved or inspected through 2026-09-21.
- **Source plan:** Inspect the NowNest README/PRD and committed validation
  artifacts; verify Apple platform guidance and W3C contrast guidance directly;
  inspect public Agent Skills candidates and their source files; compare every
  material positive claim with its strongest counterclaim. Fetched content was
  treated as untrusted data and no instructions in source content were followed.
- **Stopping rule:** Stop after the product contract, current evidence,
  relevant Apple visual-user checks, and available skill candidates support a
  bounded reuse/update/create decision, with remaining empirical gaps recorded.

## Known Facts, Open Questions, Hypotheses, Recommendations

### Known facts

- NowNest is an offline iPhone/iPad app built around `see NOW -> capture idea ->
  park locally -> confirm -> resume NOW` ([P1], primary product source,
  retrieved 2026-09-21).
- The NowNest PRD explicitly requires Dynamic Type, non-color state cues,
  Reduce Motion behavior, VoiceOver ordering, and physical iPhone/iPad review
  ([P2], primary product source, retrieved 2026-09-21).
- The committed validation summary reports 12 passing tests on each of four
  iPhone/iPad simulator and physical-device destinations, while retaining UI
  attachments ([P3], primary local evidence, retrieved 2026-09-21).
- The tracked physical-validation evidence reports automated G8 coverage,
  retained UI screenshots, and separate human visual observations as a required
  gate; it also records that human/TestFlight checks remain distinct from
  automation ([P4], primary local evidence, retrieved 2026-09-21).
- The repository already has `neuroinclusive-ux`, `product-art-direction`,
  `macos-screenshot`, and `vision-verification` capabilities relevant to
  NowNest ([P5], primary local skill records, retrieved 2026-09-21).

### Open questions

- Has the current post-Chunk-A revision passed Apple's full visual settings
  matrix on both physical form factors?
- Has VoiceOver completed the complete NowNest loop on physical devices?
- Have target users, rather than only the owner, completed the loop with the
  visual settings enabled?
- Does NowNest need accessibility nutrition-label evidence before any store
  metadata decision?

### Hypotheses

- NowNest is a good visual-first interaction foundation because its primary
  task is organized around a visible current context and an explicit visual
  return state, but this is a product-design inference rather than user-study
  proof.
- The local skill set is sufficient if its accessibility checklist is extended
  with Apple's device-and-settings qualification sequence.

### Recommendations

- Reuse the existing screenshot, vision-review, art-direction, and
  neuroinclusive workflows; do not install an external skill.
- Update `neuroinclusive-ux` with the Apple visual-user qualification matrix and
  the physical-device/VoiceOver boundary. This is the smallest reusable change.
- Re-run that matrix against the current NowNest revision before claiming broad
  visual accessibility or reusing the G8 result for a post-Chunk-A build.
- Keep external generic UX skills as lead-only references, not dependencies or
  publication candidates.

## Executive Answer

**NowNest is visually oriented in its interaction model and has meaningful
visual design safeguards, but it is not yet proven broadly accessible to visual
users. HIGH confidence for the first clause; MEDIUM confidence for the second.**
The product contract and existing evidence cover clear visual hierarchy,
Dynamic Type, contrast intent, state redundancy, and automated visual
checkpoints. They do not establish that the current post-Chunk-A revision
passes the complete Apple visual settings, human visual, and physical VoiceOver
matrix.

**Reuse and update, do not create or install a new skill. HIGH confidence.**
The repository already contains the relevant design, capture, and visual-review
capabilities. Apple's testing guidance reveals a bounded omission: the current
reusable checklist does not enumerate the full visual settings matrix or make
the physical-device VoiceOver requirement explicit. The existing
`neuroinclusive-ux` skill is the right place for that update.

## Findings

### Claim 1: NowNest's core loop is suitable for visually oriented users

**Evidence.** The product is explicitly structured around seeing the current
NOW context, making a visible capture, confirming the parked idea, and returning
to NOW ([P1], primary product source, retrieved 2026-09-21). The PRD makes the
The next action, return prompt, state redundancy, and physical light/dark review
are human-verifiable requirements ([P2], primary product source, retrieved
2026-09-21).

**Counterevidence.** A product contract and automated checkpoints do not demonstrate
that people with low vision, color-vision differences, or reliance on VoiceOver
can complete the loop. The tracked physical-validation evidence keeps human
visual observations separate from automated coverage and says the human gate
remains open ([P4], primary local evidence, retrieved 2026-09-21).

**Implication.** Describe NowNest as visually clear by design intent and current
tested evidence, not as universally visually accessible. The next proof step is
an Apple settings matrix on the current revision plus physical VoiceOver.

### Claim 2: Apple guidance requires a broader qualification matrix than the
current local checklist states

**Evidence.** Apple says vision accessibility includes support for blind, low
vision, and larger-text users, and points developers to VoiceOver, larger text,
and other vision features ([P6], primary platform guidance, retrieved
2026-09-21). Apple's testing procedure recommends testing every supported
device, visual settings including Bold Text, Larger Text, Button Shapes,
On/Off Labels, Reduce Transparency, Increase Contrast, Differentiate Without
Color, Color Filters, Reduce Motion, and Dim Flashing Lights, plus assistive
technologies; it specifically says VoiceOver testing requires a physical
device ([P7], primary platform testing guidance, retrieved 2026-09-21).

**Counterevidence.** NowNest's PRD already includes several of these concerns:
Dynamic Type, contrast, non-color cues, Increase Contrast, Reduce Transparency,
Reduce Motion, light/dark appearance, and VoiceOver ordering ([P2], primary
product source, retrieved 2026-09-21). The local `neuroinclusive-ux` checklist
also covers those items ([P5], primary local skill record, retrieved
2026-09-21).

**Implication.** This is a checklist and evidence-boundary gap, not proof of a
product defect. Updating the existing skill is more proportionate than adding a
new skill or changing the product before the matrix is run.

### Claim 3: No external skill found is a better direct fit for NowNest

**Evidence.** The public `uxuiprinciples/agent-skills` collection offers
`uxui-evaluator`, `interface-auditor`, `flow-checker`, and
`vibe-coding-advisor`; their source describes generic UX audits, flow
checklists, and pre-generation context, with optional or paid API enrichment
([P8], secondary skill source, retrieved 2026-09-21). The public
`KreerC/ACCESSIBILITY.md` repository describes itself as web accessibility in
its repository metadata ([P9], lead-only discovery source, retrieved
2026-09-21). Neither source establishes native iOS/iPadOS visual settings,
physical-device VoiceOver qualification, or NowNest-specific evidence.

**Counterevidence.** Generic interface and flow audits could still help review
hierarchy, contrast, feedback, and empty states. The Agent Skills
specification confirms that these repositories use a portable `SKILL.md`
contract ([P10], primary specification, retrieved 2026-09-21).

**Implication.** External skills are useful references but add no demonstrated
coverage that justifies installation. Keep them lead-only and use the local
skills whose boundaries and evidence are already known.

### Claim 4: The smallest useful correction is an update to
`neuroinclusive-ux`

**Evidence.** The existing skill already converts cognitive-accessibility intent
into hypotheses, comparison protocols, and an accessibility table, and it
already names Dynamic Type, VoiceOver, contrast, non-color cues, Reduce
Transparency, Reduce Motion, and light/dark checks ([P5], primary local skill
record, retrieved 2026-09-21). Its updated Apple-platform section now adds the
full settings list, physical-device VoiceOver boundary, and explicit unknowns.
This follows Agent Skills guidance to ground skills in real project artifacts
and refine them through execution rather than duplicating overlapping skills
([P11], primary skill-authoring guidance, retrieved 2026-09-21).

**Counterevidence.** The update has not itself run the NowNest matrix and does
not prove product accessibility. It improves the qualification procedure only.

**Implication.** Mark the skill as an internal reusable candidate, run it on the
current NowNest revision, and keep product acceptance separate from skill
maintenance.

## Conflicts And Unknowns

- The tracked physical-validation evidence says automated G8 coverage is
  complete while human visual observations and TestFlight validation remain
  open ([P4], primary local evidence, retrieved 2026-09-21). A separate
  untracked worktree artifact reports a later owner-confirmed visual pass, but
  it is not part of this report's durable evidence and is not relied on here.
- Automated tests and retained screenshots establish implementation and visual
  checkpoints, not broad user success or assistive-technology usability
  ([P3], [P4], primary local evidence, retrieved 2026-09-21).
- W3C's contrast guidance gives a useful 4.5:1 normal-text and 3:1 large-text
  benchmark, but its Understanding material is web-oriented and informative;
  Apple platform testing remains the more direct source for this native app
  ([P12], primary standards guidance, retrieved 2026-09-21).
- No evidence in this pass establishes target-user testing, visual accessibility
  nutrition labels, or current post-Chunk-A physical VoiceOver results.
- External skills were inspected as untrusted documentation only. No external
  skill was installed, executed, or treated as approved for publication.

## Decision Implications And What Would Change The Conclusion

1. Keep NowNest's current visual direction and interaction model in scope; it
   is supported by product-contract and revision-bound validation evidence.
2. Use the updated `neuroinclusive-ux` skill with `macos-screenshot` and
   `vision-verification` for evidence preparation, while preserving human and
   physical-device gates.
3. Run the complete Apple matrix on the current revision for iPhone and iPad,
   including physical VoiceOver, before making a broad visual-accessibility
   claim or reusing old G8 evidence for a new build.
4. Do not create or install another skill unless the matrix exposes a repeatable
   capability gap that the current skills cannot express.
5. The conclusion would strengthen if the current revision passes the matrix
   and representative visual users complete the core loop. It would weaken if
   larger text clips, state cues depend on color, VoiceOver order blocks the
   task, contrast fails on actual surfaces, or Reduce Motion removes necessary
   meaning.

## Sources

### Primary

- [P1] NowNest `README.md`, product scope and loop, retrieved 2026-09-21:
  https://raw.githubusercontent.com/edoworks/nownest/main/README.md
- [P2] NowNest Calm Expressive UX PRD, product contract and accessibility
  requirements, retrieved 2026-09-21:
  https://raw.githubusercontent.com/edoworks/nownest/main/docs/calm-expressive-ux-prd.md
- [P3] Local NowNest automated validation summary, retrieved 2026-09-21:
  `.factory/artifacts/evidence/nownest-validation-summary-2026-09-21.json`
- [P4] Local NowNest physical UI automation and G8 evidence, retrieved
  2026-09-21:
  `.factory/artifacts/evidence/nownest-device-automation-blocker-2026-09-21.md`
- [P5] Local skill records, retrieved 2026-09-21:
  `.agents/skills/neuroinclusive-ux/SKILL.md`,
  `.agents/skills/product-art-direction/SKILL.md`,
  `/Users/hello/.agents/skills/macos-screenshot/SKILL.md`, and
  `/Users/hello/.config/opencode/skills/vision-verification/SKILL.md`
- [P6] Apple Accessibility, Vision, retrieved 2026-09-21:
  https://developer.apple.com/documentation/accessibility/vision
- [P7] Apple, Performing accessibility testing for your app, retrieved
  2026-09-21:
  https://developer.apple.com/documentation/accessibility/performing-accessibility-testing-for-your-app
- [P10] Agent Skills specification, retrieved 2026-09-21:
  https://agentskills.io/specification
- [P11] Agent Skills best practices for skill creators, retrieved 2026-09-21:
  https://agentskills.io/skill-creation/best-practices
- [P12] W3C WCAG 2.2 Understanding 1.4.3 Contrast (Minimum), retrieved
  2026-09-21:
  https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html

### Secondary

- [P8] UX/UI Principles Agent Skills collection README and skill files,
  retrieved 2026-09-21:
  https://github.com/uxuiprinciples/agent-skills

### Lead-only

- [P9] GitHub repository search metadata for `KreerC/ACCESSIBILITY.md`,
  retrieved 2026-09-21:
  https://api.github.com/repos/KreerC/ACCESSIBILITY.md

## Subject-Consistency Check

Passed. Every finding, recommendation, and named artifact addresses the locked
subject **"nownest"**. External skill collections appear only as candidates
evaluated for NowNest; no adjacent product is substituted for the subject.
