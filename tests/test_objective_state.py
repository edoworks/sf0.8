import unittest

from scripts.objective_notification import notification_result
from scripts.objective_state import evaluate


def rung_record():
    stages = (
        "IMPLEMENTATION",
        "LOCAL_VALIDATION",
        "BRANCH_PUSH",
        "PR",
        "REQUIRED_REVIEW",
        "MERGE",
        "DEPLOYMENT",
        "LIVE_HTTP_CHECK",
        "CANONICAL_ROUTING",
    )
    return {
        "external": True,
        "task_execution_complete": True,
        "required_stages": list(stages),
        "stage_evidence": {stage: {"status": "VERIFIED"} for stage in stages},
    }


class ObjectiveStateTests(unittest.TestCase):
    def test_rung_branch_push_is_not_objective_complete(self):
        record = rung_record()
        record["stage_evidence"].pop("PR")
        result = evaluate(record)
        self.assertEqual(result["state"], "TASK_EXECUTION_COMPLETE")
        self.assertFalse(result["objective_complete"])
        self.assertEqual(notification_result(record)[0], "blocked")

    def test_human_boundary_is_not_objective_complete(self):
        record = rung_record()
        record["state"] = "HUMAN_AUTHORIZATION_REQUIRED"
        self.assertEqual(evaluate(record)["state"], "HUMAN_AUTHORIZATION_REQUIRED")
        self.assertEqual(notification_result(record)[0], "blocked")

    def test_all_external_stages_are_required_for_completion(self):
        result = evaluate(rung_record())
        self.assertEqual(result["state"], "OBJECTIVE_COMPLETE")
        self.assertTrue(result["objective_complete"])
        self.assertEqual(notification_result(rung_record())[0], "completed")
