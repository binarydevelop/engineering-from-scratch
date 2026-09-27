import os
import sys
import unittest
import importlib.util

evaluator_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "platform", "scorecards", "evaluator.py"))
spec = importlib.util.spec_from_file_location("platform_scorecards_evaluator", evaluator_path)
evaluator_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(evaluator_mod)
evaluate_service_directory = evaluator_mod.evaluate_service_directory


class TestPlatformEvaluator(unittest.TestCase):
    def test_scorecard_evaluation_api_gateway(self):
        res = evaluate_service_directory("services/api-gateway")
        self.assertNotIn("error", res)
        self.assertIn("score_percent", res)
        self.assertIn("grade", res)
        self.assertTrue(res["checks"]["health_probes"])
        self.assertTrue(res["checks"]["metrics_endpoint"])
        self.assertTrue(res["checks"]["structured_logging"])


if __name__ == "__main__":
    unittest.main()
