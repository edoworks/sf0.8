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

Federal trademark filing should normally occur only after the product:

1. survives Customer Zero;
2. has credible commercialization intent;
3. has a public name intended to persist;
4. completes clearance;
5. has accurately defined goods/services;
6. has the correct owner determined;
7. has appropriate address/domicile handling determined; and
8. receives explicit human spending approval.

A strategic studio identity such as EDOWORKS may qualify earlier, but it still
requires clearance and explicit human approval. Filing, amendment, search,
monitoring, or legal spend never follows automatically from a domain or prior
investment. Domain registration, renewal, transfer, purchase, sale, redirect,
or publication likewise requires a human decision after classification and
review. Automation may report or block; it may not transact.

## No Product Distortion

Existing trademark filings must not dictate product functionality. The factory
must not build a mobile operating system to fit the FOCULOOM application, add
desktop-publishing behavior to Veilsort to fit its application, manufacture
token use, fabricate specimens or statements of use, or rewrite product
descriptions to hide a mismatch. Trademark records follow commercial reality;
products solve supported user problems.

No product needs a dedicated domain while `INTERNAL`, `PROVISIONAL`, or
`CUSTOMER_ZERO`. A `COMMERCIALIZATION_CANDIDATE` may evaluate domains, and an
`ADOPTED` product may receive a canonical domain. The factory never purchases,
cancels, transfers, or redirects a domain.

Run `python3 scripts/validate-identity-registry.py`. The validator checks state
vocabularies, durable-ID uniqueness, owner support, registration claims,
adoption gates, private-address minimization, and referenced portfolio
lifecycles.
