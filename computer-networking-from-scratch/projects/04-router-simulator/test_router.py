#!/usr/bin/env python3
"""
projects/04-router-simulator/test_router.py
Automated test suite verifying the multi-homed router simulator.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from router import RouterSimulator
from simulations.encapsulation import encapsulate, decapsulate


class TestRouterSimulator(unittest.TestCase):
    def setUp(self):
        self.router = RouterSimulator()
        self.router.add_interface("eth0", "10.0.1.1", "52:54:00:00:01:01", "10.0.1.0/24")
        self.router.add_interface("eth1", "10.0.2.1", "52:54:00:00:02:01", "10.0.2.0/24")
        self.router.set_neighbor_arp("10.0.2.50", "52:54:00:00:02:50")

    def test_successful_forwarding_and_ttl_decrement(self):
        frame = encapsulate(
            src_mac="52:54:00:00:01:10",
            dst_mac="52:54:00:00:01:01",
            src_ip="10.0.1.10",
            dst_ip="10.0.2.50",
            src_port=50000,
            dst_port=80,
            payload=b"test-payload",
        )
        status, egress_iface, out_frame = self.router.forward_frame("eth0", frame)
        self.assertEqual(status, "FORWARDED")
        self.assertEqual(egress_iface, "eth1")
        self.assertIsNotNone(out_frame)

        d = decapsulate(out_frame)
        self.assertEqual(d.src_mac, "52:54:00:00:02:01")  # Router's eth1 MAC
        self.assertEqual(d.dst_mac, "52:54:00:00:02:50")  # Next-hop host MAC
        self.assertEqual(d.ttl, 63)                       # Decremented from 64
        self.assertEqual(d.src_ip, "10.0.1.10")            # IP preserved
        self.assertEqual(d.dst_ip, "10.0.2.50")

    def test_ttl_expired_drop(self):
        # Frame with TTL=1
        frame = encapsulate(
            src_mac="52:54:00:00:01:10",
            dst_mac="52:54:00:00:01:01",
            src_ip="10.0.1.10",
            dst_ip="10.0.2.50",
            src_port=50000,
            dst_port=80,
            payload=b"ttl-test",
        )
        # Modify TTL to 1
        ba = bytearray(frame)
        ba[22] = 1
        status, _, out_frame = self.router.forward_frame("eth0", bytes(ba))
        self.assertEqual(status, "ICMP_TIME_EXCEEDED_TTL_EXPIRED")
        self.assertIsNone(out_frame)


if __name__ == "__main__":
    unittest.main()
