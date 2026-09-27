import unittest
from instrumentation.stdlib_metrics import Counter, Gauge, Histogram, SimpleRegistry


class TestStdlibMetrics(unittest.TestCase):
    def test_counter_monotonic_behavior(self):
        c = Counter("test_requests_total", "Test requests")
        c.inc(1.0, labels={"service": "checkout", "status": "200"})
        c.inc(4.0, labels={"service": "checkout", "status": "200"})
        self.assertEqual(c.get(labels={"service": "checkout", "status": "200"}), 5.0)

        with self.assertRaises(ValueError):
            c.inc(-1.0)

    def test_gauge_fluctuation(self):
        g = Gauge("test_active_concurrency", "Test concurrency")
        g.set(10.0, labels={"service": "api"})
        self.assertEqual(g.get(labels={"service": "api"}), 10.0)
        g.inc(5.0, labels={"service": "api"})
        self.assertEqual(g.get(labels={"service": "api"}), 15.0)
        g.dec(3.0, labels={"service": "api"})
        self.assertEqual(g.get(labels={"service": "api"}), 12.0)

    def test_histogram_buckets_and_prometheus_format(self):
        h = Histogram("test_latency_seconds", "Test latency", buckets=[0.01, 0.05, 0.1, 0.5])
        h.observe(0.02, labels={"route": "/orders"})
        h.observe(0.08, labels={"route": "/orders"})
        h.observe(0.30, labels={"route": "/orders"})

        text = h.to_prometheus_text()
        self.assertIn("# TYPE test_latency_seconds histogram", text)
        self.assertIn('test_latency_seconds_bucket{le="0.05",route="/orders"} 1', text)
        self.assertIn('test_latency_seconds_bucket{le="0.1",route="/orders"} 2', text)
        self.assertIn('test_latency_seconds_bucket{le="0.5",route="/orders"} 3', text)
        self.assertIn('test_latency_seconds_count{route="/orders"} 3', text)


if __name__ == "__main__":
    unittest.main()
