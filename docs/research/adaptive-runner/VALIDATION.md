# Adaptive Runner Research Package Validation

Date: `2026-09-23`

Scope: research decision package only

## Structural Checks

- All Markdown files rendered successfully with Pandoc using GitHub-flavored
  Markdown input.
- `phase-gate.schema.json` parsed successfully as JSON.
- Schema fixtures accept reviewed `PREREGISTRATION` and completed `RESULT`
  records, while a `STOP` result that authorizes the next phase is rejected.
- Local Markdown links resolve to files in this package or the repository.
- Targeted terminology checks found no stale `RunPlanDraft`, `PlayerProfile`, or
  obsolete E0 percentage-rule language; references to raw events state their
  prohibition or active-run-only lifetime.

## Visual Review

The package index was rendered in Safari at desktop and phone-width window
sizes. Direct inspection found:

- readable title, headings, body text, code labels, links, and tables;
- no text clipping, overlap, or page-level horizontal overflow;
- coherent hierarchy and sufficient light-on-dark contrast;
- responsive wrapping at phone width; and
- table containment at desktop width.

Local vision review used `ollama/qwen3.5:4b`. It passed document loading, layout,
responsiveness, hierarchy, contrast, and readability. It reported a possible
phone-width heading overlap; direct inspection of the capture showed the
heading and rule were separated and aligned, so this finding was reclassified
as a model false positive.

The visual review validates documentation rendering only. It does not validate
factual accuracy or cross-file contracts, provide player evidence, or authorize
product implementation beyond E0.

## Playwright Capture Gap: 5 Whys

1. The planned Playwright mobile capture did not run because its WebKit and
   Chromium executables were absent.
2. The executables were absent because the installed Playwright package did
   not have a matching browser payload in the local cache.
3. The validation plan assumed CLI availability implied browser availability;
   that assumption was not checked before capture.
4. Installing browsers during closeout would introduce an unnecessary download
   and mutate the validation environment, so Safari was used instead.

Root cause: the capture-backend preflight checked the command only, not its
browser payload.

Immediate correction: capture both viewports from the already-installed Safari
browser with the macOS screenshot workflow.

Recurrence guard: future visual-validation plans must confirm the selected
browser executable or payload before capture and name an installed-browser
fallback. This run exercised the fallback successfully.
