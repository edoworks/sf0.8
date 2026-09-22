---
name: neuroinclusive-ux
description: Convert a product interaction loop into cognitive-accessibility hypotheses, task-based prototypes, moderated test scripts, and behavioral metrics for users who experience distractibility, task-switching cost, or cognitive overload. Use when designing, prototyping, or testing UX for neurodivergent audiences or calm-productivity tools.
license: Apache-2.0
compatibility: Local, advisory; never impersonate participants, fabricate observations, or claim clinical effectiveness.
metadata:
  version: "0.1.0"
  disposition: INTERNAL_REUSABLE_CANDIDATE
---

# Neuroinclusive UX

Turn cognitive-accessibility intent into testable hypotheses, bounded
prototypes, and evidence-based decisions without claiming medical benefit or
fabricating participant data.

## When to use

- A product targets users who experience distractibility, task-switching cost,
  or cognitive overload.
- A team needs a calm-productivity design reviewed against accessibility
  guidance.
- A prototype needs a comparison protocol before selecting a production
  treatment.
- A mascot, animation, or gamification element is proposed and needs
  guardrails.

## Primary guidance

- [W3C Making Content Usable for People with Cognitive and Learning Disabilities](https://www.w3.org/TR/coga-usable/)
- [W3C Understanding Success Criterion 2.3.3: Animation from Interactions](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html)
- [Apple Accessibility: Cognitive](https://developer.apple.com/documentation/accessibility/cognitive)

These are standards and platform guidance, not clinical proof. Cite them for
design rationale, not treatment claims.

## Design principles

1. **Calm expressiveness over continuous stimulation.** Identity at meaningful
   transitions, then return to visual rest.
2. **One dominant action.** The next step must be unmistakable.
3. **Short critical paths.** Minimize choices and screens.
4. **Recognizable feedback.** Capture, success, and error must be immediately
   clear.
5. **User-controlled interruption.** No random notifications, streaks, or
   pet demands.
6. **Motion carries meaning.** No decorative loops; respect Reduce Motion with
   immediate state replacements.
7. **No color-only state.** Combine color with text, icon, or shape.
8. **No infantilization.** Warm and concise voice; never needy, scolding,
   guilt-inducing, or diagnostic.

## Anti-patterns

- Dashboards, feeds, counters, streaks, points, currencies, collectibles,
  levels, or routine confetti.
- Random interruptions, punishment mechanics, or virtual-pet obligation.
- Busy pages, changing content, or unnecessary imagery that causes overload.
- Claiming ADHD diagnosis, treatment, or clinical benefit.

## Comparison protocol

When comparing treatments, use this structure:

1. **Fix the interaction model.** Do not change the core loop between variants.
2. **Seed identical content.** Use the same fixture for every variant.
3. **Counterbalance order.** Rotate variant order across participants.
4. **Run the same tasks.** Identify, capture, resume, recover from distraction,
   review.
5. **Record per variant.** Completion, errors, capture-to-resume time, recall,
   perceived effort (1-5), satisfaction (1-5), distraction (1-5), qualitative
   response, and observed defects.
6. **Apply rejection rules before selection rules.** Reject on regression,
   distraction, or infantilization before considering satisfaction.
7. **Report raw observations and uncertainty.** Do not infer statistical
   significance from small samples.
8. **Record the decision with authority.** Name the operator, evidence
   location, limitations, dissent, and owner approval.

## Participant and consent rules

- Use adult participants from the target audience.
- At least some should self-identify as regularly experiencing distractibility
  or task-switching cost; do not require or record a diagnosis.
- Obtain consent, minimize notes, and record no unnecessary personal or health
  information.
- If the minimum sample is unmet, record as formative dogfooding and do not
  change the production default.

## Accessibility checklist

Produce a mode-by-mode table with device, variant, pass/fail, evidence path:

| Check | Pass condition |
| --- | --- |
| Dynamic Type | Content visible, readable, reachable at accessibility sizes |
| VoiceOver order | Task content before decorative identity |
| Text contrast | 4.5:1 normal, 3:1 large text |
| Non-text contrast | 3:1 for essential controls and boundaries |
| Differentiate Without Color | State retains text/icon/shape cues |
| Increase Contrast | Hierarchy intact, content readable |
| Reduce Transparency | No lost boundaries or text |
| Reduce Motion | No movement; immediate state replacement |
| Light/dark appearance | No clipping, illegible pairings, or lost boundaries |

## Visual-user qualification for Apple platforms

For an iPhone or iPad product whose acceptance criterion includes visual-user
support, qualify the main tasks on every supported form factor. Test each
setting separately, then record the device, OS, setting, task result, and
evidence path:

- Bold Text
- Larger Text, including the largest supported accessibility sizes
- Button Shapes
- On/Off Labels
- Reduce Transparency
- Increase Contrast
- Differentiate Without Color
- Color Filters, including at least one red/green filter
- Reduce Motion
- Dim Flashing Lights when motion or flashing content exists

Test VoiceOver on physical devices, not only simulators. Confirm that task
content precedes decorative identity, the primary action has a clear accessible
label, and the complete capture-to-resume loop can be completed. Retained
screenshots can support visual review, but screenshots and unit/UI tests do not
prove assistive-technology usability or real-user success.

Use Apple's visual-accessibility and accessibility-testing guidance as the
platform source of truth:

- [Apple Accessibility: Vision](https://developer.apple.com/documentation/accessibility/vision)
- [Apple: Performing accessibility testing for your app](https://developer.apple.com/documentation/accessibility/performing-accessibility-testing-for-your-app)

Do not call a product visually accessible because one appearance, one device,
or one owner review passed. Record unsupported settings and remaining physical
device or participant evidence as unknowns.

## Skill boundaries

- This skill produces hypotheses, prototypes, scripts, metrics, and
  evidence summaries. It does not produce clinical proof.
- An implementation agent may prepare builds and blank records but may not
  recruit, impersonate, consent, or sign decisions.
- Physical-device deployment and any upload or publication remain separately
  human-authorized.
