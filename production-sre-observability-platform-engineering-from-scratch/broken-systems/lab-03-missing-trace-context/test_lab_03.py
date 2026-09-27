import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from broken_client import make_outbound_call_broken, make_outbound_call_fixed
from instrumentation.stdlib_tracing import SpanContext


class TestTraceContextPropagation(unittest.TestCase):
    def test_broken_client_fails_context_propagation(self):
        headers = make_outbound_call_broken({"order_id": "123"})
        self.assertNotIn("traceparent", headers, "Broken client should be missing traceparent")

    def test_fixed_client_propagates_w3c_traceparent(self):
        headers = make_outbound_call_fixed({"order_id": "123"})
        self.assertIn("traceparent", headers, "Fixed client must include W3C 'traceparent' header")
        
        # Verify W3C traceparent syntax: 00-{trace_id}-{span_id}-{flags}
        tp = headers["traceparent"]
        context = SpanContext.from_traceparent(tp)
        self.assertIsNotNone(context, "Failed to parse traceparent header")
        self.assertEqual(len(context.trace_id), 32, "Trace ID must be 32 hex characters (16 bytes)")
        self.assertEqual(len(context.span_id), 16, "Span ID must be 16 hex characters (8 bytes)")


if __name__ == "__main__":
    unittest.main()
