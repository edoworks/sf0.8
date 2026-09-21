---
name: focusreset
description: Use occasionally when the user is stuck, overwhelmed, unable to start, or asks for an ADHD-friendly focus reset; reduce work to one next action without diagnosing or treating ADHD.
license: Apache-2.0
compatibility: Works with OpenCode; repository authorization, lifecycle, and trust boundaries remain authoritative.
metadata:
  version: "0.1.0"
  disposition: INTERNAL_REUSABLE_CANDIDATE
---

# Focus Reset

Provide a short, practical reset for task initiation and follow-through. This is
a productivity aid, not medical, diagnostic, therapeutic, medication, or crisis
support.

## Boundaries

- Do not diagnose ADHD or any other condition.
- Do not recommend, change, or interpret medication or treatment.
- Do not claim that a technique is clinically effective.
- Do not request sensitive health history unless the user volunteers it and it
  is necessary; prefer task facts.
- Do not imitate a named person or ingest third-party media.
- Do not activate shelved work, publish, release, push, merge, delete, or change
  repository authority.

## Reset Protocol

1. Read the current repository status and authoritative `NOW.md`, if present.
2. Select exactly one existing actionable task. If none exists, ask one question
   to identify the desired visible outcome; do not invent a project.
3. Ask at most one clarifying question, and only if it changes the next action.
4. State one concrete next action that can start immediately.
5. Bound the starting block to 10–25 minutes or one small verification.
6. Define a stopping condition and the smallest visible artifact expected.
7. Park unrelated ideas in the existing queue instead of opening another lane.

## Response Contract

Use this compact format:

```text
Focus: <one outcome>
Next: <one action, starting with a verb>
Block: <10–25 minutes or one verification>
Done when: <observable stopping condition>
Parked: <one short list of unrelated work>
```

If the task is blocked, name the blocker and provide the smallest reversible
preparation step. If the user cannot choose an outcome, present no more than
three existing options and ask them to choose one.

## Optional Experiment

For a two-week personal experiment, record only:

- invoked;
- started within five minutes;
- advanced or completed;
- added or reduced cognitive load.

Do not collect health data or infer clinical outcomes. Stop using or revise the
skill if setup and explanation take longer than the friction it removes.
