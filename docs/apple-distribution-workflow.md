# Apple Distribution Workflow

The authoritative capability matrix is `.factory/apple-distribution/capabilities.json`.
Run `python3 scripts/validate-apple-distribution.py --list` to inspect it, or
`--can ios` for one capability. Human-readable discovery is generated at
`docs/apple-distribution-capabilities.md`.

## Product preflight

Product manifests under `.factory/apple-distribution/products/` reference
canonical product evidence and contain only the distribution facts needed by the
factory. Generate a reviewer-mode report with:

```text
python3 scripts/validate-apple-distribution.py --product product-a --write-report
```

Reports distinguish software, distribution, internal TestFlight, external
TestFlight, and App Review readiness. Findings are not Apple decisions.

The reviewer has three layers: structural validity, semantic product truth, and
adversarial reviewer quality. Public identity is independent from technical
bundle identity. An unresolved internal codename, placeholder, or unauthorized
public name blocks `APP_REVIEW_READY`.

## Draft preparation

The factory can emit a local App Store Connect preparation draft:

```text
python3 scripts/validate-apple-distribution.py --product product-a --write-report --write-draft
```

The draft is a checked-in-safe preparation artifact. It contains no credentials,
does not call App Store Connect, and cannot submit, publish, or release. Xcode,
Transporter, and App Store Connect API adapters may consume this contract only
inside a separately authorized release operation.

## Authority boundary

`APP_REVIEW_READY` means required fields exist, structural validation passes,
metadata is semantically coherent and product-true, no known placeholder or
internal material remains, identity and discoverability are resolved, and no
known blocking preflight finding remains. It never means Apple will approve the
app. The transition from `APP_REVIEW_READY` to `SUBMITTED` requires human
authority and is not implemented by this factory increment.
