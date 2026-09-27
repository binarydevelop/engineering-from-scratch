import unittest
from alert_compiler import compile_alert_rule

class TestProject05(unittest.TestCase):
    def test_compile_alert(self):
        rule = compile_alert_rule("HighErrorRate", "http_errors_total", 10.0, "2m", "critical")
        self.assertEqual(rule["labels"]["severity"], "critical")
        self.assertEqual(rule["for"], "2m")

if __name__ == "__main__":
    unittest.main()
