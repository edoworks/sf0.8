import importlib.util
import copy
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("apple_distribution", ROOT / "scripts/validate-apple-distribution.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class AppleDistributionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = MODULE.load(ROOT / ".factory/apple-distribution/capabilities.json")
        cls.identity_registry = MODULE.load(ROOT / ".factory/identity-registry.json")

    def test_registry_is_complete(self):
        self.assertEqual([], MODULE.validate_registry(self.registry))
        self.assertGreaterEqual(len(self.registry["capabilities"]), 25)

    def test_supported_and_unsupported_discovery(self):
        ios = next(item for item in self.registry["capabilities"] if item["id"] == "ios")
        mac = next(item for item in self.registry["capabilities"] if item["id"] == "macos-native")
        self.assertEqual("SUPPORTED_UNVERIFIED", ios["state"])
        self.assertEqual("UNSUPPORTED", mac["state"])

    def test_partial_capability_is_explicit(self):
        item = next(item for item in self.registry["capabilities"] if item["id"] == "privacy-disclosures")
        self.assertEqual("PARTIAL", item["state"])
        self.assertIn("privacy", item["references"])

    def test_product_a_has_review_blockers_and_issue_links(self):
        product = MODULE.load(ROOT / ".factory/apple-distribution/products/product-a.json")
        report = MODULE.preflight(product, self.registry)
        codes = {item["code"] for item in report["findings"]}
        self.assertIn("AGE_RATING_MISSING", codes)
        self.assertIn("SCREENSHOTS_INVALID", codes)
        self.assertIn("PUBLIC_IDENTITY_UNRESOLVED", codes)
        self.assertTrue(all(item["linked_issue"] for item in report["findings"] if item["type"] == "BLOCKER"))
        self.assertFalse(report["states"]["app_review_ready"])
        self.assertEqual("BUILD", report["release_stage"])

    def test_internal_codename_cannot_reach_app_review_ready(self):
        product = {
            "id": "fixture", "platform": "iOS", "app_type": "pet companion",
            "default_blocking_issue": 35,
            "identity": {"internal_codename": "Product A", "public_name": "Product A", "authorized": False, "blocking_issue": 35},
            "metadata": {field: "Distinctive product copy" for field in ("name", "subtitle", "description", "keywords", "category", "copyright", "support_url", "privacy_url")},
            "privacy": {"collected_data": [], "declared_data": []}, "age_rating": {"complete": True},
            "screenshots": {"valid": True, "reviewer_validated": True}, "review_information": {"complete": True},
            "purchases": {"applicable": False}, "export_compliance": {"decided": True},
            "evidence": {"archive": "release.xcarchive", "processed_build": True, "external_testflight": True, "customer_zero": True, "accessibility": True},
        }
        report = MODULE.preflight(product, self.registry)
        self.assertFalse(report["states"]["app_review_ready"])
        self.assertIn("PLACEHOLDER_OR_INTERNAL_PUBLIC_NAME", {item["code"] for item in report["findings"]})
        self.assertNotEqual("APP_STORE_READINESS", report["release_stage"])

    def test_distinctive_authorized_identity_can_pass_identity_review(self):
        product = {
            "id": "fixture", "app_type": "voice organization", "default_blocking_issue": 35,
            "identity": {"internal_codename": "Voice Tool", "public_name": "Vorynce", "authorized": True, "blocking_issue": 35, "customer_zero_alignment": True},
            "metadata": {field: "Useful customer-facing copy" for field in ("name", "subtitle", "description", "keywords", "category", "copyright", "support_url", "privacy_url")},
        }
        self.assertEqual([], MODULE.review_identity(product))

    def test_placeholder_copy_is_semantic_blocker(self):
        product = {"id": "fixture", "default_blocking_issue": 35, "metadata": {"description": "TODO replace me"}}
        findings = MODULE.review_metadata(product)
        self.assertEqual("PLACEHOLDER_METADATA_COPY", findings[0]["code"])
        self.assertEqual("SEMANTIC", findings[0]["validation_layer"])

    def test_valid_bundle_id_can_differ_from_public_name(self):
        product = {"id": "fixture", "app_type": "voice organization", "identity": {"internal_codename": "Voice Tool", "public_name": "Vorynce", "authorized": True, "customer_zero_alignment": True}, "metadata": {"name": "Vorynce"}}
        self.assertEqual([], MODULE.review_identity(product))

    def test_generic_name_requires_human_judgment(self):
        product = {"id": "fixture", "app_type": "voice organization", "identity": {"internal_codename": "Voice Tool", "public_name": "Voice", "authorized": True, "customer_zero_alignment": True}}
        findings = MODULE.review_identity(product)
        self.assertEqual("REQUIRES_HUMAN_JUDGMENT", findings[0]["classification"])

    def test_authorized_name_inconsistent_with_purpose_is_blocked(self):
        product = {"id": "fixture", "app_type": "voice organization", "identity": {"internal_codename": "Voice Tool", "public_name": "Garden Friends", "authorized": True, "customer_zero_alignment": False}}
        findings = MODULE.review_identity(product)
        self.assertIn("PUBLIC_NAME_PURPOSE_MISMATCH", {item["code"] for item in findings})

    def test_vorynce_iap_gap_and_privacy_manifest_alignment(self):
        product = MODULE.load(ROOT / ".factory/apple-distribution/products/vorynce.json")
        report = MODULE.preflight(product, self.registry)
        codes = {item["code"] for item in report["findings"]}
        self.assertNotIn("PRIVACY_CONTRADICTION", codes)
        self.assertIn("PURCHASE_CONFIGURATION_MISSING", codes)

    def test_public_identity_warning_blocks_app_review(self):
        product = MODULE.load(ROOT / ".factory/apple-distribution/products/vorynce.json")
        report = MODULE.preflight(product, self.registry, MODULE.load(ROOT / ".factory/identity-registry.json"), {
            "status": "WARN",
            "findings": [{"code": "NONCANONICAL_PUBLIC_EMAIL", "classification": "WARNING"}],
        })
        self.assertIn("PUBLIC_IDENTITY_REPORT_NOT_PASSING", {item["code"] for item in report["findings"]})
        self.assertFalse(report["states"]["app_review_ready"])

    def test_missing_review_information_is_detected(self):
        product = {"id": "fixture", "platform": "iOS", "app_type": "app", "factory_support_state": "SUPPORTED_UNVERIFIED", "default_blocking_issue": 35, "metadata": {}, "privacy": {"collected_data": [], "declared_data": []}, "age_rating": {"complete": True}, "screenshots": {"valid": True}, "review_information": {"complete": False}, "purchases": {"applicable": False}, "export_compliance": {"decided": True}, "evidence": {"archive": "archive.xcarchive", "customer_zero": True, "accessibility": True}}
        report = MODULE.preflight(product, self.registry)
        self.assertIn("REVIEW_INFORMATION_MISSING", {item["code"] for item in report["findings"]})

    def test_submission_boundary_is_hard_denied(self):
        product = MODULE.load(ROOT / ".factory/apple-distribution/products/product-a.json")
        report = MODULE.preflight(product, self.registry)
        draft = MODULE.submission_draft(product, report)
        self.assertFalse(MODULE.can_submit(report, explicit_human_authorization=True))
        self.assertFalse(draft["submission"]["performed"])
        self.assertEqual("NONE", draft["secrets"])
        self.assertTrue(draft["preflight_report"].startswith(".factory/"))

    def test_distribution_archive_is_not_development_signed(self):
        product = MODULE.load(ROOT / ".factory/apple-distribution/products/product-a.json")
        report = MODULE.preflight(product, self.registry)
        self.assertNotIn("ARCHIVE_DEVELOPMENT_SIGNING", {item["code"] for item in report["findings"]})
        self.assertTrue(report["states"]["distribution_ready"])
        self.assertFalse(report["evidence_levels"]["apple_pipeline_proof"])

    def test_canonical_inventory_matches_distribution_manifests(self):
        products = [MODULE.load(path) for path in sorted((ROOT / ".factory/apple-distribution/products").glob("*.json"))]
        self.assertEqual([], MODULE.validate_product_inventory(products))

    def test_shelved_product_manifest_is_canonical_but_not_required(self):
        product = MODULE.load(ROOT / ".factory/apple-distribution/products/product-a.json")
        self.assertEqual([], MODULE.validate_product_inventory([product]))
        self.assertFalse(any("product-a" in error for error in MODULE.validate_product_inventory([])))

    def test_archive_plan_fails_closed_without_project_inputs(self):
        product = MODULE.load(ROOT / ".factory/apple-distribution/products/product-a.json")
        plan = MODULE.archive_plan(product)
        self.assertEqual("BLOCKED_INPUT_MISSING", plan["status"])
        self.assertFalse(plan["submission"]["performed"])

    def test_complete_preflight_can_reach_app_review_ready(self):
        product = {
            "id": "complete-fixture", "platform": "iOS", "app_type": "offline app",
            "factory_support_state": "SUPPORTED_UNVERIFIED", "default_blocking_issue": 35,
            "software_production_ready": True,
            "identity": {"internal_codename": "Complete Fixture", "public_name": "present", "authorized": True, "blocking_issue": 35, "customer_zero_alignment": True},
            "discoverability": {"reviewed": True},
            "metadata": {field: "present" for field in ("name", "subtitle", "description", "keywords", "category", "copyright", "support_url", "privacy_url")},
            "privacy": {"collected_data": [], "declared_data": []},
            "age_rating": {"complete": True}, "screenshots": {"valid": True, "reviewer_validated": True},
            "review_information": {"complete": True}, "purchases": {"applicable": False},
            "export_compliance": {"decided": True},
            "evidence": {"archive": "release.xcarchive", "processed_build": True, "external_testflight": True, "customer_zero": True, "accessibility": True},
            "human_authorized": False,
        }
        report = MODULE.preflight(product, self.registry)
        self.assertTrue(report["states"]["app_review_ready"])
        self.assertFalse(report["states"]["human_authorized"])
        self.assertEqual([], report["findings"])

    def test_vorynce_historical_rejection_fixture_is_detected(self):
        fixture = MODULE.load(ROOT / ".factory/artifacts/portfolio-archaeology/fixtures/vorynce-rejection.json")
        report = MODULE.preflight(fixture["product_fixture"], self.registry)
        codes = {item["code"] for item in report["findings"]}
        self.assertTrue(fixture["historical_evidence_only"])
        self.assertIn("ORIENTATION_MATRIX_MISSING", codes)
        self.assertIn("PURCHASE_DISCLOSURE_EVIDENCE_MISSING", codes)

    def test_nownest_is_truthful_non_submitting_and_identity_blocked(self):
        product = MODULE.load(ROOT / ".factory/apple-distribution/products/nownest.json")
        report = MODULE.preflight(product, self.registry, self.identity_registry)
        self.assertEqual("com.foculoom.nownest", product["build"]["bundle_id"])
        self.assertEqual("iOS/iPadOS", product["platform"])
        self.assertEqual("uploaded_processing", product["release_state"])
        self.assertFalse(product["submission"]["performed"])
        self.assertFalse(product["submission"]["apple_accepted"])
        self.assertIn("IDENTITY_CLEARANCE_UNRESOLVED", {item["code"] for item in report["findings"]})
        self.assertFalse(report["states"]["app_review_ready"])
        self.assertFalse(MODULE.can_submit(report, explicit_human_authorization=True))
        serialized = json.dumps(product)
        self.assertNotIn("/Users/", serialized)
        self.assertNotIn("api_key", serialized.casefold())

    def test_vorynce_binds_registry_and_approved_owner_seller(self):
        product = MODULE.load(ROOT / ".factory/apple-distribution/products/vorynce.json")
        self.assertEqual("product:vorynce", product["identity"]["registry_ref"])
        self.assertIn(product["legal"]["owner_name"], product["legal"]["approved_owner_names"])
        self.assertIn(product["legal"]["seller_name"], product["legal"]["approved_seller_names"])

    def nownest_fixture(self):
        return MODULE.load(ROOT / ".factory/apple-distribution/products/nownest.json")

    def governance_codes(self, product, registry=None, public_report=None):
        return {
            item["code"] for item in MODULE.review_identity_governance(
                product, registry or self.identity_registry, public_report
            )
        }

    def test_internal_identity_public_request_is_blocked(self):
        registry = copy.deepcopy(self.identity_registry)
        next(item for item in registry["identities"] if item["entity_id"] == "product:nownest")["trademark_state"] = "INTERNAL"
        self.assertIn("INTERNAL_IDENTITY_PUBLIC_REQUEST", self.governance_codes(self.nownest_fixture(), registry))

    def test_registered_symbol_and_registration_claim_are_blocked(self):
        product = self.nownest_fixture()
        product["public_surface"]["registered_symbol"] = True
        product["public_surface"]["application_described_as_registration"] = True
        codes = self.governance_codes(product)
        self.assertTrue({"UNAUTHORIZED_REGISTERED_SYMBOL", "APPLICATION_DESCRIBED_AS_REGISTERED"} <= codes)

    def test_private_address_report_is_blocked(self):
        report = {"findings": [{"code": "PRIVATE_ADDRESS_PATTERN"}]}
        self.assertIn("PRIVATE_ADDRESS_EXPOSURE", self.governance_codes(self.nownest_fixture(), public_report=report))

    def test_legal_owner_and_seller_conflicts_are_blocked(self):
        product = self.nownest_fixture()
        product["legal"]["owner_name"] = "Other Corp"
        product["legal"]["seller_name"] = "Different Corp"
        codes = self.governance_codes(product)
        self.assertTrue({"LEGAL_OWNER_CONFLICT", "APP_STORE_SELLER_CONFLICT"} <= codes)

    def test_privacy_support_terms_contradiction_is_blocked(self):
        product = self.nownest_fixture()
        product["public_surface"]["privacy_support_terms_consistent"] = False
        self.assertIn("PRIVACY_SUPPORT_TERMS_CONTRADICTION", self.governance_codes(product))

    def test_structured_product_truth_contradictions_are_blocked(self):
        product = self.nownest_fixture()
        product["canonical_claims"]["pricing"] = "canonical-price"
        product["observed_claims"]["pricing"] = "contradictory-price"
        for field in product["observed_claims"]:
            if field != "pricing":
                product["observed_claims"][field] = "contradiction"
        codes = self.governance_codes(product)
        expected = {
            "LIFECYCLE_CONTRADICTION", "PRICING_CONTRADICTION", "PLATFORM_CONTRADICTION",
            "FEATURES_CONTRADICTION", "PRIVACY_CONTRADICTION", "FUNCTION_CONTRADICTION",
            "TRADEMARK_STATE_CONTRADICTION",
        }
        self.assertTrue(expected <= codes)

    def test_provisional_identity_cannot_be_claimed_established(self):
        product = self.nownest_fixture()
        product["identity"]["authorized"] = True
        product["identity"]["identity_state"] = "ESTABLISHED"
        self.assertIn("PROVISIONAL_AS_ESTABLISHED", self.governance_codes(product))


if __name__ == "__main__":
    unittest.main()
