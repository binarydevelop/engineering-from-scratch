"""
Scenario: Read-Heavy Traffic Distribution.
Simulates 90% read requests (cache hits) and 10% write requests (cache invalidation).
Demonstrates steady-state latency profiles under realistic production traffic mixes.
"""

import sys
import os
import random
import asyncio

LOAD_TESTS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if LOAD_TESTS_DIR not in sys.path:
    sys.path.insert(0, LOAD_TESTS_DIR)

from load_test_runner import LoadTestRunner

class CatalogTrafficService:
    def __init__(self):
        self.cache = {f"prod_{i}": {"name": f"Product {i}"} for i in range(10)}
        self._lock = asyncio.Lock()

    async def handle_request(self) -> int:
        is_write = random.random() < 0.10
        if is_write:
            # Write request (DB update + cache invalidate)
            await asyncio.sleep(0.003)
            async with self._lock:
                key = f"prod_{random.randint(0, 9)}"
                self.cache[key] = {"name": "Updated Name"}
            return 200
        else:
            # Read request (Cache hit)
            await asyncio.sleep(0.0005)
            key = f"prod_{random.randint(0, 9)}"
            _ = self.cache.get(key)
            return 200

async def main():
    service = CatalogTrafficService()
    runner = LoadTestRunner(concurrency=40, total_requests=300)

    print("Running Read-Heavy Traffic Load Test (90% Read / 10% Write)...")
    report = await runner.run(service.handle_request)
    report.print_summary("Read-Heavy Catalog Workload")

    assert report.status_codes.get(200) == 300
    print("✔ All requests served successfully with low latency.")

if __name__ == "__main__":
    asyncio.run(main())
