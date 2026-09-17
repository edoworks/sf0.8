# Safety Kernel PRD

## Purpose

Provide a small, inspectable control-plane reference that prevents an agent
from authorizing an external effect using model judgment, identity, or
delegation alone.

## v0 acceptance criteria

1. Missing, unknown, expired, revoked, mismatched, and out-of-scope
   capabilities are denied.
2. Human-only operations return `REQUIRE_HUMAN_AUTHORIZATION` and never allow.
3. Hard cost, runtime, and agent ceilings are enforced before accounting.
4. Audit-sink failure denies without consuming budget.
5. Every completed decision has structured, hash-chained evidence.
6. Delegation cannot increase operation, resource, duration, or limits.
7. Host sandboxing, real secret brokering, and remote immutable audit are
   explicitly not claimed by this prototype.

## Docker execution backend

Docker Business is an existing subscription and may be used without adding a
new paid service. Docker is an execution backend, not the policy engine. The
adapter must generate a fixed profile with disposable containers, a read-only
root filesystem, no network, dropped capabilities, `no-new-privileges`, a
non-root user, explicit CPU/memory/PID/storage/runtime limits, and only a
dedicated workspace mount. Agents must never receive the Docker socket or
control Docker arguments.

Docker Desktop on macOS introduces a Linux VM, but this prototype does not
claim protection from Docker Desktop, the daemon, the VM, the host OS,
hypervisor, kernel, or image supply-chain compromise. A missing or failing
Docker daemon denies execution. The subscription does not make containers
equivalent to Firecracker microVMs or provide immutable audit storage.

## Non-goals

No agent framework, learned policy, production credential integration,
deployment integration, or meaningful autonomous external action is included.
Docker image pulls, compute, storage, and maintenance remain operational
costs even when no new subscription is purchased.

## Owner effort target

Routine bounded local work should be pre-authorized. Human interaction is
reserved for envelope creation/change, consequential effects, ambiguity, and
failed safety evidence. Approval packets must be short and independently
verifiable.

## Evidence

`tests/test_safety_kernel.py` is the executable acceptance suite. Future
increments must add attacks before adding authority.

Docker smoke evidence (2026-09-14): Docker Desktop server `29.7.2` ran the
adapter with the already-local image
`node@sha256:e4bf2a82ad0a4037d28035ae71529873c069b13eb0455466ae0bc13363826e34`.
The process UID was `65532`; writes to `/etc` and `/workspace` were denied;
outbound TCP connectivity was denied. No image pull, credential, or external
write was used. This demonstrates the configured profile on this host only;
it does not demonstrate escape resistance or host independence.

Kernel integration evidence (2026-09-14): an authorized `run_command` request
was required to launch the same restricted backend; the container returned
`integrated-ok` and the audit recorded `container_completed=success`. A direct
call without a kernel or a non-`ALLOW` decision is rejected. The integration
does not make Docker or the host part of the trusted computing base disappear.
