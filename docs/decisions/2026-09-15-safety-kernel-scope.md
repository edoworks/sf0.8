# ADR: Small Safety Kernel Scope

## Decision

Build a conventional, dependency-free authorization and accounting prototype
before adding an agent framework, broker integration, or production sandbox.

## Rationale

The factory has policy documents but no independently enforced capability
boundary. A small executable core makes the missing guarantees testable without
pretending that Python can provide host-level isolation or immutable storage.

## Rejected

- LLM-based authorization or review as a security boundary
- learned policy mutation
- broad credentials exposed to agents
- a large orchestration framework before representative attacks exist

## Consequence

The prototype is useful evidence, not a production control plane. Real sandbox,
credential, external audit, and platform-boundary work remains gated on attacks
against this core and explicit owner-set envelopes.
