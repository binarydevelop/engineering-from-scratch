import unittest
import time
from instrumentation.stdlib_tracing import SimpleTracer, SpanContext


class TestStdlibTracing(unittest.TestCase):
    def setUp(self):
        self.tracer = SimpleTracer("test-service")

    def test_span_context_w3c_serialization(self):
        ctx = SpanContext("4bf92f3577b34da6a3ce929d0e0e4736", "00f067aa0ba902b7", sampled=True)
        tp = ctx.to_traceparent()
        self.assertEqual(tp, "00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01")

        parsed = SpanContext.from_traceparent(tp)
        self.assertIsNotNone(parsed)
        self.assertEqual(parsed.trace_id, "4bf92f3577b34da6a3ce929d0e0e4736")
        self.assertEqual(parsed.span_id, "00f067aa0ba902b7")
        self.assertTrue(parsed.sampled)

    def test_span_hierarchy_and_duration(self):
        with self.tracer.start_span("root_operation") as root:
            root.set_attribute("http.route", "/api/v1/checkout")
            time.sleep(0.01) # 10ms
            
            with self.tracer.start_span("child_operation") as child:
                child.set_attribute("db.system", "postgresql")
                time.sleep(0.01) # 10ms
                
                self.assertEqual(child.parent_span_id, root.context.span_id)
                self.assertEqual(child.context.trace_id, root.context.trace_id)

        self.assertGreaterEqual(root.duration_ms, 15.0)
        self.assertEqual(root.status, "OK")
        self.assertEqual(child.status, "OK")


if __name__ == "__main__":
    unittest.main()
