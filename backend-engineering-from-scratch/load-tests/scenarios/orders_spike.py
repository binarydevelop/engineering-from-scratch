"""
Scenario: Orders Flash-Sale Spike.
Simulates 200 concurrent requests competing for 20 units of inventory.
Verifies atomic isolation: exactly 20 orders succeed, 180 return out-of-stock, 0 oversells.
"""

import sys
import os
import asyncio

LOAD_TESTS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_ROOT = os.path.dirname(LOAD_TESTS_DIR)
if LOAD_TESTS_DIR not in sys.path:
    sys.path.insert(0, LOAD_TESTS_DIR)

from load_test_runner import LoadTestRunner

class FlashSaleService:
    def __init__(self, initial_stock: int = 20):
        self.stock = initial_stock
        self.orders = []
        self._lock = asyncio.Lock()

    async def order(self) -> int:
        # Simulate small I/O delay (e.g. 1ms)
        await asyncio.sleep(0.001)
        async with self._lock:
            if self.stock > 0:
                self.stock -= 1
                self.orders.append(len(self.orders) + 1)
                return 201
            return 400

async def main():
    service = FlashSaleService(initial_stock=20)
    runner = LoadTestRunner(concurrency=30, total_requests=200)

    print("Running Orders Spike Load Test...")
    report = await runner.run(service.order)
    report.print_summary("Flash-Sale Inventory Contention")

    # Assert correctness
    assert service.stock == 0, f"Expected 0 stock remaining, got {service.stock}"
    assert len(service.orders) == 20, f"Expected exactly 20 orders, got {len(service.orders)}"
    assert report.status_codes.get(201) == 20, "Expected 20 successful orders (201)"
    assert report.status_codes.get(400) == 180, "Expected 180 out-of-stock rejections (400)"
    print("✔ Transactional integrity preserved: 0 oversold items.")

if __name__ == "__main__":
    asyncio.run(main())
