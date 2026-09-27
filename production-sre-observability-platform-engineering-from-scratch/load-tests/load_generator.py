#!/usr/bin/env python3
"""
Asynchronous Production Load Generator & Tail Latency Analyzer.

Generates realistic concurrent HTTP workloads with configurable arrival rates,
skewed payload distributions, and computes exact quantile distributions (p50, p95, p99, p99.9).
"""

import argparse
import asyncio
import random
import time
import math
import httpx
from typing import List, Dict, Any


async def send_checkout_request(client: httpx.AsyncClient, gateway_url: str, request_idx: int) -> Dict[str, Any]:
    """Generates a realistic checkout request and measures round-trip latency."""
    user_id = f"user_{random.randint(1000, 9999)}"
    num_items = random.choices([1, 2, 5, 10], weights=[70, 20, 8, 2])[0]
    
    items = [
        {
            "product_id": f"item_{random.choice(['101', '102', '103'])}",
            "quantity": random.randint(1, 3),
            "unit_price": round(random.uniform(10.0, 99.0), 2)
        }
        for _ in range(num_items)
    ]
    total_amount = round(sum(i["quantity"] * i["unit_price"] for i in items), 2)

    payload = {
        "user_id": user_id,
        "items": items,
        "payment_token": f"tok_{user_id}_{int(time.time())}",
        "total_amount": total_amount
    }

    t0 = time.time()
    try:
        resp = await client.post(
            f"{gateway_url}/api/v1/checkout",
            json=payload,
            headers={"x-correlation-id": f"corr_load_{request_idx}_{int(time.time()*1000)}"}
        )
        duration_ms = (time.time() - t0) * 1000.0
        return {
            "status_code": resp.status_code,
            "duration_ms": duration_ms,
            "success": 200 <= resp.status_code < 400
        }
    except Exception as e:
        duration_ms = (time.time() - t0) * 1000.0
        return {
            "status_code": 0,
            "duration_ms": duration_ms,
            "success": False,
            "error": str(e)
        }


async def run_load_test(gateway_url: str, target_rps: int, duration_sec: int, max_concurrency: int):
    print("=========================================================================")
    print(f" STARTING LOAD GENERATOR: {target_rps} RPS for {duration_sec}s (Max Concurrency: {max_concurrency})")
    print(f" Target: {gateway_url}")
    print("=========================================================================")

    limits = httpx.Limits(max_keepalive_connections=max_concurrency, max_connections=max_concurrency)
    timeout = httpx.Timeout(10.0)
    
    results: List[Dict[str, Any]] = []
    start_time = time.time()
    total_requests_sent = 0

    async with httpx.AsyncClient(limits=limits, timeout=timeout) as client:
        while time.time() - start_time < duration_sec:
            batch_start = time.time()
            tasks = []
            
            for _ in range(target_rps):
                total_requests_sent += 1
                tasks.append(send_checkout_request(client, gateway_url, total_requests_sent))
                
            batch_results = await asyncio.gather(*tasks)
            results.extend(batch_results)

            elapsed = time.time() - batch_start
            sleep_needed = max(0.0, 1.0 - elapsed)
            await asyncio.sleep(sleep_needed)

    total_time = time.time() - start_time
    total_samples = len(results)
    if total_samples == 0:
        print("No samples gathered.")
        return

    durations = sorted([r["duration_ms"] for r in results])
    success_count = sum(1 for r in results if r["success"])
    failure_count = total_samples - success_count

    p50 = durations[int(len(durations) * 0.50)]
    p90 = durations[int(len(durations) * 0.90)]
    p95 = durations[int(len(durations) * 0.95)]
    p99 = durations[int(len(durations) * 0.99)]
    p999 = durations[int(len(durations) * 0.999)]

    effective_rps = total_samples / total_time

    status_codes: Dict[int, int] = {}
    for r in results:
        status_codes[r["status_code"]] = status_codes.get(r["status_code"], 0) + 1

    print("\n=========================================================================")
    print("                      LOAD TEST EMPIRICAL RESULTS                        ")
    print("=========================================================================")
    print(f" Total Requests Completed: {total_samples:,} in {total_time:.2f}s")
    print(f" Effective Throughput:     {effective_rps:.1f} req/sec")
    print(f" Success Rate:             {(success_count / total_samples)*100:.2f}% ({success_count} success, {failure_count} errors)")
    print("-------------------------------------------------------------------------")
    print(" Latency Percentiles (Duration Round-Trip):")
    print(f"   - Minimum:              {durations[0]:.2f} ms")
    print(f"   - p50 (Median):         {p50:.2f} ms")
    print(f"   - p90:                  {p90:.2f} ms")
    print(f"   - p95:                  {p95:.2f} ms")
    print(f"   - p99 (Tail):           {p99:.2f} ms")
    print(f"   - p99.9 (Extreme Tail): {p999:.2f} ms")
    print(f"   - Maximum:              {durations[-1]:.2f} ms")
    print("-------------------------------------------------------------------------")
    print(" Status Code Breakdown:")
    for code, count in sorted(status_codes.items()):
        status_name = f"HTTP {code}" if code > 0 else "Connection/Timeout Error"
        print(f"   - {status_name}: {count:,} ({count/total_samples*100:.1f}%)")
    print("=========================================================================\n")


def main():
    parser = argparse.ArgumentParser(description="Async Production Load Generator")
    parser.add_argument("--gateway-url", type=str, default="http://localhost:8000", help="API Gateway URL")
    parser.add_argument("--rps", type=int, default=20, help="Target Requests Per Second")
    parser.add_argument("--duration", type=int, default=10, help="Duration in seconds")
    parser.add_argument("--concurrency", type=int, default=50, help="Max connection pool concurrency")
    parser.add_argument("--scenario", type=str, default="steady_state", help="Scenario profile name")

    args = parser.parse_args()
    asyncio.run(run_load_test(args.gateway_url, args.rps, args.duration, args.concurrency))


if __name__ == "__main__":
    main()
