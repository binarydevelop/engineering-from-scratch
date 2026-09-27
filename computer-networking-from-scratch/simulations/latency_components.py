#!/usr/bin/env python3
"""
simulations/latency_components.py
Calculates and decomposes total network latency into its four physical components:
  1. Processing Delay (d_proc)
  2. Queueing Delay (d_queue)
  3. Transmission (Serialization) Delay (d_trans = L / R)
  4. Propagation Delay (d_prop = d / s)

Formula:
  d_end_to_end = N_hops * (d_proc + d_queue + d_trans + d_prop)
"""

from dataclasses import dataclass
from typing import List


# Speed of light in single-mode fiber optic cable: ~200,000 km/s (2.0 * 10^8 m/s)
SPEED_OF_LIGHT_FIBER_MPS = 200_000_000.0


@dataclass
class NetworkHop:
    name: str
    distance_meters: float
    bandwidth_bps: float
    processing_delay_seconds: float = 0.000010  # 10 microseconds default
    queueing_delay_seconds: float = 0.000100    # 100 microseconds default
    propagation_speed_mps: float = SPEED_OF_LIGHT_FIBER_MPS


@dataclass
class LatencyBreakdown:
    processing_ms: float
    queueing_ms: float
    transmission_ms: float
    propagation_ms: float
    total_one_way_ms: float
    estimated_rtt_ms: float


def compute_hop_latency(hop: NetworkHop, packet_size_bytes: int) -> LatencyBreakdown:
    """Computes the four delay components for a single network hop."""
    trans_sec = (packet_size_bytes * 8) / hop.bandwidth_bps
    prop_sec = hop.distance_meters / hop.propagation_speed_mps
    proc_sec = hop.processing_delay_seconds
    queue_sec = hop.queueing_delay_seconds

    total_one_way_sec = proc_sec + queue_sec + trans_sec + prop_sec

    return LatencyBreakdown(
        processing_ms=proc_sec * 1000.0,
        queueing_ms=queue_sec * 1000.0,
        transmission_ms=trans_sec * 1000.0,
        propagation_ms=prop_sec * 1000.0,
        total_one_way_ms=total_one_way_sec * 1000.0,
        estimated_rtt_ms=total_one_way_sec * 2000.0,
    )


def simulate_path(hops: List[NetworkHop], packet_size_bytes: int) -> LatencyBreakdown:
    """Computes cumulative end-to-end latency across multiple hops."""
    proc = 0.0
    queue = 0.0
    trans = 0.0
    prop = 0.0

    for hop in hops:
        b = compute_hop_latency(hop, packet_size_bytes)
        proc += b.processing_ms
        queue += b.queueing_ms
        trans += b.transmission_ms
        prop += b.propagation_ms

    total = proc + queue + trans + prop
    return LatencyBreakdown(
        processing_ms=proc,
        queueing_ms=queue,
        transmission_ms=trans,
        propagation_ms=prop,
        total_one_way_ms=total,
        estimated_rtt_ms=total * 2.0,
    )


if __name__ == "__main__":
    packet_size = 1500  # Standard MTU size in bytes
    print(f"Latency Decomposition for 1500-Byte Packet:")
    print("=" * 75)

    scenarios = [
        ("Datacenter Intra-Rack (5m fiber, 100 Gbps)", [
            NetworkHop("ToR Switch", 5, 100 * 10**9, 0.000001, 0.000002)
        ]),
        ("Cross-Country NYC -> LA (4,000 km, 10 Gbps, 8 router hops)", [
            NetworkHop(f"Hop {i}", 4_000_000 / 8, 10 * 10**9, 0.000020, 0.000500)
            for i in range(1, 9)
        ]),
        ("Transatlantic NYC -> London (5,600 km, 10 Gbps, 10 router hops)", [
            NetworkHop(f"Hop {i}", 5_600_000 / 10, 10 * 10**9, 0.000020, 0.000400)
            for i in range(1, 11)
        ]),
    ]

    for title, hops in scenarios:
        res = simulate_path(hops, packet_size)
        print(f"\n{title}:")
        print(f"  Processing Delay:   {res.processing_ms:8.3f} ms ({res.processing_ms/res.total_one_way_ms*100:5.1f}%)")
        print(f"  Queueing Delay:     {res.queueing_ms:8.3f} ms ({res.queueing_ms/res.total_one_way_ms*100:5.1f}%)")
        print(f"  Transmission Delay: {res.transmission_ms:8.3f} ms ({res.transmission_ms/res.total_one_way_ms*100:5.1f}%)")
        print(f"  Propagation Delay:  {res.propagation_ms:8.3f} ms ({res.propagation_ms/res.total_one_way_ms*100:5.1f}%)")
        print(f"  --> Total One-Way:  {res.total_one_way_ms:8.3f} ms")
        print(f"  --> Estimated RTT:  {res.estimated_rtt_ms:8.3f} ms (approx. ping time)")
