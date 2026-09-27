import unittest
from service import TelemetryMiddleware

class TestProject01(unittest.TestCase):
    def test_telemetry_and_trace_injection(self):
        mw = TelemetryMiddleware()
        res = mw.handle_request("GET", "/checkout", {}, lambda: "success")
        self.assertEqual(res["status"], 200)
        self.assertTrue(res["traceparent"].startswith("00-"))
        self.assertEqual(mw.request_count, 1)
        self.assertEqual(mw.error_count, 0)

    def test_error_handling(self):
        mw = TelemetryMiddleware()
        def fail(): raise ValueError("DB failed")
        res = mw.handle_request("POST", "/pay", {}, fail)
        self.assertEqual(res["status"], 500)
        self.assertEqual(mw.error_count, 1)

if __name__ == "__main__":
    unittest.main()
