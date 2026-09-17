# Capability Model

A capability is a signed or otherwise unforgeable control-plane record in the
production design. The prototype uses an in-process immutable value and is not
itself a cryptographic credential system.

Each grant contains a principal, one operation, one resource scope, expiry,
optional limits, and a revocation identifier. Authority is never inferred from
agent identity, prompt text, role names, or model output.

Resource matching is exact or boundary-safe descendant matching; string
prefixes such as `/repo/a` must not authorize `/repo/attacker`.

Delegation may issue a child capability only with a subset of the parent's
operation, resource, time, and resource limits. It may not create authority.

Human-only operations include secret access, policy changes, publication,
deployment, repository visibility changes, permanent deletion, and spending
outside an active envelope.
