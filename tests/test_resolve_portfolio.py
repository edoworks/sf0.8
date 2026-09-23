import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
SPEC = importlib.util.spec_from_file_location("resolve_portfolio", ROOT / "scripts" / "resolve-portfolio.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class PortfolioResolutionTests(unittest.TestCase):
    def test_product_a_resolves_to_canonical_remote(self):
        result = MODULE.resolve("edoworks/product-a")
        self.assertEqual(result["source_of_truth"], "https://github.com/edoworks/product-a.git")
        self.assertEqual(result["default_branch"], "main")
        self.assertEqual(result["lifecycle"], "shelved")

    def test_unregistered_repository_is_rejected(self):
        with self.assertRaises(ValueError):
            MODULE.resolve("edoworks/not-registered")

    def test_apple_products_are_enumerated_from_canonical_portfolio(self):
        products = MODULE.enumerate_apple_products()
        self.assertEqual({product["id"] for product in products}, {"nownest", "product-a", "vorynce"})
        self.assertEqual(next(product for product in products if product["id"] == "vorynce")["repository"], "foculoom/vorynce")

    def test_historical_products_are_discoverable_without_active_authority(self):
        products = MODULE.enumerate_historical_products()
        self.assertEqual(len(products), 10)
        self.assertEqual({product["lifecycle"] for product in products}, {"dormant", "retired"})
        self.assertEqual(next(product for product in products if product["id"] == "find-my-loophole")["source"], "UNKNOWN")


if __name__ == "__main__":
    unittest.main()
