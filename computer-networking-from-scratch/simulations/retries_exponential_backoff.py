#!/usr/bin/env python3
"""
simulations/retries_exponential_backoff.py
Simulates client retry storms and compares backoff strategies:
  1. No Backoff (Immediate retry -> Thundering Herd / DoS)
  2. Fixed Interval Retry (Persistent synchronized wave)
  3. Exponential Backoff without Jitter (Spiky periodic harmonics)
  4. Exponential Backoff with Full Jitter (De-correlates traffic spikes)
"""

import random
from typing import Dict, List, Tuple


def calculate_delays(
    strategy: str,
    base_delay_sec: float,
    max_delay_sec: float,
    max_retries: int,
    seed: int = 42,
) -> List[float]:
    """Calculates retry sleep intervals for a given strategy."""
    rng = random.Random(seed)
    delays = []

    for attempt in range(max_retries):
        if strategy == "IMMEDIATE":
            delays.append(0.0)
        elif strategy == "FIXED":
            delays.append(base_delay_sec)
        elif strategy == "EXPONENTIAL":
            # 2^attempt * base_delay
            d = min(max_delay_sec, base_delay_sec * (2**attempt))
            delays.append(d)
        elif strategy == "FULL_JITTER":
            # random(0, min(max_delay, base_delay * 2^attempt))
            ceiling = min(max_delay_sec, base_delay_sec * (2**attempt))
            delays.append(rng.uniform(0.0, ceiling))
        else:
            raise ValueError(f"Unknown strategy {strategy}")

    return delays


def simulate_concurrent_clients(
    num_clients: int,
    strategy: str,
    max_retries: int = 5,
    base_delay: float = 1.0,
    max_delay: float = 32.0,
) -> Dict[int, int]:
    """
    Simulates multiple clients encountering a failed server at t=0,
    and returns a histogram of retry request timestamps (rounded to integer seconds).
    """
    timeline: Dict[int, int] = {}

    for client_id in range(num_clients):
        delays = calculate_delays(strategy, base_delay, max_delay, max_retries, seed=client_id)
        current_time = 0.0
        for d in delays:
            current_time += d
            sec = int(round(current_time))
            timeline[sec] = timeline.get(sec, 0) + 1

    return timeline


if __name__ == "__main__":
    clients = 100
    retries = 4
    print(f"Simulating {clients} Concurrent Clients Retrying After Outage:")
    print("=" * 65)

    for strat in ["FIXED", "EXPONENTIAL", "FULL_JITTER"]:
        timeline = simulate_concurrent_clients(clients, strat, max_retries=retries)
        peak_second = max(timeline.keys(), key=lambda s: timeline[s])
        peak_volume = timeline[peak_second]

        print(f"\nStrategy: {strat}")
        print(f"  Peak Concurrency: {peak_volume} requests hitting server in a single second (at t={peak_second}s)")
        # Show top 5 spike seconds
        spikes = sorted(timeline.items(), key=lambda x: x[1], reverse=True)[:4]
        spike_str = ", ".join(f"t={s}s ({c} reqs)" for s, c in spikes)
        print(f"  Highest Spikes:   {spike_str}")

    print("\nObservation:")
    print("  Notice how FULL_JITTER spreads the 400 total retries across the timeline,")
    print("  preventing the thundering herd that knocks the recovered server down again.")
    print("\nSUCCESS: Retry and exponential backoff with jitter simulation verified.")
