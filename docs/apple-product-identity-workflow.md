# Apple Product Identity Workflow

Apple distribution has two identities: technical identity (repository, bundle
identifier, scheme, and archive) and public identity (name, purpose, seller,
store metadata, and customer-facing destinations). They must not be conflated.

The public identity workflow is:

`Customer Zero -> product purpose -> naming territory -> candidates -> genericity review -> App Store/collision research -> trademark-risk research -> domain/public-destination research -> candidate evidence -> human selection -> authorized identity -> propagation`

The factory performs deterministic checks and gathers evidence. It does not
choose a brand, determine trademark rights, conclude App Store availability, or
publish a public identity. Those decisions remain human-authorized.

`APP_REVIEW_READY` requires an authorized public identity and a completed
semantic/reviewer audit. A technically valid bundle identifier or archive does
not satisfy that requirement.
