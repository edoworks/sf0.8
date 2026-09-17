# Public Surface Remediation

Reviewed: 2026-09-15

## Local source changes

- The Edoworks portfolio Rung card now displays a named `Rung` mark instead of
  a lone placeholder initial.
- The Edoworks Rung project page now links its footer contact path to the
  existing Foculoom contact form.
- The local Foculoom homepage source already routes visitors to the Edoworks
  portfolio rather than the deprecated `rung.edoworks.com` hostname.
- The repository preflight now recognizes modern PyPI license metadata such as
  `License-Expression` and `license_files`; the published Rung package exposes
  `MIT` and `LICENSE` through those fields.

These changes are local source changes only. They are not represented as live
publication until the accountable owner reviews and publishes the relevant
website repositories.

## Remaining owner action

The live Foculoom homepage still links `https://rung.edoworks.com/`, which
returned HTTP 530 during review. Replace that link with
`https://edoworks.com/rung/` or restore a 301 redirect before publication.

The live Rung evidence preview renders its readiness assessment into an empty
`#quiz` element and says, “Enable JavaScript to use the readiness assessment.”
Its source is not present in this checkout, so a non-JavaScript equivalent
requires an owner-controlled change to that externally hosted surface.
