import json
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
EXPERIMENT = ROOT / "experiments" / "continuous-competence-mobile"
CORPUS = ROOT / "docs" / "research" / "continuous-competence-ai-skeptic-corpus-2026-09-20.json"


class ContinuousCompetenceMobileContractTests(unittest.TestCase):
    def test_fixture_is_local_and_contains_controlled_defect(self):
        fixture = json.loads((EXPERIMENT / "fixture.json").read_text())
        self.assertEqual(fixture["experiment_id"], "continuous-competence-mobile-v1")
        self.assertIn("defect", fixture["task"])
        self.assertIn("repair", fixture["task"])
        self.assertEqual(fixture["task"]["language"], "scala")
        self.assertGreaterEqual(len(fixture["task"]["test_cases"]), 4)

    def test_surface_has_no_external_runtime_dependencies(self):
        html = (EXPERIMENT / "index.html").read_text()
        css = (EXPERIMENT / "styles.css").read_text()
        js = (EXPERIMENT / "app.js").read_text()
        service_worker = (EXPERIMENT / "sw.js").read_text()
        combined = html + css
        self.assertNotIn("https://", combined)
        self.assertNotIn("fetch(", js)
        self.assertIn("localStorage", js)
        self.assertIn("function sourceLink", js)
        self.assertNotIn("https://", service_worker)
        self.assertIn("caches.open", service_worker)

    def test_installable_mobile_metadata_exists(self):
        html = (EXPERIMENT / "index.html").read_text()
        manifest = (EXPERIMENT / "manifest.webmanifest").read_text()
        self.assertIn('rel="manifest"', html)
        self.assertIn('apple-mobile-web-app-capable', html)
        self.assertIn('"display": "standalone"', manifest)

    def test_both_experimental_modes_are_present(self):
        js = (EXPERIMENT / "app.js").read_text()
        self.assertIn('"CONTROL"', js)
        self.assertIn('"INTERVENTION"', js)
        self.assertIn("confidenceBefore", js)
        self.assertIn("confidenceAfter", js)

    def test_intervention_has_optional_hints_and_explanation(self):
        fixture = json.loads((EXPERIMENT / "fixture.json").read_text())
        js = (EXPERIMENT / "app.js").read_text()
        self.assertGreaterEqual(len(fixture["task"]["hints"]), 3)
        self.assertIn("Show hint 1", js)
        self.assertIn("Show plain-language explanation", js)
        self.assertIn("hintsUsed", js)
        self.assertIn("explanationRevealed", js)

    def test_scala_contract_has_local_test_runner_and_discloses_boundary(self):
        js = (EXPERIMENT / "app.js").read_text()
        readme = (EXPERIMENT / "README.md").read_text()
        self.assertIn('language: "scala"', js)
        self.assertIn("Run test cases", js)
        self.assertIn("function longestRun", js)
        self.assertIn("does not compile arbitrary Scala or SQL source", readme)

    def test_financial_big_data_question_bank_covers_requested_platforms(self):
        fixture = json.loads((EXPERIMENT / "fixture.json").read_text())
        bank = fixture["question_bank"]
        domains = {item["domain"] for item in bank}
        self.assertIn("Apache Spark Structured Streaming", domains)
        self.assertIn("Azure Synapse Analytics", domains)
        self.assertIn("Azure Event Hubs", domains)
        self.assertIn("Azure Data Lake Storage Gen2", domains)
        self.assertIn("Financial data processing", domains)
        self.assertGreaterEqual(sum(item["domain"] == "Software engineering practice" for item in bank), 4)
        self.assertTrue(all(len(item["test_cases"]) >= 4 for item in bank))
        self.assertTrue(all(item["reference"] for item in bank))

    def test_mobile_surface_exposes_question_selection_and_contract_runner(self):
        js = (EXPERIMENT / "app.js").read_text()
        self.assertIn('id="task-select"', js)
        self.assertIn("question_bank", js)
        self.assertIn("function runContract", js)
        self.assertIn("activeTask.test_cases", js)

    def test_mobile_surface_exposes_learning_library_and_references(self):
        js = (EXPERIMENT / "app.js").read_text()
        css = (EXPERIMENT / "styles.css").read_text()
        self.assertIn("Open learning library", js)
        self.assertIn("Visual walkthroughs", js)
        self.assertIn("function sourceLink", js)
        self.assertIn("target=\"_blank\"", js)
        self.assertIn(".learning-library", css)

    def test_native_experiment_declares_light_visual_contract(self):
        swift = (ROOT / "experiments" / "continuous-competence-ios" / "Sources" / "CompetenceCheckApp.swift").read_text()
        self.assertIn("preferredColorScheme(.light)", swift)

    def test_ai_skeptic_corpus_is_balanced_and_decision_consistent(self):
        corpus = json.loads(CORPUS.read_text())
        items = corpus["items"]
        self.assertEqual(len(items), 14)
        self.assertEqual(len({item["id"] for item in items}), len(items))
        self.assertEqual(sum(item["contains_error"] for item in items), 7)
        self.assertEqual(sum(not item["contains_error"] for item in items), 7)
        required = {"id", "defect_family", "contains_error", "prompt", "ai_output", "ground_truth", "expected_decision", "verification_basis"}
        for item in items:
            self.assertTrue(required <= item.keys())
            self.assertEqual(item["expected_decision"], "REJECT" if item["contains_error"] else "ACCEPT")
        self.assertGreaterEqual(len(corpus["source_plan"]), 1)

    def test_ai_skeptic_corpus_records_required_scoring_metrics(self):
        corpus = json.loads(CORPUS.read_text())
        metrics = set(corpus["scoring"]["required_recorded_metrics"])
        self.assertTrue({"decision", "confidence", "decision_time_seconds", "reason", "verification_step", "correction_quality"} <= metrics)


if __name__ == "__main__":
    unittest.main()
