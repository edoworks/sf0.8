# Threat Model

## Protected assets

- Human authority and approval decisions
- Credentials, private data, source history, and audit evidence
- Policy, capability, budget, sandbox, and shutdown controls
- Money, compute, network access, repositories, deployments, and published data

## Adversaries

Treat every agent as potentially erroneous, hallucinating, prompt-injected,
deceptive, reward-hacking, compromised, or malicious. Model malicious external
issues, pull requests, dependencies, documents, and network responses. Assume
all agents may collude, impersonate one another, manipulate evaluators or
metrics, extract secrets, create persistence, exhaust resources, or exploit the
factory.

## Unacceptable outcomes

- Unauthorized secret disclosure, external communication, spending, deployment,
  publication, deletion, or policy weakening
- Privilege escalation or authority amplification through delegation
- Escape from required isolation or bypass of shutdown
- Erasure, rewriting, or concealment of security-relevant history
- Resource use beyond a human-set hard ceiling
- Treating model agreement or self-certification as authorization

## Boundary and assumptions

The control plane, its host, operating system, hypervisor, hardware, and the
human owner's credentials are trusted only to the extent explicitly stated and
tested. This prototype does not defend against compromise of those components,
kernel-level escape, malicious filesystem administrators, denial of service by
the host, or a compromised human owner. A Python append-only file is
tamper-evident in this prototype, not immutable against a privileged host.

## Security questions

For each claimed guarantee: what technically prevents a coalition of every AI
agent from violating it? If the answer is a prompt, model behavior, convention,
or another agent, the guarantee is rejected.
