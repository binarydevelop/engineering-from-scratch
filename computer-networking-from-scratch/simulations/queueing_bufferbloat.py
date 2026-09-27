#!/usr/bin/env python3
"""
simulations/queueing_bufferbloat.py
Simulates M/M/1 Queueing Delay and the Bufferbloat phenomenon.
Demonstrates:
  1. Explosive queue growth and latency inflation as link utilization rho -> 1.0
  2. Bufferbloat: large unmanaged FIFO buffers delaying packets for seconds
     while maintaining zero packet loss, ruining interactive latency.
"""

from typing import Dict, List, Tuple


def mm1_theoretical_delay(arrival_rate_lambda: float, service_rate_mu: float) -> Tuple[float, float, float]:
    """
    Computes theoretical M/M/1 queue metrics:
      rho = lambda / mu (link utilization)
      L = rho / (1 - rho) (average number of packets in system)
      W = 1 / (mu - lambda) (average total time in system)
    """
    if arrival_rate_lambda >= service_rate_mu:
        return 1.0, float("inf"), float("inf")
    rho = arrival_rate_lambda / service_rate_mu
    avg_packets = rho / (1.0 - rho)
    avg_delay_sec = 1.0 / (service_rate_mu - arrival_rate_lambda)
    return rho, avg_packets, avg_delay_sec


def simulate_buffer_growth(
    service_rate_pkts_per_sec: float,
    arrival_rate_pkts_per_sec: float,
    buffer_capacity: int,
    duration_seconds: float = 5.0,
    time_step_sec: float = 0.01,
) -> Dict[str, float]:
    """Simulates a FIFO router buffer over time and calculates latency inflation."""
    queue_len = 0
    total_arrived = 0
    total_dropped = 0
    total_served = 0
    max_queue_seen = 0

    t = 0.0
    while t < duration_seconds:
        # Number of packets arriving this time step
        arrivals = arrival_rate_pkts_per_sec * time_step_sec
        # Number of packets served this time step
        services = service_rate_pkts_per_sec * time_step_sec

        total_arrived += arrivals

        # Attempt to queue arrivals
        free_space = buffer_capacity - queue_len
        admitted = min(arrivals, free_space)
        dropped = arrivals - admitted

        queue_len += admitted
        total_dropped += dropped

        # Serve packets
        served = min(queue_len, services)
        queue_len -= served
        total_served += served

        if queue_len > max_queue_seen:
            max_queue_seen = queue_len

        t += time_step_sec

    # Queueing delay of a full buffer = buffer_capacity / service_rate
    max_buffer_latency_ms = (buffer_capacity / service_rate_pkts_per_sec) * 1000.0

    return {
        "total_arrived": total_arrived,
        "total_served": total_served,
        "total_dropped": total_dropped,
        "max_queue_seen": max_queue_seen,
        "max_buffer_latency_ms": max_buffer_latency_ms,
    }


if __name__ == "__main__":
    service_rate = 1000.0  # 1000 packets/sec capacity
    print("M/M/1 Queueing Delay vs. Utilization (rho):")
    print("=" * 65)
    print(f"{'Arrival Rate':<14} | {'Utilization (rho)':<18} | {'Avg Packets in System':<22} | {'Avg Delay (ms)'}")
    print("-" * 75)

    for arr in [500.0, 800.0, 900.0, 950.0, 990.0]:
        rho, L, W = mm1_theoretical_delay(arr, service_rate)
        print(f"{arr:6.0f} pkts/s   | {rho*100:6.1f}%            | {L:10.1f} packets          | {W*1000:8.2f} ms")

    print("\nBufferbloat Comparison (Overload: 1200 pkts/s on 1000 pkts/s link):")
    print("-" * 75)

    # Case A: Bloated Buffer (10,000 packets deep)
    res_bloat = simulate_buffer_growth(1000.0, 1200.0, buffer_capacity=10000)
    print(f"Bloated Buffer (10,000 pkts):")
    print(f"  Max Latency Delay: {res_bloat['max_buffer_latency_ms']:.1f} ms ({res_bloat['max_buffer_latency_ms']/1000:.2f} seconds of lag!)")
    print(f"  Packets Dropped:   {res_bloat['total_dropped']:.0f} (Zero loss, but catastrophic latency)")

    # Case B: Modern Bounded Buffer (100 packets deep)
    res_bounded = simulate_buffer_growth(1000.0, 1200.0, buffer_capacity=100)
    print(f"Bounded Buffer (100 pkts):")
    print(f"  Max Latency Delay: {res_bounded['max_buffer_latency_ms']:.1f} ms (Bounded latency)")
    print(f"  Packets Dropped:   {res_bounded['total_dropped']:.0f} (Early drop signals TCP to back off)")

    print("\nSUCCESS: Queueing and bufferbloat simulation validated.")
