---
name: prose-editing
description: Edit prose for a specific audience and purpose by preserving supported meaning, removing filler, improving clarity, and matching the supplied voice. Use for humanizing, tightening, simplifying, or making writing no-fluff without fabricating claims or personal experience.
license: MIT
compatibility: Requires the source text or a clearly identified file; no external style imitation is needed.
metadata:
  version: "0.1.0"
  disposition: INTERNAL_REUSABLE_CANDIDATE
---

# Prose Editing

Improve the writing without changing what the evidence supports.

## Workflow

1. Identify audience, purpose, format, and desired level of directness.
2. Read the complete text before editing.
3. Preserve facts, numbers, dates, citations, uncertainty, attribution, and
   meaningful voice.
4. Remove repetition, filler, inflated claims, generic staging, forced
   contrasts, mechanical triads, unnecessary headings, and vague conclusions.
5. Prefer concrete verbs and specific nouns. Vary sentence length naturally.
6. Check the result against the source for dropped or invented claims.

## Humanize mode

Make the text sound like its author, not like a generic assistant. If a writing
sample is supplied, use it as the authority for cadence, vocabulary, and
punctuation. Without a sample, choose a plain voice appropriate to the genre.
Do not impersonate a real person, conceal material authorship, or claim lived
experience the source does not establish.
Do not invent personal experience.

## No-fluff mode

Lead with the answer, remove throat-clearing, keep necessary caveats, and use
specific next steps. Concision must not remove safety information, limitations,
citations, or uncertainty.

## Output

- For pasted text, return the edited text and a short change summary.
- For a file, change prose only unless the user explicitly authorizes structure
  or code edits; preserve code, commands, paths, data, and link targets.
- For factual or legal text, do not add unsupported details while polishing.
