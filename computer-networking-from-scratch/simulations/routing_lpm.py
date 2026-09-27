#!/usr/bin/env python3
"""
simulations/routing_lpm.py
Implements the Longest Prefix Match (LPM) routing table lookup algorithm.
Given an arbitrary destination IPv4 address, selects the route with the most
specific network mask (longest prefix length).

Supports:
  - Default route (0.0.0.0/0)
  - Arbitrary CIDR prefixes (/8, /16, /24, /27, etc.)
  - Next hop gateway & outgoing interface selection
"""

import socket
import struct
from dataclasses import dataclass
from typing import List, Optional, Tuple


def ip_to_int(ip_str: str) -> int:
    """Converts dotted-quad string '192.168.1.1' to a 32-bit unsigned integer."""
    packed = socket.inet_aton(ip_str)
    return struct.unpack("!I", packed)[0]


def int_to_ip(ip_int: int) -> str:
    """Converts a 32-bit integer back to dotted-quad string."""
    packed = struct.pack("!I", ip_int)
    return socket.inet_ntoa(packed)


@dataclass
class RouteEntry:
    destination_prefix: str  # e.g. "10.1.2.0/24"
    next_hop: Optional[str]  # e.g. "192.168.1.1" or None for direct link
    interface: str           # e.g. "eth0"
    metric: int = 100

    def __post_init__(self):
        if "/" in self.destination_prefix:
            ip_part, prefix_len_part = self.destination_prefix.split("/")
            self.prefix_len = int(prefix_len_part)
        else:
            ip_part = self.destination_prefix
            self.prefix_len = 32

        if self.prefix_len < 0 or self.prefix_len > 32:
            raise ValueError(f"Invalid prefix length {self.prefix_len}")

        # Compute 32-bit netmask
        if self.prefix_len == 0:
            self.netmask = 0
        else:
            self.netmask = (0xFFFFFFFF << (32 - self.prefix_len)) & 0xFFFFFFFF

        self.network_int = ip_to_int(ip_part) & self.netmask


class RoutingTable:
    def __init__(self):
        self.routes: List[RouteEntry] = []

    def add_route(self, destination_prefix: str, next_hop: Optional[str], interface: str, metric: int = 100) -> None:
        """Adds a route entry to the routing table."""
        entry = RouteEntry(
            destination_prefix=destination_prefix,
            next_hop=next_hop,
            interface=interface,
            metric=metric,
        )
        self.routes.append(entry)

    def lookup(self, dest_ip: str) -> Optional[RouteEntry]:
        """
        Performs Longest Prefix Match (LPM) for dest_ip.
        Returns the matching RouteEntry with the maximum prefix_len.
        Tie-breaker: lowest metric.
        """
        dest_int = ip_to_int(dest_ip)
        best_match: Optional[RouteEntry] = None

        for route in self.routes:
            # Check if destination IP matches this network prefix
            if (dest_int & route.netmask) == route.network_int:
                if best_match is None:
                    best_match = route
                else:
                    # Prefer longer prefix length
                    if route.prefix_len > best_match.prefix_len:
                        best_match = route
                    # Tie-breaker: lower metric
                    elif route.prefix_len == best_match.prefix_len:
                        if route.metric < best_match.metric:
                            best_match = route

        return best_match


if __name__ == "__main__":
    rt = RoutingTable()

    # The exact scenario from the prompt:
    # 10.0.0.0/8
    # 10.1.0.0/16
    # 10.1.2.0/24
    # default (0.0.0.0/0)
    rt.add_route("0.0.0.0/0", "192.168.1.1", "eth0", metric=100)
    rt.add_route("10.0.0.0/8", "10.0.0.1", "eth1", metric=10)
    rt.add_route("10.1.0.0/16", "10.1.0.1", "eth2", metric=10)
    rt.add_route("10.1.2.0/24", None, "eth3", metric=10)  # Direct subnet link

    print("Configured Routing Table:")
    for r in rt.routes:
        print(f"  {r.destination_prefix:<15} via {str(r.next_hop):<15} dev {r.interface}")
    print("=" * 65)

    test_ips = [
        ("10.1.2.50", "10.1.2.0/24", "eth3", "Direct subnet link"),
        ("10.1.5.88", "10.1.0.0/16", "eth2", "/16 matches, /24 does not"),
        ("10.99.1.1", "10.0.0.0/8",  "eth1", "/8 matches"),
        ("8.8.8.8",   "0.0.0.0/0",   "eth0", "Default route fallback"),
    ]

    for ip, expected_prefix, expected_iface, note in test_ips:
        match = rt.lookup(ip)
        assert match is not None
        print(f"Destination: {ip:<15} -> Route: {match.destination_prefix:<12} (NextHop: {match.next_hop}) Dev: {match.interface}")
        assert match.destination_prefix == expected_prefix, f"Expected {expected_prefix}, got {match.destination_prefix}"
        assert match.interface == expected_iface, f"Expected {expected_iface}, got {match.interface}"

    print("\nSUCCESS: Longest Prefix Match (LPM) verified.")
