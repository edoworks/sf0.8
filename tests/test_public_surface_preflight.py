import unittest
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from unittest.mock import patch


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "public-surface-preflight.py"
SPEC = spec_from_file_location("public_surface_preflight", MODULE_PATH)
MODULE = module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)

PageParser = MODULE.PageParser
PLACEHOLDER_RE = MODULE.PLACEHOLDER_RE
audit = MODULE.audit
check_link = MODULE.check_link
github_metadata = MODULE.github_metadata


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

    @patch.object(MODULE, "fetch")
    def test_broken_external_link_blocks_page(self, fetch):
        fetch.side_effect = [
            (200, "https://site.test/", '<a href="https://broken.test">Broken</a>'),
            (404, "https://broken.test/", ""),
        ]
        result = audit("https://site.test/", None, [], [], 1, True)
        self.assertEqual(result["status"], "blocked")
        self.assertIn("HTTP 404", result["errors"][0])

    @patch.object(MODULE, "fetch_json")
    def test_github_metadata_preserves_fork_and_lifecycle(self, fetch_json):
        fetch_json.return_value = {
            "html_url": "https://github.com/edoworks/trycycle",
            "visibility": "public",
            "fork": True,
            "archived": False,
            "license": {"spdx_id": "MIT"},
        }
        result = github_metadata("edoworks/trycycle", 1)
        self.assertEqual(result["status"], "pass")
        self.assertTrue(result["fork"])

    @patch.object(MODULE, "fetch")
    def test_lifecycle_assertions_block_contradiction(self, fetch):
        fetch.return_value = (200, "https://site.test/", "Concept preview; beta not open")
        result = audit("https://site.test/", None, ["Concept preview"], ["Beta is open"], 1, False)
        self.assertEqual(result["status"], "pass")
        result = audit("https://site.test/", None, ["Concept preview"], ["beta not open"], 1, False)
        self.assertEqual(result["status"], "blocked")


if __name__ == "__main__":
    unittest.main()
