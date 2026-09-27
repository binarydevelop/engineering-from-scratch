#!/usr/bin/env python3
"""
simulations/transmission_delay.py
Calculates and simulates serialization (transmission) delay across network links.
Formula: Transmission Delay = Packet Size (bits) / Link Bandwidth (bps)
"""

from typing import Dict, List, Tuple


def calculate_transmission_delay(size_bytes: int, bandwidth_bps: int) -> float:
    """Calculates transmission delay in seconds."""
    if bandwidth_bps <= 0:
        raise ValueError("Bandwidth must be positive.")
    size_bits = size_bytes * 8
    return size_bits / bandwidth_bps


def compare_link_speeds(size_bytes: int) -> List[Dict[str, float]]:
    """Compares transmission delay across standard Ethernet and WAN link speeds."""
    speeds = [
        ("Dial-up (56 Kbps)", 56 * 1000),
        ("Ethernet (10 Mbps)", 10 * 1000 * 1000),
        ("Fast Ethernet (100 Mbps)", 100 * 1000 * 1000),
        ("Gigabit Ethernet (1 Gbps)", 1000 * 1000 * 1000),
        ("10-Gigabit Ethernet (10 Gbps)", 10 * 1000 * 1000 * 1000),
        ("100-Gigabit Datacenter (100 Gbps)", 100 * 1000 * 1000 * 1000),
    ]
    results = []
    for name, bps in speeds:
        delay_sec = calculate_transmission_delay(size_bytes, bps)
        results.append({
            "link_name": name,
            "bandwidth_bps": bps,
            "delay_seconds": delay_sec,
            "delay_milliseconds": delay_sec * 1000.0,
        })
    return results


def format_delay_table(size_bytes: int) -> str:
    """Generates an ASCII comparison table of serialization times."""
    results = compare_link_speeds(size_bytes)
    lines = [
        f"Transmission Delay for {size_bytes:,} Bytes ({size_bytes / (1024*1024):.2f} MB):",
        "-" * 70,
        f"{'Link Speed':<35} | {'Delay (seconds)':<16} | {'Delay (ms)':<12}",
        "-" * 70,
    ]
    for r in results:
        lines.append(f"{r['link_name']:<35} | {r['delay_seconds']:<16.6f} | {r['delay_milliseconds']:<12.3f}")
    lines.append("-" * 70)
    return "\n".join(lines)


if __name__ == "__main__":
    # Standard prompt scenario: 1 MB over 10 Mbps link
    one_mb = 1024 * 1024  # 1,048,576 bytes
    delay_10mbps = calculate_transmission_delay(one_mb, 10 * 1000 * 1000)
    print(f"1 MB (1,048,576 bytes) over 10 Mbps = {delay_10mbps:.4f} seconds ({delay_10mbps*1000:.1f} ms)")
    print()
    print(format_delay_table(one_mb))
