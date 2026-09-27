"""
Benchmark: Synchronous Sequential I/O vs Asynchronous Event-Loop Concurrency.
Simulates 50 concurrent network calls with 10ms simulated I/O latency.
"""

import time
import asyncio
from typing import Dict, Any

def run_sync_work(count: int = 20, delay_sec: float = 0.005) -> float:
    start = time.perf_counter()
    for _ in range(count):
        time.sleep(delay_sec)
    return time.perf_counter() - start

async def async_task(delay_sec: float):
    await asyncio.sleep(delay_sec)

async def run_async_work(count: int = 20, delay_sec: float = 0.005) -> float:
    start = time.perf_counter()
    tasks = [async_task(delay_sec) for _ in range(count)]
    await asyncio.gather(*tasks)
    return time.perf_counter() - start

def benchmark() -> Dict[str, Any]:
    count = 25
    delay = 0.005
    sync_time = run_sync_work(count, delay)
    async_time = asyncio.run(run_async_work(count, delay))
    speedup = sync_time / async_time if async_time > 0 else 1.0

    return {
        "name": "Sync vs Async Concurrency (I/O Bound)",
        "tasks": count,
        "sync_time_sec": round(sync_time, 4),
        "async_time_sec": round(async_time, 4),
        "speedup_ratio": round(speedup, 2)
    }

if __name__ == "__main__":
    res = benchmark()
    print(f"[{res['name']}]")
    print(f"  Sync:  {res['sync_time_sec']}s")
    print(f"  Async: {res['async_time_sec']}s")
    print(f"  Speedup: {res['speedup_ratio']}x")
