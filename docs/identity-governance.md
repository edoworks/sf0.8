# Identity Governance

`.factory/identity-registry.json` is the canonical repository record for legal
identity, public brands, product names, trademark posture, domains, public
contacts, and address-handling policy. `.factory/portfolio.yaml` remains the
authority for product and surface lifecycle. A disagreement blocks validation;
the identity registry must not silently supersede the portfolio.

## Safety Rules

- Registry states are operational controls, not legal opinions. `FILED` means
  an application exists; it does not mean registered or cleared.
- `PROVISIONAL`, `CLEARANCE_REQUIRED`, and `LEGAL_REVIEW_REQUIRED` block name
  adoption. Domain ownership never supplies trademark clearance.
- No sunk cost creates authority: prior filing, registration, development,
  publication, or domain spend never justifies adoption or further spend.
- The repository may contain a registered-agent name, but no residential or
  private domicile value. `PRIVATE_DOMICILE` contains metadata pointing to an
  external secure record only.
- `REGISTERED` requires verified registration evidence. The current federal
  records are applications and make no registration claim.

## Spend Gates

Trademark filing, amendment, search, monitoring, or legal spend requires an
owner decision after the registry identifies the mark, owner, intended goods,
current evidence, and unresolved review. Domain registration, renewal,
transfer, purchase, sale, or publication likewise requires an owner decision
after classification and clearance review. Automation may report or block; it
may not transact.

Run `python3 scripts/validate-identity-registry.py`. The validator checks state
vocabularies, durable-ID uniqueness, owner support, registration claims,
adoption gates, private-address minimization, and referenced portfolio
lifecycles.
