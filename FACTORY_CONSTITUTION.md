# Factory Constitution

Status: proposal for the safety-kernel increment (Issue #12). This document
is human-owned policy, not an agent instruction file.

## Invariants

1. The human owner is the final authority. Agents may propose policy or
   capability changes, but cannot authorize or apply them.
2. Every security-relevant request resolves to exactly `ALLOW`, `DENY`, or
   `REQUIRE_HUMAN_AUTHORIZATION`. Unknown operations, missing evidence,
   evaluator errors, and ambiguous policy resolve to `DENY`.
3. Agents have zero ambient authority. Effects are mediated by conventional
   control-plane code outside the agent process.
4. Capabilities are narrow, scoped, expiring where practical, revocable, and
   auditable. Delegation cannot increase authority.
5. Secrets are not supplied to agents when a mediated operation is possible.
6. Generated code and untrusted input execute in disposable isolation with
   explicit resource and network limits.
7. Policy, capability, credential, budget, audit, sandbox, and shutdown
   mechanisms cannot be changed by agents.
8. External effects are recorded with the principal, operation, arguments,
   capability, policy, decision, time, effect, and resource use.
9. Reversible operations are preferred. Publication, deployment, spending,
   visibility changes, credential access, and permanent deletion require a
   matching owner authorization or remain denied.
10. Increasing autonomy is never a terminal objective. Safety and human
    authority outrank velocity and convenience.

## Owner bottleneck rule

The owner pre-authorizes bounded, reversible routine work in written envelopes.
The system should ask for a human only when an envelope is absent or exceeded,
an operation is consequential, or the evidence is ambiguous. It must never
turn an absent human into implicit approval.

## Claim discipline

`FACT` means directly evidenced. `INFERENCE` means an engineering conclusion.
`HYPOTHESIS` requires testing. `PROPOSAL` means a design choice. Passing this
prototype does not establish production isolation or factory safety.
