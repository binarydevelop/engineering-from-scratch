#!/usr/bin/env python3
"""
Controlled Progressive Memory Leak Simulation.

Allocates memory chunks steadily to observe telemetry, alerts, and cgroup limits
with a strictly enforced ceiling to avoid uncontrolled host disruption.
"""

import argparse
import time
import sys


def simulate_leak(rate_mb_per_sec: int, max_limit_mb: int, duration_sec: int):
    print("=========================================================================")
    print(f" [CHAOS] Simulating memory allocation: {rate_mb_per_sec} MB/s")
    print(f" Strict safety ceiling: {max_limit_mb} MB | Maximum duration: {duration_sec}s")
    print("=========================================================================")

    blocks = []
    total_allocated_mb = 0
    start_time = time.time()

    try:
        while time.time() - start_time < duration_sec:
            if total_allocated_mb + rate_mb_per_sec > max_limit_mb:
                print(f"[SAFETY CEILING REACHED] Allocated {total_allocated_mb} MB. Holding for observation...")
                time.sleep(max(0.0, duration_sec - (time.time() - start_time)))
                break

            # Allocate 1MB chunks of bytearray
            chunk = bytearray(1024 * 1024 * rate_mb_per_sec)
            blocks.append(chunk)
            total_allocated_mb += rate_mb_per_sec
            print(f"  -> Allocated: {total_allocated_mb} MB (Elapsed: {time.time()-start_time:.1f}s)")
            time.sleep(1.0)
    except KeyboardInterrupt:
        print("\nManual abort received.")
    finally:
        print("Releasing all allocated memory...")
        del blocks
        print("[SAFETY] Memory released. Returning to clean state.")


def main():
    parser = argparse.ArgumentParser(description="Controlled Memory Leak Simulator")
    parser.add_argument("--rate-mb", type=int, default=20, help="Allocation rate in MB per second")
    parser.add_argument("--max-mb", type=int, default=256, help="Strict safety limit in MB")
    parser.add_argument("--duration", type=int, default=15, help="Total simulation duration in seconds")

    args = parser.parse_args()
    simulate_leak(args.rate_mb, args.max_mb, args.duration)


if __name__ == "__main__":
    main()
