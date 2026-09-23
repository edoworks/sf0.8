import copy
import importlib.util
import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
SPEC = importlib.util.spec_from_file_location(
    "validate_identity_registry", ROOT / "scripts/validate-identity-registry.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class IdentityRegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = json.loads((ROOT / ".factory/identity-registry.json").read_text())
        cls.portfolio = (ROOT / ".factory/portfolio.yaml").read_text()

    def validate(self, registry):
        return MODULE.validate(registry, self.portfolio)

    def test_canonical_registry_is_valid(self):
        self.assertEqual([], self.validate(self.registry))

    def test_private_domicile_value_is_rejected(self):
        registry = copy.deepcopy(self.registry)
        private = next(item for item in registry["address_policies"] if item["category"] == "PRIVATE_DOMICILE")
        private["street_address"] = "must never be committed"
        self.assertTrue(any("metadata only" in error for error in self.validate(registry)))

    def test_address_values_are_rejected_outside_private_domicile(self):
        for target in ("legal_entity", "PUBLIC_MAILING_ADDRESS"):
            with self.subTest(target=target):
                registry = copy.deepcopy(self.registry)
                record = registry["legal_entity"] if target == "legal_entity" else next(item for item in registry["address_policies"] if item["category"] == target)
                record["street_address"] = "must never be committed"
                self.assertTrue(any("repository address values are prohibited" in error for error in self.validate(registry)))

    def test_nested_and_variant_address_keys_are_rejected(self):
        for key in ("mailing_address", "residential_address", "address_line_1", "locality", "province"):
            with self.subTest(key=key):
                registry = copy.deepcopy(self.registry)
                registry["legal_entity"]["metadata"] = {key: "must never be committed"}
                self.assertTrue(any("repository address values are prohibited" in error for error in self.validate(registry)))

    def test_address_values_are_rejected_in_every_record_class(self):
        for group in ("contacts", "identities", "trademarks", "domains"):
            with self.subTest(group=group):
                registry = copy.deepcopy(self.registry)
                registry[group][0]["metadata"] = {"residential_address": "must never be committed"}
                self.assertTrue(any("repository address values are prohibited" in error for error in self.validate(registry)))

    def test_unresolved_identity_cannot_allow_adoption(self):
        registry = copy.deepcopy(self.registry)
        veilsort = next(item for item in registry["identities"] if item["name"] == "Veilsort")
        veilsort["adoption_allowed"] = True
        self.assertTrue(any("block adoption" in error for error in self.validate(registry)))

    def test_unverified_registration_claim_is_rejected(self):
        registry = copy.deepcopy(self.registry)
        registry["trademarks"][0]["registration_claimed"] = True
        self.assertTrue(any("unverified registration" in error for error in self.validate(registry)))

    def test_unsupported_owner_is_rejected(self):
        registry = copy.deepcopy(self.registry)
        registry["trademarks"][1]["owner_name"] = "Unverified Owner"
        self.assertTrue(any("unsupported trademark owner" in error for error in self.validate(registry)))

    def test_duplicate_domain_is_rejected(self):
        registry = copy.deepcopy(self.registry)
        duplicate = copy.deepcopy(registry["domains"][0])
        duplicate["entity_id"] = "domain:duplicate-record"
        registry["domains"].append(duplicate)
        self.assertTrue(any("duplicate domain" in error for error in self.validate(registry)))

    def test_portfolio_lifecycle_contradiction_is_rejected(self):
        registry = copy.deepcopy(self.registry)
        nownest = next(item for item in registry["identities"] if item["name"] == "NowNest")
        nownest["lifecycle"] = "active"
        self.assertTrue(any("lifecycle contradiction" in error for error in self.validate(registry)))

    def test_expected_trademark_records_do_not_claim_registration(self):
        marks = {item["mark"]: item for item in self.registry["trademarks"]}
        self.assertEqual("LEGAL_REVIEW_REQUIRED", marks["FOCULOOM"]["state"])
        self.assertEqual("Movotosa Ojiru", marks["FOCULOOM"]["owner_name"])
        self.assertEqual("Downloadable mobile operating system software", marks["FOCULOOM"]["goods"])
        self.assertEqual("FILED", marks["SKIPLET"]["state"])
        self.assertEqual("Foculoom LLC", marks["SKIPLET"]["owner_name"])
        self.assertEqual(
            "Downloadable game software; video game programs; computer game programs",
            marks["SKIPLET"]["goods"],
        )
        self.assertEqual("LEGAL_REVIEW_REQUIRED", marks["VEILSORT"]["state"])
        self.assertEqual("Downloadable desktop publishing software", marks["VEILSORT"]["goods"])
        self.assertTrue(all(item["registration_claimed"] is False for item in marks.values()))

    def test_registered_agent_and_role_contacts_match_owner_facts(self):
        self.assertEqual("Northwest Registered Agent, Inc.", self.registry["legal_entity"]["registered_agent_name"])
        self.assertEqual(
            {"hello@foculoom.com", "support@foculoom.com", "billing@foculoom.com"},
            {item["email"] for item in self.registry["contacts"]},
        )

    def test_skiplet_preserves_existing_use_without_inferring_clearance(self):
        skiplet = next(item for item in self.registry["identities"] if item["entity_id"] == "product:skiplet")
        self.assertEqual("ADOPTED", skiplet["identity_state"])
        self.assertEqual("FILED", skiplet["trademark_state"])
        self.assertEqual("PRESERVE", skiplet["existing_use_disposition"])
        self.assertFalse(skiplet["adoption_allowed"])

    def test_every_supplied_domain_is_present(self):
        supplied = {
            "edoworks.com", "foculoom.com", "foculoom.net", "foculoom.org",
            "getskiplet.com", "playskiplet.com", "veilsort.com", "blooplo.com",
            "diffrek.com", "docketloom.com", "dojaaa.com", "drawtobloom.com",
            "edglex.com", "emtosa.com", "findmyloophole.com", "jumpyloo.com",
            "kanyee.com", "lawgaps.com", "legalexception.com", "noraze.com",
            "reliatra.com", "rihanno.com", "taylerr.com", "vorynce.com",
            "weekndd.com", "zendayaa.com",
        }
        self.assertTrue(supplied <= {item["domain"] for item in self.registry["domains"]})


if __name__ == "__main__":
    unittest.main()
