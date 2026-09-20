import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


DISCOVERY = load("discover-portfolio")
RECONCILE = load("reconcile-portfolio")
IDENTITY = load("identity_model")


class PortfolioDiscoveryTests(unittest.TestCase):
    def test_identity_model_requires_durable_provenance(self):
        self.assertEqual(IDENTITY.validate_entity({
            "entity_type": "product",
            "entity_id": "opaque",
            "bundle_id": "com.foculoom.opaque",
            "provenance": ["source.json"],
        }), [])
        self.assertTrue(IDENTITY.validate_entity({"entity_type": "product", "entity_id": "opaque"}))

    def test_blind_discovery_uses_distribution_and_bundle_identity(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            history = root / "history.json"
            history.write_text(json.dumps({"apps": [{
                "name": "Historical Shipping App",
                "bundle_id": "com.foculoom.veilsort",
                "asc_status": "Ready for Sale",
                "source": "historical-source",
            }]}))
            product = root / "foculoom" / "products" / "veilsort"
            product.mkdir(parents=True)
            (product / "project.yml").write_text("PRODUCT_BUNDLE_IDENTIFIER: com.foculoom.veilsort\n")
            result = DISCOVERY.discover(foculoom=root / "foculoom", history=history)
            veilsort = next(item for item in result["candidates"] if "com.foculoom.veilsort" in item["bundle_ids"])
            self.assertNotIn("Veilsort", result["discovery_input"])
            self.assertIn(str(history), veilsort["provenance"])
            self.assertIn(str(product), veilsort["local_paths"])

    def test_discovery_is_independent_of_factory_registry(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            history = root / "history.json"
            history.write_text(json.dumps({"apps": [{
                "name": "Unnamed Shipping App",
                "bundle_id": "com.foculoom.opaqueapp",
                "asc_status": "Ready for Sale",
                "source": str(root / "different-repository")
            }]}))
            result = DISCOVERY.discover(foculoom=root / "empty-company", history=history)
            self.assertEqual(result["candidates"][0]["bundle_ids"], ["com.foculoom.opaqueapp"])

    def test_omitted_verified_product_blocks_reconciliation(self):
        discovery = {"candidates": [{
            "product_id": "opaque-app",
            "bundle_ids": ["com.foculoom.opaqueapp"],
            "confidence": "HIGH",
            "distribution_states": ["Ready for Sale"],
            "provenance": ["independent-store-export.json"]
        }]}
        fixture = [{"product_id": "opaque-app", "bundle_id": "com.foculoom.opaqueapp"}]
        result = RECONCILE.reconcile(discovery, fixture, fixture)
        self.assertEqual(result["portfolio_recall"]["value"], 1.0)
        self.assertEqual(result["completion"]["state"], "PORTFOLIO_RECONCILED")

        omitted = RECONCILE.reconcile({"candidates": []}, [], fixture)
        self.assertEqual(omitted["portfolio_recall"]["value"], 0.0)
        self.assertEqual(omitted["completion"]["state"], "PORTFOLIO_RECONCILIATION_BLOCKED")

    def test_product_and_repository_names_need_not_match(self):
        discovery = {"candidates": [{
            "product_id": "opaque-app",
            "bundle_ids": ["com.foculoom.opaqueapp"],
            "repositories": ["foculoom/different-repository"],
            "confidence": "HIGH"
        }]}
        known = [{"id": "opaque-app", "bundle_id": "com.foculoom.opaqueapp", "repository": "foculoom/different-repository"}]
        result = RECONCILE.reconcile(discovery, known, known)
        self.assertEqual(result["matched_factory_products"], ["opaque-app"])
        self.assertEqual(result["portfolio_recall"]["value"], 1.0)

    def test_known_product_without_implementation_fails_closed(self):
        product = {"id": "unbuilt", "bundle_id": "com.foculoom.unbuilt"}
        result = RECONCILE.reconcile({"candidates": []}, [product], [product])
        self.assertEqual(result["portfolio_recall"]["value"], 0.0)
        self.assertFalse(result["completion"]["done"])
        self.assertEqual(result["completion"]["state"], "PORTFOLIO_RECONCILIATION_BLOCKED")


if __name__ == "__main__":
    unittest.main()
