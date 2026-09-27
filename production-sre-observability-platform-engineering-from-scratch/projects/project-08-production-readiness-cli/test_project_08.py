import unittest
from prr_linter import lint_production_readiness

class TestProject08(unittest.TestCase):
    def test_prr_linter_pass(self):
        spec = {
            "health_check_endpoint": "/healthz",
            "metrics_endpoint": "/metrics",
            "resources": {"limits": {"cpu": "1", "memory": "512Mi"}},
            "slo": "99.9%",
            "runbook_url": "https://wiki.corp/runbooks/checkout"
        }
        res = lint_production_readiness(spec)
        self.assertTrue(res["is_ready"])
        self.assertEqual(res["score_percent"], 100.0)

if __name__ == "__main__":
    unittest.main()
