import json
import sys
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
github_release = MODULE.github_release
pypi_metadata = MODULE.pypi_metadata
validate_github_contract = MODULE.validate_github_contract


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

    @patch.object(MODULE, "fetch_json")
    def test_github_metadata_contract_blocks_stale_homepage(self, fetch_json):
        fetch_json.return_value = {
            "html_url": "https://github.com/edoworks/rung",
            "description": "Rung",
            "homepage": "https://rung.edoworks.com/",
            "visibility": "public",
            "fork": False,
            "archived": False,
            "default_branch": "main",
            "license": {"spdx_id": "MIT"},
        }
        result = github_metadata(
            "edoworks/rung",
            1,
            {"homepage": "https://edoworks.com/rung/", "license": "MIT"},
        )
        self.assertEqual(result["status"], "blocked")
        self.assertIn("homepage mismatch", result["errors"][0])

    @patch.object(MODULE, "fetch_json")
    def test_explicit_mixed_license_policy_allows_missing_root_license(self, fetch_json):
        fetch_json.return_value = {
            "html_url": "https://github.com/edoworks/artifacts",
            "description": "Artifacts",
            "homepage": None,
            "visibility": "public",
            "fork": False,
            "archived": False,
            "default_branch": "main",
            "license": None,
        }
        result = github_metadata(
            "edoworks/artifacts",
            1,
            {"license": None, "allow_missing_license": True},
        )
        self.assertEqual(result["status"], "pass")

    @patch.object(MODULE, "fetch")
    def test_lifecycle_assertions_block_contradiction(self, fetch):
        fetch.return_value = (200, "https://site.test/", "Concept preview; beta not open")
        result = audit("https://site.test/", None, ["Concept preview"], ["Beta is open"], 1, False)
        self.assertEqual(result["status"], "pass")
        result = audit("https://site.test/", None, ["Concept preview"], ["beta not open"], 1, False)
        self.assertEqual(result["status"], "blocked")

    @patch.object(MODULE, "fetch_json")
    def test_draft_release_blocks(self, fetch_json):
        fetch_json.return_value = {"html_url": "https://github.com/o/r/releases/tag/v1", "draft": True, "prerelease": False}
        self.assertEqual(github_release("o/r", "v1", 1)["status"], "blocked")

    @patch.object(MODULE, "fetch_json")
    def test_release_contract_checks_immutability_and_assets(self, fetch_json):
        fetch_json.return_value = {
            "html_url": "https://github.com/o/r/releases/tag/v1",
            "draft": False,
            "prerelease": False,
            "immutable": False,
            "assets": [],
        }
        result = github_release(
            "o/r",
            "v1",
            1,
            {"immutable": True, "asset_count": 1, "asset_names": ["artifact.tar.gz"]},
        )
        self.assertEqual(result["status"], "blocked")
        self.assertTrue(any("immutable mismatch" in error for error in result["errors"]))
        self.assertTrue(any("asset_count mismatch" in error for error in result["errors"]))

    @patch.object(MODULE, "fetch")
    @patch.object(MODULE, "fetch_json")
    def test_release_contract_binds_tag_distribution_and_documentation(self, fetch_json, fetch):
        fetch_json.side_effect = [
            {
                "html_url": "https://github.com/o/r/releases/tag/v1",
                "draft": False,
                "prerelease": False,
                "immutable": False,
                "assets": [],
            },
            {"object": {"type": "commit", "sha": "a" * 40}},
        ]
        fetch.side_effect = [
            (200, "https://archive.test/final.tar.gz", ""),
            (200, "https://docs.test/README.md", f"REVISION={'a' * 40}"),
        ]
        result = github_release(
            "o/r",
            "v1",
            1,
            {
                "tag_target_commit": "a" * 40,
                "distribution_url": "https://archive.test/v1.tar.gz",
                "documentation_url": "https://docs.test/README.md",
                "documentation_contains": [f"REVISION={'a' * 40}"],
            },
        )
        self.assertEqual(result["status"], "pass")
        self.assertEqual(result["tag_target_commit"], "a" * 40)

    def test_github_contract_rejects_empty_or_incomplete_document(self):
        errors = validate_github_contract({})
        self.assertIn("contract fields drifted", errors)
        self.assertTrue(any("non-empty" in error for error in errors))

    def test_checked_in_github_contract_schema_is_valid(self):
        contract_path = Path(__file__).parents[1] / ".factory/repository-metadata-target.json"
        contract = json.loads(contract_path.read_text())
        self.assertEqual(validate_github_contract(contract), [])

        del contract["repositories"][0]["homepage"]
        self.assertTrue(
            any("repositories[0] fields drifted" in error for error in validate_github_contract(contract))
        )

    def test_github_contract_requires_digests_for_attached_assets(self):
        contract_path = Path(__file__).parents[1] / ".factory/repository-metadata-target.json"
        contract = json.loads(contract_path.read_text())
        constitution = next(
            release
            for release in contract["releases"]
            if release["tag"] == "constitution/v1.0.0"
        )
        del constitution["asset_digests"]
        self.assertTrue(
            any("asset digests are incomplete" in error for error in validate_github_contract(contract))
        )

    def test_github_contract_rejects_boolean_integer_substitution(self):
        contract_path = Path(__file__).parents[1] / ".factory/repository-metadata-target.json"
        contract = json.loads(contract_path.read_text())
        contract["repositories"][0]["archived"] = 0
        contract["releases"][0]["draft"] = 0
        contract["releases"][0]["asset_count"] = False
        errors = validate_github_contract(contract)
        self.assertTrue(any("lifecycle flags are invalid" in error for error in errors))
        self.assertTrue(any("release flags are invalid" in error for error in errors))
        self.assertTrue(any("asset inventory is invalid" in error for error in errors))

    @patch.object(MODULE, "github_release")
    @patch.object(MODULE, "github_metadata")
    def test_complete_contract_passes_declared_blocker_mode_when_all_checks_pass(
        self, github_metadata_mock, github_release_mock
    ):
        contract_path = Path(__file__).parents[1] / ".factory/repository-metadata-target.json"
        contract = json.loads(contract_path.read_text())
        github_metadata_mock.side_effect = [
            {"repo": item["repo"], "errors": [], "status": "pass"}
            for item in contract["repositories"]
        ]
        github_release_mock.side_effect = [
            {"repo": item["repo"], "tag": item["tag"], "errors": [], "status": "pass"}
            for item in contract["releases"]
        ]

        with patch.object(
            sys,
            "argv",
            [
                "public-surface-preflight.py",
                "--github-contract",
                str(contract_path),
                "--allow-declared-blockers",
            ],
        ):
            self.assertEqual(MODULE.main(), 0)

    @patch.object(MODULE, "github_release")
    @patch.object(MODULE, "github_metadata")
    def test_complete_contract_rejects_any_live_blocker(
        self, github_metadata_mock, github_release_mock
    ):
        contract_path = Path(__file__).parents[1] / ".factory/repository-metadata-target.json"
        contract = json.loads(contract_path.read_text())
        github_metadata_mock.side_effect = [
            {
                "repo": item["repo"],
                "errors": ["drift"] if index == 0 else [],
                "status": "blocked" if index == 0 else "pass",
            }
            for index, item in enumerate(contract["repositories"])
        ]
        github_release_mock.side_effect = [
            {"repo": item["repo"], "tag": item["tag"], "errors": [], "status": "pass"}
            for item in contract["releases"]
        ]

        with patch.object(
            sys,
            "argv",
            [
                "public-surface-preflight.py",
                "--github-contract",
                str(contract_path),
                "--allow-declared-blockers",
            ],
        ):
            self.assertEqual(MODULE.main(), 1)

    @patch.object(MODULE, "fetch_json")
    def test_missing_package_license_blocks(self, fetch_json):
        fetch_json.return_value = {"info": {"version": "1.0.0", "license": None, "home_page": None}}
        result = pypi_metadata("example-package", 1)
        self.assertEqual(result["status"], "blocked")
        self.assertIn("declared license", result["errors"][0])

    @patch.object(MODULE, "fetch_json")
    def test_modern_package_license_metadata_passes(self, fetch_json):
        fetch_json.return_value = {
            "info": {
                "version": "1.0.0",
                "license": None,
                "license_expression": "MIT",
                "home_page": None,
            }
        }
        self.assertEqual(pypi_metadata("example-package", 1)["status"], "pass")


if __name__ == "__main__":
    unittest.main()
