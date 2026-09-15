# Public Surface Review Contract

## Review record

```text
surface:
url:
surface_type:
reviewed_at:
commit_or_version:
intended_audience:
intended_action:
canonical_source:
canonical_url:
personas_run:
deterministic_checks:
decision:
```

## Finding record

```text
severity: P0 | P1 | P2 | P3
persona:
url_or_path:
quoted_text_or_selector:
problem:
evidence:
audience_consequence:
minimal_recommended_change:
confidence: high | medium | low
follow_up_issue:
```

## Scoring

Score each dimension from 0 to 4:

| Dimension | 0 | 4 |
|---|---|---|
| Audience usefulness | Unclear value | Immediate, concrete value |
| Human voice | Generic or synthetic | Specific and accountable |
| Actionability | Dead end | Clear useful next step |
| Evidence | Unsupported | Current, corroborated evidence |
| Lifecycle consistency | Contradictory | All surfaces agree |
| Accessibility | Blocking barriers | Tested and usable |
| Trust and privacy | Misleading or absent | Clear and proportionate |

## Blocking rules

A surface is blocked by any of the following:

- Material unsupported or contradicted claim.
- Broken canonical or primary CTA.
- Placeholder destination in a public surface.
- Privacy statement inconsistent with observed behavior.
- Product, payment, audit, or beta availability overstated.
- Fork, ownership, or lifecycle ambiguity with material audience impact.
- Known accessibility blocker in the primary journey.

An average score cannot override a blocking finding.

## Required deterministic preflight

Run mechanical checks before language review:

- HTTP status, TLS, and redirects.
- Placeholder-token scan.
- Canonical and sitemap consistency.
- External link status.
- Repository visibility, fork, license, and release metadata.
- Package and version availability.
- Presence of privacy and contact paths where data or consequential actions exist.

Deterministic checks outrank model judgment for observable facts.

The repository preflight can run without secrets:

```sh
python3 scripts/public-surface-preflight.py URL [URL ...] --json
```

Use `--skip-links` when only page status, placeholders, and canonical metadata
are being checked. Keep live link checks outside mandatory CI when destinations
are controlled by third parties; attach their output to the review evidence.
Use `--require-text` and `--forbid-text` for lifecycle assertions, and
`--github-repo OWNER/REPO` for public visibility, fork, archive, and license
metadata checks, `--github-release OWNER/REPO TAG` for stable release metadata,
and `--pypi-package NAME` for package version and license metadata.

## Review verdicts

- `pass`: no blockers; audience and evidence scores meet threshold.
- `pass-with-follow-up`: no blocker; non-critical improvements recorded.
- `blocked`: at least one blocker; publication or promotion must wait.
- `unobservable`: evidence is insufficient; do not interpret as pass.

## Human approval

The accountable owner approves material copy, privacy, payment, legal, lifecycle,
and publication decisions. A reviewer can recommend a rewrite but cannot silently
change a claim or publish a surface.
