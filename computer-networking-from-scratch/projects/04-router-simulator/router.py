#!/usr/bin/env python3
"""
projects/04-router-simulator/router.py
Simulates a multi-homed IPv4 router performing:
  1. Layer-2 frame decapsulation
  2. TTL validation and decrement (ICMP Time Exceeded if TTL <= 1)
  3. Longest Prefix Match (LPM) routing table lookup
  4. IPv4 header checksum recalculation
  5. Next-hop ARP neighbor resolution
  6. Layer-2 frame rewrite and forwarding
"""

import socket
import struct
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from simulations.routing_lpm import RoutingTable, RouteEntry
from simulations.encapsulation import encapsulate, decapsulate, compute_ip_checksum


@dataclass
class RouterInterface:
    name: str
    ip_address: str
    mac_address: str
    subnet_prefix: str


class RouterSimulator:
    def __init__(self):
        self.interfaces: Dict[str, RouterInterface] = {}
        self.routing_table = RoutingTable()
        self.arp_cache: Dict[str, str] = {}  # IP -> MAC

    def add_interface(self, name: str, ip: str, mac: str, subnet_prefix: str):
        iface = RouterInterface(name, ip, mac, subnet_prefix)
        self.interfaces[name] = iface
        # Add connected subnet directly to routing table
        self.routing_table.add_route(subnet_prefix, None, name, metric=0)
        # Add local interface to ARP cache
        self.arp_cache[ip] = mac

    def add_static_route(self, prefix: str, next_hop: str, interface: str, metric: int = 10):
        self.routing_table.add_route(prefix, next_hop, interface, metric)

    def set_neighbor_arp(self, ip: str, mac: str):
        self.arp_cache[ip] = mac

    def forward_frame(self, ingress_iface: str, raw_frame: bytes) -> Tuple[str, Optional[str], Optional[bytes]]:
        """
        Processes and forwards an incoming Ethernet frame.
        Returns: (status: str, egress_interface: Optional[str], forwarded_frame: Optional[bytes])
        """
        # Step 1: Decapsulate L2 frame
        d = decapsulate(raw_frame)

        # Step 2: Validate TTL
        if d.ttl <= 1:
            return "ICMP_TIME_EXCEEDED_TTL_EXPIRED", None, None

        # Step 3: Route Lookup via Longest Prefix Match
        route = self.routing_table.lookup(d.dst_ip)
        if not route:
            return "ICMP_DESTINATION_UNREACHABLE_NO_ROUTE", None, None

        egress_iface = route.interface
        if egress_iface not in self.interfaces:
            return "ROUTING_ERROR_UNKNOWN_INTERFACE", None, None

        router_egress = self.interfaces[egress_iface]

        # Step 4: Determine next-hop IP for Layer 2 resolution
        next_hop_ip = route.next_hop if route.next_hop else d.dst_ip

        # Step 5: Neighbor ARP resolution
        if next_hop_ip not in self.arp_cache:
            return f"ARP_RESOLUTION_FAILED_FOR_{next_hop_ip}", None, None

        next_hop_mac = self.arp_cache[next_hop_ip]

        # Step 6: Re-encapsulate with decremented TTL and rewritten MACs
        forwarded = encapsulate(
            src_mac=router_egress.mac_address,
            dst_mac=next_hop_mac,
            src_ip=d.src_ip,      # IP addresses remain unchanged end-to-end!
            dst_ip=d.dst_ip,
            src_port=d.src_port,
            dst_port=d.dst_port,
            payload=d.application_payload,
            seq=d.tcp_seq,
            ack=d.tcp_ack,
            flags=d.tcp_flags,
        )

        # Decrement TTL manually in wire bytes (offset 14 + 8 = offset 22)
        frame_ba = bytearray(forwarded)
        new_ttl = d.ttl - 1
        frame_ba[22] = new_ttl

        # Recalculate IP checksum (offset 14 + 10 = offset 24)
        frame_ba[24] = 0
        frame_ba[25] = 0
        ip_header = bytes(frame_ba[14:34])
        new_checksum = compute_ip_checksum(ip_header)
        struct.pack_into("!H", frame_ba, 24, new_checksum)

        return "FORWARDED", egress_iface, bytes(frame_ba)


if __name__ == "__main__":
    router = RouterSimulator()
    router.add_interface("eth0", "10.0.1.1", "52:54:00:00:01:01", "10.0.1.0/24")
    router.add_interface("eth1", "10.0.2.1", "52:54:00:00:02:01", "10.0.2.0/24")
    router.set_neighbor_arp("10.0.2.10", "52:54:00:00:02:10")

    # Ingress frame from Host A (10.0.1.10) to Host B (10.0.2.10)
    payload = b"PING-MESSAGE-ROUTER-TEST"
    test_frame = encapsulate(
        src_mac="52:54:00:00:01:10",
        dst_mac="52:54:00:00:01:01",
        src_ip="10.0.1.10",
        dst_ip="10.0.2.10",
        src_port=12345,
        dst_port=80,
        payload=payload,
    )

    status, out_iface, out_frame = router.forward_frame("eth0", test_frame)
    print(f"Routing result: {status} -> Egress on {out_iface}")
    assert status == "FORWARDED"
    assert out_iface == "eth1"

    d_out = decapsulate(out_frame)
    print(f"Transformed Frame on {out_iface}:")
    print(f"  MAC: {d_out.src_mac} -> {d_out.dst_mac}")
    print(f"  IP:  {d_out.src_ip} -> {d_out.dst_ip} (TTL={d_out.ttl})")
    assert d_out.src_mac == "52:54:00:00:02:01"
    assert d_out.dst_mac == "52:54:00:00:02:10"
    assert d_out.ttl == 63  # Decremented by 1
    print("\nSUCCESS: Router forwarding and L2 rewrite verified.")
