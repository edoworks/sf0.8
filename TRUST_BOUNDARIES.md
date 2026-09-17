# Trust Boundaries

```text
HUMAN OWNER
    |
    v
TRUSTED CONTROL PLANE
  policy + capability + budget + audit gateway
    |
    v
UNTRUSTED AGENT PROCESS
    |
    v
DISPOSABLE EXECUTION SANDBOX / MEDIATED EFFECTS
```

The prototype trusts only small, conventional policy and accounting code plus
its configured audit sink. Agents do not receive direct shell, filesystem,
network, GitHub, credential, deployment, spending, or policy mutation access.

The prototype demonstrates request authorization and accounting. It does not
yet provide a host-enforced sandbox, real credential broker, or immutable
remote audit store. Those are explicit follow-up boundaries, not implied by
the Python API.

## Docker boundary

When enabled, Docker is a bounded execution backend below the untrusted agent
plane. The control plane owns the Docker invocation and supplies a fixed
profile. The agent receives no Docker socket, host mount, credential, or
external-write capability. Docker daemon, Docker Desktop, its Linux VM, image
registry, host OS, kernel, and hypervisor remain trusted dependencies outside
the demonstrated Python guarantee.
