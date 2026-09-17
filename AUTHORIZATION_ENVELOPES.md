# Authorization Envelopes

An envelope is a human-authored ceiling, not an agent recommendation. Values
are inactive until the owner supplies them and the control plane verifies them.

## Initial routine envelope

The prototype may authorize only explicitly granted, reversible operations on a
named task resource. Suggested future defaults are read-only inspection,
branch-local edits, deterministic tests, and bounded local commits. No network,
secret, publication, deployment, deletion, policy mutation, or external spend
is included by default.

## Required ceilings

Before enabling external work, the owner must set hard limits for task/day/month
spend, model tokens, CPU time, memory, storage, network transfer, agent count,
execution time, and delegation depth. Until then, those dimensions deny.

## Human authorization

Authorization is required for envelope changes, control-plane changes, secrets,
external communication, publication, deployment, destructive operations,
visibility changes, and exceeding any ceiling. Approval must identify the
operation, resource, duration, limits, reversibility, and evidence required.
