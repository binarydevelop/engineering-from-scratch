#!/usr/bin/env python3
"""
projects/08-tiny-internet/verify_tiny_internet.py
Automated cross-platform topology verifier for the Tiny Internet project.
Validates the mathematical IP subnets, routing prefix matching, and multi-hop forwarding logic.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from simulations.routing_lpm import RoutingTable


class TestTinyInternetRouting(unittest.TestCase):
    def setUp(self):
        # Router A's Routing Table
        self.router_a = RoutingTable()
        self.router_a.add_route("10.10.1.0/24", None, "veth-ra-c")       # Client LAN
        self.router_a.add_route("172.16.0.0/30", None, "veth-ra-t")      # Transit Link
        self.router_a.add_route("10.20.1.0/24", "172.16.0.2", "veth-ra-t") # Static route to Server LAN

        # Router B's Routing Table
        self.router_b = RoutingTable()
        self.router_b.add_route("10.20.1.0/24", None, "veth-rb-s")      # Server LAN
        self.router_b.add_route("172.16.0.0/30", None, "veth-rb-t")      # Transit Link
        self.router_b.add_route("10.10.1.0/24", "172.16.0.1", "veth-rb-t") # Static route to Client LAN

    def test_outbound_routing_path(self):
        # Client wants to send packet to Server (10.20.1.10)
        # Packet arrives at Router A
        r_a_match = self.router_a.lookup("10.20.1.10")
        self.assertIsNotNone(r_a_match)
        self.assertEqual(r_a_match.destination_prefix, "10.20.1.0/24")
        self.assertEqual(r_a_match.next_hop, "172.16.0.2")
        self.assertEqual(r_a_match.interface, "veth-ra-t")

        # Packet traverses transit network and arrives at Router B
        r_b_match = self.router_b.lookup("10.20.1.10")
        self.assertIsNotNone(r_b_match)
        self.assertEqual(r_b_match.destination_prefix, "10.20.1.0/24")
        self.assertIsNone(r_b_match.next_hop)  # Directly connected link
        self.assertEqual(r_b_match.interface, "veth-rb-s")

    def test_return_routing_path(self):
        # Server replies to Client (10.10.1.10)
        # Packet arrives at Router B
        r_b_return = self.router_b.lookup("10.10.1.10")
        self.assertIsNotNone(r_b_return)
        self.assertEqual(r_b_return.next_hop, "172.16.0.1")
        self.assertEqual(r_b_return.interface, "veth-rb-t")

        # Packet arrives at Router A
        r_a_return = self.router_a.lookup("10.10.1.10")
        self.assertIsNotNone(r_a_return)
        self.assertIsNone(r_a_return.next_hop)
        self.assertEqual(r_a_return.interface, "veth-ra-c")


if __name__ == "__main__":
    unittest.main()
