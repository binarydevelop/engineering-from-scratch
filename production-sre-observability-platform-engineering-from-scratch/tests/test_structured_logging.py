import json
import logging
import unittest
from instrumentation.structured_logging import (
    JSONFormatter,
    set_request_context,
    clear_request_context,
    redact_sensitive_info
)


class TestStructuredLogging(unittest.TestCase):
    def test_pii_redaction(self):
        text = "Customer card 4532-1234-5678-9010 paid via user@example.com with password: 'secret_pass_123'"
        redacted = redact_sensitive_info(text)
        self.assertNotIn("4532-1234-5678-9010", redacted)
        self.assertNotIn("user@example.com", redacted)
        self.assertNotIn("secret_pass_123", redacted)
        self.assertIn("[REDACTED_CREDIT_CARD]", redacted)
        self.assertIn("[REDACTED_EMAIL]", redacted)

    def test_json_formatting_with_trace_context(self):
        formatter = JSONFormatter(service_name="test-checkout", environment="production")
        set_request_context(correlation_id="corr_test_99", trace_id="trace_abc123", span_id="span_def456")

        record = logging.LogRecord(
            name="test_logger",
            level=logging.ERROR,
            pathname=__file__,
            lineno=25,
            msg="Payment service connection timed out",
            args=(),
            exc_info=None
        )

        formatted_json = formatter.format(record)
        data = json.loads(formatted_json)

        self.assertEqual(data["service"], "test-checkout")
        self.assertEqual(data["level"], "ERROR")
        self.assertEqual(data["correlation_id"], "corr_test_99")
        self.assertEqual(data["trace_id"], "trace_abc123")
        self.assertEqual(data["span_id"], "span_def456")
        self.assertIn("timestamp", data)

        clear_request_context()


if __name__ == "__main__":
    unittest.main()
