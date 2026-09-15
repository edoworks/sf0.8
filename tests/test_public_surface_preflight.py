import unittest
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "public-surface-preflight.py"
SPEC = spec_from_file_location("public_surface_preflight", MODULE_PATH)
MODULE = module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)

PageParser = MODULE.PageParser
PLACEHOLDER_RE = MODULE.PLACEHOLDER_RE


class PublicSurfacePreflightTests(unittest.TestCase):
    def test_detects_public_placeholders(self):
        self.assertTrue(PLACEHOLDER_RE.search("Read [RUNG_DOCS_URL]"))
        self.assertTrue(PLACEHOLDER_RE.search("lorem ipsum"))
        self.assertFalse(PLACEHOLDER_RE.search("Beta coming soon"))
        self.assertFalse(PLACEHOLDER_RE.search("https://github.com/edoworks/rung"))

    def test_extracts_links_and_canonical(self):
        parser = PageParser()
        parser.feed(
            '<link rel="canonical" href="/rung/">'
            '<a href="https://github.com/edoworks/rung">Source</a>'
        )
        self.assertEqual(parser.canonicals, ["/rung/"])
        self.assertEqual(parser.links, ["https://github.com/edoworks/rung"])


if __name__ == "__main__":
    unittest.main()
