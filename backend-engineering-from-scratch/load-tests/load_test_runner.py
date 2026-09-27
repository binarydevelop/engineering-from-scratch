"""
Asynchronous Load Test Runner.
Executes concurrent requests, records latency histograms, and reports RPS and percentiles.
"""

import time
import asyncio
from typing import Callable, List, Dict, Any

class LoadTestReport:
    def __init__(self, total_requests: int, duration_sec: float, latencies: List[float], status_codes: Dict[int, int]):
        self.total_requests = total_requests
        self.duration_sec = duration_sec
        self.latencies = sorted(latencies)
        self.status_codes = status_codes
        self.rps = round(total_requests / duration_sec, 2) if duration_sec > 0 else 0.0

    def percentile(self, p: float) -> float:
        if not self.latencies:
            return 0.0
        idx = int(p * len(self.latencies))
        idx = min(idx, len(self.latencies) - 1)
        return round(self.latencies[idx] * 1000, 2)  # In milliseconds

    def summary(self) -> Dict[str, Any]:
        return {
            "total_requests": self.total_requests,
            "duration_sec": round(self.duration_sec, 3),
            "requests_per_sec": self.rps,
            "latency_p50_ms": self.percentile(0.50),
            "latency_p90_ms": self.percentile(0.90),
            "latency_p95_ms": self.percentile(0.95),
            "latency_p99_ms": self.percentile(0.99),
            "status_codes": self.status_codes
        }

    def print_summary(self, scenario_name: str = "Load Test"):
        s = self.summary()
        print("=" * 60)
        print(f"Scenario: {scenario_name}")
        print("=" * 60)
        print(f"Total Requests:     {s['total_requests']}")
        print(f"Total Duration:     {s['duration_sec']} s")
        print(f"Throughput (RPS):   {s['requests_per_sec']} req/sec")
        print(f"Latency p50:        {s['latency_p50_ms']} ms")
        print(f"Latency p90:        {s['latency_p90_ms']} ms")
        print(f"Latency p95:        {s['latency_p95_ms']} ms")
        print(f"Latency p99:        {s['latency_p99_ms']} ms")
        print(f"Status Codes:       {s['status_codes']}")
        print("=" * 60)

class LoadTestRunner:
    def __init__(self, concurrency: int = 20, total_requests: int = 200):
        self.concurrency = concurrency
        self.total_requests = total_requests

    async def run(self, request_fn: Callable[[], Any]) -> LoadTestReport:
        queue = asyncio.Queue()
        for i in range(self.total_requests):
            queue.put_nowait(i)

        latencies: List[float] = []
        status_codes: Dict[int, int] = {}
        lock = asyncio.Lock()

        async def worker():
            while not queue.empty():
                try:
                    _ = queue.get_nowait()
                except asyncio.QueueEmpty:
                    break

                t0 = time.perf_counter()
                try:
                    code = await request_fn()
                except Exception:
                    code = 500
                t1 = time.perf_counter()

                async with lock:
                    latencies.append(t1 - t0)
                    status_codes[code] = status_codes.get(code, 0) + 1
                queue.task_done()

        start_time = time.perf_counter()
        workers = [asyncio.create_task(worker()) for _ in range(self.concurrency)]
        await asyncio.gather(*workers)
        duration = time.perf_counter() - start_time

        return LoadTestReport(self.total_requests, duration, latencies, status_codes)
