#!/usr/bin/env python3
"""
CPU Saturation Chaos Tool.

Generates 100% CPU burn across available cores with mandatory automated timeout.
Adheres strictly to SAFETY.md invariants.
"""

import argparse
import multiprocessing
import time
import os
import signal


def burn_cpu(stop_time: float):
    # Tight loop computing hashes or primes to burn CPU
    while time.time() < stop_time:
        _ = [x**2 for x in range(1000)]


def main():
    parser = argparse.ArgumentParser(description="Controlled CPU Saturation Harness")
    parser.add_argument("--duration", type=int, default=15, help="Duration in seconds (enforced timeout)")
    parser.add_argument("--cores", type=int, default=multiprocessing.cpu_count(), help="Number of cores to saturate")

    args = parser.parse_args()
    print("=========================================================================")
    print(f" [SAFETY INVARIANT] Starting CPU Burn on {args.cores} cores for {args.duration}s")
    print(f" Automated abort guaranteed after {args.duration} seconds.")
    print("=========================================================================")

    stop_time = time.time() + args.duration
    processes = []
    
    for _ in range(args.cores):
        p = multiprocessing.Process(target=burn_cpu, args=(stop_time,))
        p.start()
        processes.append(p)

    try:
        for p in processes:
            p.join(timeout=args.duration + 2)
    except KeyboardInterrupt:
        print("\nManual abort received. Terminating workers...")
    finally:
        for p in processes:
            if p.is_alive():
                p.terminate()
        print("[SAFETY] CPU Burn stopped. System returning to baseline.")


if __name__ == "__main__":
    main()
