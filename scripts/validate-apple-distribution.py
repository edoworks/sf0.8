#!/usr/bin/env python3
"""Validate Apple distribution capabilities and run a non-submitting review preflight."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0, str(ROOT / "scripts"))
from evidence_strength import evidence_levels as normalized_evidence_levels


REGISTRY = ROOT / ".factory/apple-distribution/capabilities.json"
PRODUCTS = ROOT / ".factory/apple-distribution/products"
REPORTS = ROOT / ".factory/artifacts/reports/apple-distribution"
STATES = {"SUPPORTED_VERIFIED", "SUPPORTED_UNVERIFIED", "PARTIAL", "UNSUPPORTED", "NOT_APPLICABLE"}
STAGES = {"build", "validate", "package", "internal_testflight", "external_testflight", "app_review"}
FINDING_TYPES = {"BLOCKER", "LIKELY_REVIEW_CONCERN", "METADATA_DEFECT", "EVIDENCE_GAP", "NON_BLOCKING_IMPROVEMENT", "NOT_APPLICABLE"}
FINDING_CLASSIFICATIONS = {"PASS", "WARNING", "BLOCKER", "REQUIRES_HUMAN_JUDGMENT"}
PLACEHOLDER_RE = re.compile(r"\b(?:product\s*[a-z]|test\s*app|demo|example|sample|untitled|new\s*app|app\s*\d+|prototype|todo|tbd|internal|dev|staging)\b", re.IGNORECASE)
PLACEHOLDER_COPY_RE = re.compile(r"\b(?:lorem ipsum|replace me|coming soon|your description here|todo|tbd|example text)\b", re.IGNORECASE)
TECHNICAL_NAME_RE = re.compile(r"(?:product[_ -]?a|product[_ -]?b|app[_ -]?\d+|internal|staging|dev(?:elopment)?)", re.IGNORECASE)
MODES = {"PREFLIGHT", "PREPARE", "VALIDATE", "DELIVER", "SUBMIT", "RELEASE"}


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_products() -> list[dict[str, str]]:
    spec = importlib.util.spec_from_file_location("resolve_portfolio", ROOT / "scripts/resolve-portfolio.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("canonical portfolio resolver is unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.enumerate_apple_products()


def validate_product_inventory(products: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    canonical = {product["id"]: product for product in canonical_products() if product.get("lifecycle") in {"active", "released"}}
    manifests = {product.get("id") for product in products}
    missing = sorted(set(canonical) - manifests)
    unknown = sorted(manifests - set(canonical))
    if missing:
        errors.append(f"distribution manifests missing canonical Apple products: {', '.join(missing)}")
    if unknown:
        errors.append(f"distribution manifests contain non-canonical Apple products: {', '.join(str(item) for item in unknown)}")
    for product in products:
        expected = canonical.get(product.get("id"))
        if expected and product.get("platform") != expected.get("platform"):
            errors.append(f"{product.get('id')}: platform disagrees with canonical portfolio")
    return errors


def validate_registry(registry: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if registry.get("schema_version") != 1:
        errors.append("registry schema_version must be 1")
    if registry.get("states") != sorted(registry.get("states", [])):
        errors.append("registry states must be sorted")
    if set(registry.get("states", [])) != STATES:
        errors.append("registry states do not match the factory state contract")
    if set(registry.get("stages", [])) != STAGES:
        errors.append("registry stages do not match the distribution lifecycle")
    sources = {source.get("id") for source in registry.get("sources", [])}
    if len(sources) != len(registry.get("sources", [])):
        errors.append("registry source ids must be unique")
    seen: set[str] = set()
    for index, capability in enumerate(registry.get("capabilities", [])):
        prefix = f"capabilities[{index}]"
        capability_id = capability.get("id")
        if capability_id in seen:
            errors.append(f"{prefix}: duplicate id {capability_id}")
        seen.add(capability_id)
        for field in ("id", "name", "kind", "state", "supported_platforms", "tooling", "required_evidence", "limitations", "verification_evidence", "references", "blocking_issues"):
            if field not in capability:
                errors.append(f"{prefix}: missing {field}")
        if capability.get("state") not in STATES:
            errors.append(f"{prefix}: invalid state")
        if not isinstance(capability.get("supported_platforms"), list) or not capability.get("supported_platforms"):
            errors.append(f"{prefix}: supported_platforms must be non-empty")
        if not capability.get("limitations"):
            errors.append(f"{prefix}: limitations are required")
        stage_states = capability.get("stages", {})
        if set(stage_states) != STAGES:
            errors.append(f"{prefix}: stage support must cover every distribution stage")
        for stage, state in stage_states.items():
            if state not in STATES:
                errors.append(f"{prefix}: invalid state for {stage}")
        for source in capability.get("references", []):
            if source not in sources:
                errors.append(f"{prefix}: unknown Apple source {source}")
        for issue in capability.get("blocking_issues", []):
            if not isinstance(issue, int) or issue <= 0:
                errors.append(f"{prefix}: blocking issue must be a positive issue number")
    if not registry.get("capabilities"):
        errors.append("registry must contain capabilities")
    return errors


def finding(kind: str, code: str, title: str, requirement: str, evidence: list[str], truth: str, verify: str, issue: int | None, layer: str = "STRUCTURAL", classification: str | None = None) -> dict[str, Any]:
    if classification is None:
        classification = "BLOCKER" if kind == "BLOCKER" else "WARNING"
    return {
        "type": kind,
        "classification": classification,
        "validation_layer": layer,
        "code": code,
        "title": title,
        "requirement_at_risk": requirement,
        "evidence": evidence,
        "must_become_true": truth,
        "verification": verify,
        "linked_issue": issue,
    }


def _identity_finding(product: dict[str, Any], code: str, title: str, requirement: str, evidence: list[str], truth: str, verify: str, classification: str = "BLOCKER") -> dict[str, Any]:
    return finding("BLOCKER" if classification == "BLOCKER" else "LIKELY_REVIEW_CONCERN", code, title, requirement, evidence, truth, verify, product.get("identity", {}).get("blocking_issue") or product.get("default_blocking_issue"), "SEMANTIC", classification)


def review_identity(product: dict[str, Any]) -> list[dict[str, Any]]:
    identity = product.get("identity", {})
    metadata = product.get("metadata", {})
    public_name = str(identity.get("public_name") or metadata.get("name") or "").strip()
    internal_name = str(identity.get("internal_codename") or product.get("id") or "").strip()
    purpose = " ".join(str(value) for value in (product.get("app_type"), identity.get("product_purpose"), identity.get("customer_zero_alignment"))).lower()
    findings: list[dict[str, Any]] = []
    if not public_name or not identity.get("authorized"):
        findings.append(_identity_finding(product, "PUBLIC_IDENTITY_UNRESOLVED", "Authorized public product identity is unresolved", "App Review metadata must identify an intentional, authorized customer-facing product.", [f"public_name={public_name!r}", f"internal_codename={internal_name!r}", f"authorized={bool(identity.get('authorized'))}"], "An owner-authorized public identity is recorded and traceable to the product purpose.", "Review the identity decision and retain explicit owner authorization before App Review readiness."))
    if public_name and (PLACEHOLDER_RE.search(public_name) or TECHNICAL_NAME_RE.search(public_name)):
        findings.append(_identity_finding(product, "PLACEHOLDER_OR_INTERNAL_PUBLIC_NAME", "Public name appears to be placeholder or internal terminology", "Customer-facing metadata must not expose factory codenames or temporary copy.", [f"public_name={public_name!r}"], "The public name is distinctive, intentional, customer-facing, and not an internal artifact.", "Compare the public name with authorized identity evidence and the product page.", "BLOCKER"))
    if public_name and len(public_name.split()) == 1 and public_name.lower() in {"app", "voice", "pet", "notes", "capture", "recorder", "product"}:
        findings.append(_identity_finding(product, "GENERIC_PUBLIC_NAME", "Public name is generic and requires human judgment", "A customer should be able to understand and find the product without meaningless naming.", [f"public_name={public_name!r}"], "The name is distinctive enough for the product purpose and discoverability context.", "Perform human naming and collision review before readiness.", "REQUIRES_HUMAN_JUDGMENT"))
    if public_name and identity.get("authorized") and identity.get("customer_zero_alignment") is False:
        findings.append(_identity_finding(product, "PUBLIC_NAME_PURPOSE_MISMATCH", "Public name does not fit Customer Zero or product purpose", "Public identity must accurately represent the product received.", [f"public_name={public_name!r}", f"purpose={purpose!r}"], "Customer Zero recognizes the product and its outcome from the public identity.", "Review the name against the canonical Customer Zero record and product journey."))
    return findings


def review_metadata(product: dict[str, Any]) -> list[dict[str, Any]]:
    metadata = product.get("metadata", {})
    issue = product.get("default_blocking_issue")
    findings: list[dict[str, Any]] = []
    public_name = str(product.get("identity", {}).get("public_name") or "").strip()
    metadata_name = str(metadata.get("name") or "").strip()
    if public_name and metadata_name and public_name.casefold() != metadata_name.casefold():
        findings.append(finding("METADATA_DEFECT", "PUBLIC_NAME_MISMATCH", "Store name disagrees with authorized public identity", "Public product identity must be consistent across store metadata and identity evidence.", [f"public_name={public_name!r}", f"metadata.name={metadata_name!r}"], "The authorized public name is propagated consistently without changing technical identifiers.", "Compare the identity record with the App Store metadata draft.", issue, "SEMANTIC", "BLOCKER"))
    for field, value in metadata.items():
        text = str(value or "").strip()
        if text and PLACEHOLDER_COPY_RE.search(text):
            findings.append(finding("METADATA_DEFECT", "PLACEHOLDER_METADATA_COPY", f"{field} contains placeholder copy", "Public metadata must be finished and customer-facing.", [f"{field}={text!r}"], "The field contains intentional product-true copy.", "Review the field against product evidence and the public submission draft.", issue, "SEMANTIC", "BLOCKER"))
        if field.endswith("_url") and text and any(token in text.lower() for token in ("example.com", "localhost", "todo", "placeholder")):
            findings.append(finding("METADATA_DEFECT", "PLACEHOLDER_METADATA_URL", f"{field} appears to be a placeholder URL", "Public support and privacy destinations must be real and customer-facing.", [f"{field}={text!r}"], "The URL resolves to the intended support or privacy destination.", "Perform a safe URL and content review before submission.", issue, "REVIEWER", "BLOCKER"))
    return findings


def review_discoverability(product: dict[str, Any]) -> list[dict[str, Any]]:
    discoverability = product.get("discoverability", {})
    if not product.get("identity", {}).get("authorized"):
        return []
    if not discoverability.get("reviewed"):
        return [finding("BLOCKER", "DISCOVERABILITY_REVIEW_MISSING", "Discoverability review is incomplete", "A customer who needs the product must be able to understand and reasonably find it.", ["discoverability.reviewed=false or absent"], "Name, subtitle, keywords, category, description, developer identity, and screenshot story are reviewed for clarity, consistency, and non-stuffing.", "Perform the current Apple metadata and customer-facing discoverability review.", product.get("default_blocking_issue"), "REVIEWER", "REQUIRES_HUMAN_JUDGMENT")]
    if discoverability.get("keyword_stuffing") or discoverability.get("unsupported_claims"):
        return [finding("BLOCKER", "DISCOVERABILITY_METADATA_CONCERN", "Discoverability metadata contains reviewer concerns", "Discoverability must communicate the product honestly rather than use stuffing or unsupported claims.", [f"keyword_stuffing={bool(discoverability.get('keyword_stuffing'))}", f"unsupported_claims={bool(discoverability.get('unsupported_claims'))}"], "The metadata communicates a clear, accurate product outcome without manipulation.", "Review the metadata against the product evidence and current Apple guidance.", product.get("default_blocking_issue"), "REVIEWER", "BLOCKER")]
    return []


def review_screenshots(product: dict[str, Any]) -> list[dict[str, Any]]:
    screenshots = product.get("screenshots", {})
    if screenshots.get("valid") and not screenshots.get("reviewer_validated"):
        return [finding("LIKELY_REVIEW_CONCERN", "SCREENSHOTS_NOT_REVIEWER_VALIDATED", "Screenshots are structurally valid but not reviewer validated", "App Store screenshots must show the current product journey without internal or misleading material.", ["screenshots.valid=true", "screenshots.reviewer_validated=false"], "Current-build screenshots are coherent, customer-facing, and representative of Customer Zero's journey.", "Inspect each screenshot for overlays, placeholders, unsupported claims, and identity consistency.", product.get("default_blocking_issue"), "REVIEWER", "BLOCKER")]
    return []


def preflight(product: dict[str, Any], registry: dict[str, Any]) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    issue = product.get("default_blocking_issue")
    evidence = product.get("evidence", {})
    if not evidence.get("archive"):
        findings.append(finding("BLOCKER", "BUILD_ARCHIVE_MISSING", "No exact signed archive", "A reviewable build must be archived, signed, and inspectable.", ["product manifest: evidence.archive is absent"], "An exact archive exists and its bundle metadata, signing, entitlements, and privacy manifests are recorded.", "Run the product archive command and inspect the exported artifact.", issue))
    elif evidence.get("archive_development_signed"):
        findings.append(finding("BLOCKER", "ARCHIVE_DEVELOPMENT_SIGNING", "Archive is development-signed", "A TestFlight build must not carry development signing entitlements.", [f"archive inspection: {evidence.get('archive_inspection', 'not recorded')}", "get-task-allow=true"], "The exact archive is signed for distribution with get-task-allow=false.", "Inspect the archive code signature and embedded provisioning profile.", issue))
    required_metadata = ["name", "subtitle", "description", "keywords", "category", "copyright", "support_url", "privacy_url"]
    metadata = product.get("metadata", {})
    missing_metadata = [field for field in required_metadata if not str(metadata.get(field, "")).strip()]
    if missing_metadata:
        findings.append(finding("METADATA_DEFECT", "METADATA_INCOMPLETE", "Required store metadata is missing", "App Store Connect metadata must be complete and accurate.", [f"missing fields: {', '.join(missing_metadata)}"], "All applicable metadata fields are populated from product truth and reviewed.", "Validate the metadata draft against the App Store Connect field contract.", issue))
    findings.extend(review_identity(product))
    findings.extend(review_metadata(product))
    findings.extend(review_discoverability(product))
    if not evidence.get("customer_zero"):
        findings.append(finding("EVIDENCE_GAP", "CUSTOMER_ZERO_MISSING", "Customer Zero story is not bound to the submission", "Store claims and screenshots must represent the actual product journey.", ["product manifest: evidence.customer_zero is false"], "The primary customer, outcome, critical journey, and store story are traceable.", "Compare metadata and screenshots with the canonical customer-zero record.", issue))
    privacy = product.get("privacy", {})
    if privacy.get("collected_data") != privacy.get("declared_data"):
        findings.append(finding("BLOCKER", "PRIVACY_CONTRADICTION", "Privacy declarations contradict product evidence", "App Privacy answers must describe actual collected and transmitted data.", [f"collected_data={privacy.get('collected_data')!r}", f"declared_data={privacy.get('declared_data')!r}"], "The actual data inventory, SDK behavior, purpose strings, privacy policy, and App Privacy declaration agree.", "Inspect source, SDKs, archive contents, runtime network behavior, and declarations.", issue))
    if not product.get("age_rating", {}).get("complete"):
        findings.append(finding("BLOCKER", "AGE_RATING_MISSING", "Age rating is incomplete", "An unrated product cannot be App Review ready.", ["product manifest: age_rating.complete is false"], "Accurate age-rating answers are recorded for the actual product content and behavior.", "Complete the current App Store Connect age-rating questionnaire and review it against product evidence.", issue))
    screenshots = product.get("screenshots", {})
    if not screenshots.get("valid"):
        findings.append(finding("BLOCKER", "SCREENSHOTS_INVALID", "Screenshot candidates are invalid or absent", "Screenshots must match supported device families, dimensions, content, and build.", ["product manifest: screenshots.valid is false"], "Current-build, device-correct, opaque screenshot candidates pass dimension and traceability checks.", "Run the existing capture pipeline and validate its asset manifest.", issue))
    findings.extend(review_screenshots(product))
    if not product.get("review_information", {}).get("complete"):
        findings.append(finding("BLOCKER", "REVIEW_INFORMATION_MISSING", "App Review information is incomplete", "Reviewers need contact information, notes, setup, and access to non-obvious functionality.", ["product manifest: review_information.complete is false"], "Reviewer contact, notes, setup instructions, demo credentials if applicable, and hardware requirements are complete.", "Validate the review-information draft before submission preparation.", issue))
    if product.get("purchases", {}).get("applicable") and not product.get("purchases", {}).get("configured"):
        findings.append(finding("BLOCKER", "PURCHASE_CONFIGURATION_MISSING", "Purchase configuration is incomplete", "IAP/subscription products require valid StoreKit behavior and App Store metadata.", ["product manifest: purchases.applicable=true and configured=false"], "Products, pricing, restore, failure, entitlement, and review metadata are configured and tested.", "Run StoreKit tests and validate the App Store Connect product draft.", issue))
    if product.get("universal_device_families") and not evidence.get("orientation_matrix"):
        findings.append(finding("EVIDENCE_GAP", "ORIENTATION_MATRIX_MISSING", "Universal-app orientation evidence is incomplete", "Universal iPhone/iPad submissions must demonstrate supported orientation behavior.", ["product manifest: universal_device_families=true", "product manifest: evidence.orientation_matrix is false or absent"], "A device-family orientation matrix covers the supported iPhone and iPad journeys.", "Run orientation UI coverage on each declared device family.", issue))
    if product.get("purchases", {}).get("applicable") and "disclosure_evidence" in product.get("purchases", {}) and not product.get("purchases", {}).get("disclosure_evidence"):
        findings.append(finding("EVIDENCE_GAP", "PURCHASE_DISCLOSURE_EVIDENCE_MISSING", "Purchase disclosure evidence is incomplete", "Paywall and purchase disclosures must be readable and reviewable in the submitted journey.", ["product manifest: purchases.disclosure_evidence=false"], "A UI test or captured review artifact demonstrates the complete purchase disclosure text.", "Exercise the paywall disclosure journey with scrolling and full-text verification.", issue))
    if not evidence.get("accessibility"):
        findings.append(finding("EVIDENCE_GAP", "ACCESSIBILITY_EVIDENCE_MISSING", "Accessibility evidence is incomplete", "Accessibility declarations must reflect tested behavior.", ["product manifest: evidence.accessibility is false"], "Automated and applicable device assistive-technology evidence supports each declaration.", "Run accessibility audits and applicable device traversal checks.", issue))
    if not product.get("export_compliance", {}).get("decided"):
        findings.append(finding("EVIDENCE_GAP", "EXPORT_COMPLIANCE_UNDECIDED", "Export compliance decision is missing", "Encryption/export questions must be answered accurately before submission.", ["product manifest: export_compliance.decided is false"], "The encryption inventory and applicable export answers are reviewed and recorded.", "Complete the current export-compliance questionnaire and retain required documentation.", issue))
    unlinked = [item["code"] for item in findings if item["type"] == "BLOCKER" and not item.get("linked_issue")]
    invalid_types = [item["code"] for item in findings if item["type"] not in FINDING_TYPES or item.get("classification") not in FINDING_CLASSIFICATIONS]
    blocker = any(item["type"] == "BLOCKER" for item in findings)
    evidence_gap = any(item["type"] == "EVIDENCE_GAP" for item in findings)
    app_review_ready = not blocker and not evidence_gap and bool(evidence.get("archive"))
    blockers = [item for item in findings if item["type"] == "BLOCKER"]
    evidence_gaps = [item for item in findings if item["type"] == "EVIDENCE_GAP"]
    states = {
        "build_ready": bool(product.get("software_production_ready")),
        "test_ready": bool(product.get("evidence", {}).get("tests")),
        "product_validation_ready": bool(product.get("software_production_ready")) and not blockers and not evidence_gaps,
        "archive_ready": bool(evidence.get("archive")) and not any(item["code"] == "ARCHIVE_DEVELOPMENT_SIGNING" for item in findings),
        "software_production_ready": bool(product.get("software_production_ready")),
        "distribution_ready": bool(evidence.get("archive")),
        "internal_testflight_ready": bool(evidence.get("processed_build")) and not blocker,
        "external_testflight_ready": bool(evidence.get("external_testflight")) and not blocker,
        "app_review_ready": app_review_ready,
        "human_authorized": bool(product.get("human_authorized")),
        "submission": "NOT_SUBMITTED",
    }
    return {
        "schema_version": 1,
        "product": product.get("id"),
        "platform": product.get("platform"),
        "app_type": product.get("app_type"),
        "factory_support_state": product.get("factory_support_state"),
        "states": states,
        "release_stage": next(
            (stage for stage, ready in (
                ("BUILD", states["build_ready"]),
                ("TEST", states["test_ready"]),
                ("PRODUCT_VALIDATION", states["product_validation_ready"]),
                ("ARCHIVE", states["archive_ready"]),
                ("INTERNAL_TESTFLIGHT", states["internal_testflight_ready"]),
                ("EXTERNAL_TESTFLIGHT", states["external_testflight_ready"]),
                ("APP_STORE_READINESS", states["app_review_ready"]),
            ) if not ready),
            "APP_STORE_READINESS",
        ),
        "identity_review": {
            "internal_codename": product.get("identity", {}).get("internal_codename"),
            "public_name": product.get("identity", {}).get("public_name"),
            "candidate_public_name": product.get("identity", {}).get("candidate_public_name"),
            "authorized": bool(product.get("identity", {}).get("authorized")),
            "state": "RESOLVED" if product.get("identity", {}).get("authorized") and product.get("identity", {}).get("public_name") else "UNRESOLVED",
            "workflow": "CUSTOMER_ZERO -> PURPOSE -> CANDIDATES -> COLLISION_AND_TRADEMARK_RESEARCH -> HUMAN_SELECTION -> AUTHORIZATION -> PROPAGATION",
        },
        "validation_layers": {layer: sum(1 for item in findings if item.get("validation_layer") == layer) for layer in ("STRUCTURAL", "SEMANTIC", "REVIEWER")},
        "findings": findings,
        "unlinked_blockers": unlinked,
        "invalid_finding_types": invalid_types,
        "human_authority": {"required_for": "APP_REVIEW_READY -> SUBMITTED", "authorized": states["human_authorized"], "submission_performed": False},
        "evidence_levels": {
            "local_implementation_proof": bool(product.get("software_production_ready")),
            "apple_pipeline_proof": bool(evidence.get("processed_build")),
            "real_release_history": bool(product.get("evidence", {}).get("external_testflight")),
        },
        "evidence_strength": normalized_evidence_levels(product),
        "apple_approval_claim": "NEVER_CLAIMED",
        "registry_capabilities": len(registry.get("capabilities", [])),
        "unjustified_manual": 0,
    }


def submission_draft(product: dict[str, Any], report: dict[str, Any]) -> dict[str, Any]:
    """Create a local, non-submitting App Store Connect preparation artifact."""
    return {
        "schema_version": 1,
        "kind": "APP_STORE_CONNECT_DRAFT",
        "product": product.get("id"),
        "platform": product.get("platform"),
        "metadata": product.get("metadata", {}),
        "screenshots": product.get("screenshots", {}),
        "privacy": product.get("privacy", {}),
        "age_rating": product.get("age_rating", {}),
        "purchases": product.get("purchases", {}),
        "export_compliance": product.get("export_compliance", {}),
        "review_information": product.get("review_information", {}),
        "build_association": {"archive": product.get("evidence", {}).get("archive"), "processed_build": product.get("evidence", {}).get("processed_build", False)},
        "preflight_report": f".factory/artifacts/reports/apple-distribution/{product.get('id')}.json",
        "submission": {"performed": False, "human_authorization_required": True, "endpoint": "NOT_INVOKED"},
        "secrets": "NONE",
        "apple_approval_claim": "NEVER_CLAIMED",
        "readiness": report["states"],
    }


def can_submit(report: dict[str, Any], explicit_human_authorization: bool = False) -> bool:
    """The factory never submits; this is intentionally always false."""
    return False


def archive_plan(product: dict[str, Any]) -> dict[str, Any]:
    build = product.get("build", {})
    required = ["project", "scheme", "bundle_id"]
    missing = [field for field in required if not str(build.get(field, "")).strip()]
    return {
        "schema_version": 1,
        "kind": "XCODE_ARCHIVE_PLAN",
        "product": product.get("id"),
        "status": "BLOCKED_INPUT_MISSING" if missing else "READY_TO_EXECUTE_WITH_HUMAN_RELEASE_CONTEXT",
        "missing_inputs": missing,
        "command_template": "xcodebuild -project <project> -scheme <scheme> -configuration Release -destination 'generic/platform=iOS' archive",
        "submission": {"performed": False, "human_authorization_required": True, "endpoint": "NOT_INVOKED"},
        "secrets": "NONE",
    }


def discovery(registry: dict[str, Any]) -> str:
    lines = ["# Apple Distribution Capabilities", "", f"Last verified: {registry['last_verified']}", "", "The registry is authoritative: `.factory/apple-distribution/capabilities.json`.", "", "| Capability | State | Platforms | App Review stage |", "|---|---|---|---|"]
    for capability in registry["capabilities"]:
        lines.append(f"| `{capability['name']}` | `{capability['state']}` | {', '.join(capability['supported_platforms'])} | `{capability['stages']['app_review']}` |")
    products = canonical_products()
    lines.extend(["", "## Canonical Apple Products", "", "Distribution consumes `.factory/portfolio.yaml` and does not maintain a product registry.", "", "| Product | Repository | Lifecycle | Release state |", "|---|---|---|---|"])
    for product in products:
        lines.append(f"| `{product['id']}` | `{product['repository']}` | `{product['lifecycle']}` | `{product['release_state']}` |")
    lines.extend(["", "## Human Authority", "", "The factory may prepare evidence and drafts, but never submits, publishes, or releases. `APP_REVIEW_READY` is not Apple approval."])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=REGISTRY)
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--list", action="store_true", dest="list_capabilities")
    parser.add_argument("--can", metavar="CAPABILITY")
    parser.add_argument("--product", metavar="PRODUCT")
    parser.add_argument("--write-discovery", action="store_true")
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--write-draft", action="store_true")
    parser.add_argument("--write-archive-plan", action="store_true")
    parser.add_argument("--mode", choices=sorted(MODES), default="PREFLIGHT")
    args = parser.parse_args()
    if args.mode in {"DELIVER", "SUBMIT", "RELEASE"}:
        print(f"ERROR: {args.mode} is hard-denied; explicit human authority does not enable this factory path")
        return 3
    registry = load(args.registry)
    errors = validate_registry(registry)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    product_paths = sorted(PRODUCTS.glob("*.json"))
    inventory_errors = validate_product_inventory([load(path) for path in product_paths])
    if inventory_errors:
        for error in inventory_errors:
            print(f"ERROR: {error}")
        return 1
    if args.validate:
        print("Apple distribution registry validation passed")
    if args.list_capabilities:
        for capability in registry["capabilities"]:
            print(f"{capability['id']}: {capability['state']}")
    if args.can:
        matches = [item for item in registry["capabilities"] if item["id"] == args.can or item["name"].lower() == args.can.lower()]
        if not matches:
            print(f"UNKNOWN capability: {args.can}")
            return 2
        print(json.dumps(matches[0], indent=2, sort_keys=True))
    if args.write_discovery:
        target = ROOT / "docs/apple-distribution-capabilities.md"
        target.write_text(discovery(registry), encoding="utf-8")
        print(target)
    if args.product:
        product_path = PRODUCTS / f"{args.product}.json"
        if not product_path.is_file():
            print(f"ERROR: product manifest missing: {product_path}")
            return 1
        report = preflight(load(product_path), registry)
        print(json.dumps(report, indent=2, sort_keys=True))
        if args.write_report:
            REPORTS.mkdir(parents=True, exist_ok=True)
            target = REPORTS / f"{args.product}.json"
            target.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            print(target)
        if args.write_draft:
            REPORTS.mkdir(parents=True, exist_ok=True)
            target = REPORTS / f"{args.product}-submission-draft.json"
            target.write_text(json.dumps(submission_draft(load(product_path), report), indent=2, sort_keys=True) + "\n", encoding="utf-8")
            print(target)
        if args.write_archive_plan:
            REPORTS.mkdir(parents=True, exist_ok=True)
            target = REPORTS / f"{args.product}-archive-plan.json"
            target.write_text(json.dumps(archive_plan(load(product_path)), indent=2, sort_keys=True) + "\n", encoding="utf-8")
            print(target)
        if report["unlinked_blockers"] or report["invalid_finding_types"]:
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
