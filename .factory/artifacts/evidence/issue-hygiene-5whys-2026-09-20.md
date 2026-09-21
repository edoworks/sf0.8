# Issue Hygiene 5-Whys

Date: 2026-09-20
Tracking: no new GitHub issue created; existing issue #80 was evaluated and found adjacent, not duplicate.

## Defect

New GitHub issues could be created without labels, an explicit classification,
priority, duplicate review, or reprioritization review.

## Evidence-Based Analysis

1. Why could an issue lack hygiene metadata? The writer only transported a body
   and had no required label or triage fields in the intent schema.
2. Why did the schema omit those fields? The original contract focused on body
   completeness and transport integrity, not portfolio-level issue triage.
3. Why was triage left outside the creation boundary? Duplicate detection and
   reprioritization were treated as conversational judgment rather than frozen
   planning evidence.
4. Why could conversational judgment be lost? There was no required artifact
   field, validator failure, or remote label readback for it.
5. Root cause supported by evidence: issue creation had a transport-integrity
   contract but no machine-enforced issue-hygiene contract.

## Corrections

- Immediate correction: do not create a new issue from an intent lacking labels,
  matching classification, P0-P3 priority, and explicit duplicate and
  reprioritization review.
- Root-cause correction: extend the planner-owned immutable intent and body
  sections; require the writer to pass labels verbatim and verify them remotely.
- Mechanical recurrence guard: `issue-intent.mjs` rejects missing or invalid
  metadata, and its tests cover missing triage and label/classification drift.

## Verification

- Issue-intent suite: run `node --test /Users/hello/.config/opencode/scripts/issue-intent.test.mjs`.
- Existing issue audit: live inventory and label taxonomy retrieved 2026-09-20.
- Existing issue #80 evaluated for duplicate/reprioritization reuse before any
  new issue mutation.
