import unittest
from pipeline_validator import validate_collector_config

class TestProject02(unittest.TestCase):
    def test_valid_collector_config(self):
        config = {
            "processors": {
                "memory_limiter": {"check_interval": "1s", "limit_percentage": 75},
                "batch": {"timeout": "1s", "send_batch_size": 8192}
            },
            "service": {
                "pipelines": {
                    "traces": {"processors": ["memory_limiter", "batch"]}
                }
            }
        }
        errors = validate_collector_config(config)
        self.assertEqual(len(errors), 0)

    def test_missing_memory_limiter(self):
        config = {"processors": {}, "service": {"pipelines": {"traces": {}}}}
        errors = validate_collector_config(config)
        self.assertTrue(any("memory_limiter" in e for e in errors))

if __name__ == "__main__":
    unittest.main()
