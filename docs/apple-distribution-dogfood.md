# Apple Distribution Dogfood

Generated reports:

- [Product A report](../.factory/artifacts/reports/apple-distribution/product-a.json)
- [Product A submission draft](../.factory/artifacts/reports/apple-distribution/product-a-submission-draft.json)
- [Vorynce report](../.factory/artifacts/reports/apple-distribution/vorynce.json)
- [Vorynce submission draft](../.factory/artifacts/reports/apple-distribution/vorynce-submission-draft.json)

## Current Results

| Product | Platform/type | Factory state | Distribution | Internal TestFlight | External TestFlight | App Review | Human authority |
|---|---|---|---|---|---|---|---|
| Product A | iOS/iPadOS local microphone pet experiment | PARTIAL | Archive present | BLOCKED | BLOCKED | BLOCKED: public identity unresolved, metadata, age rating, screenshots, review information, accessibility, export | Not authorized |
| Vorynce | iOS on-device voice organization | PARTIAL | BLOCKED: no exact archive | BLOCKED | BLOCKED | BLOCKED: discoverability review, metadata, age rating, screenshots, review information, accessibility, export, IAP | Not authorized |

The canonical portfolio currently supplies no additional active or released
Apple product with a factory-reproducible distribution record. Historical manual
distribution, if discovered later, will remain evidence of that product only;
it will not upgrade a factory capability to `SUPPORTED_VERIFIED`.

The reports deliberately do not predict Apple’s decision. They identify what
would prevent a reviewer from completing review today and link every blocker to
the owning factory issue.

## Identity dogfood

Product A is treated as an internal codename. Canonical product evidence names
the product direction `Mews & Woofs`, but no authorized public identity is
recorded. The reviewer therefore blocks readiness rather than renaming it.

Vorynce has a distinctive canonical identity, but its discoverability review is
not evidenced. That is a reviewer-layer blocker, not a claim that the name is
invalid.
