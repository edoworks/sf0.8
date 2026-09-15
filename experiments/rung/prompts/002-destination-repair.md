# Rung Destination Repair Prompt

Apply the shared publication contract. Use PUBLIC mode only after independently checking every destination.

Update Rung without changing the assessment questions, scoring thresholds, disclaimers, or client-side privacy behavior.

Configure only these verified HTTPS destinations:

Documentation: [URL]
Installation: [URL]
Source code: https://github.com/edoworks/rung
Audit request: [URL]
Contact: [URL]

The following canonical Rung destinations are independently verified:

- Repository: https://github.com/edoworks/rung
- Release v0.3.2: https://github.com/edoworks/rung/releases/tag/v0.3.2
- PyPI package v0.3.2: https://pypi.org/project/rung-audit/0.3.2/
- Website: https://edoworks.com/rung/

Requirements:

- No placeholder token may remain in PUBLIC output.
- The source link must reach the canonical public repository.
- Documentation and installation links must be usable.
- The audit and contact CTAs must reach monitored destinations, or be removed and labeled unavailable.
- Describe the assessment result as an informational self-assessment only.
- Do not imply certification, compliance validation, legal advice, or security assurance.
- Do not present paid audits as an operating service unless the owner has verified the request path and monitoring.
- Preserve the statement that no analytics service is connected unless that changes through an approved privacy review.

Analytics for this version:

- Do not send outbound analytics requests.
- Keep only local event hooks for assessment_started, assessment_completed, audit_cta_clicked, and docs_clicked.
- Do not include answers, results, free text, identifiers, or payment data in event payloads.

Acceptance checks:

- Fetch the published HTML and verify no [RUNG_*_URL] token remains.
- Test every visible external destination independently.
- Complete all assessment paths on mobile and desktop.
