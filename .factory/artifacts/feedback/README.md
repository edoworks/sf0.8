# Feedback Intake

This directory records community reports, upstream releases, and proposed
improvements to reviewed artifacts. A feedback record is evidence for
reevaluation, not permission to install, execute, publish, or submit a patch.

Each record should identify the artifact, source, observation date, requested
action, current status, and the reviewer decision. Accepted feedback must still
pass the reuse, provenance, license, security, and verification gates.

Use `validate_feedback_record` in `scripts/ecosystem_gates.py` for deterministic
shape checks. Keep `applied: false` or omit it until an authorized human-led
change is separately reviewed.
