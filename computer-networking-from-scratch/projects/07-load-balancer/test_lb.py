#!/usr/bin/env python3
"""
projects/07-load-balancer/test_lb.py
Automated test suite verifying Round-Robin, Least-Connections, and IP Hash algorithms.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from load_balancer import LoadBalancer


class TestLoadBalancer(unittest.TestCase):
    def test_round_robin_selection(self):
        lb = LoadBalancer(
            algorithm="ROUND_ROBIN",
            nodes=[("10.0.0.1", 80), ("10.0.0.2", 80), ("10.0.0.3", 80)],
            bind_listener=False,
        )
        n1 = lb.select_node("192.168.1.10")
        n2 = lb.select_node("192.168.1.10")
        n3 = lb.select_node("192.168.1.10")
        n4 = lb.select_node("192.168.1.10")

        self.assertEqual(n1.host, "10.0.0.1")
        self.assertEqual(n2.host, "10.0.0.2")
        self.assertEqual(n3.host, "10.0.0.3")
        self.assertEqual(n4.host, "10.0.0.1")  # Wrapped around

    def test_least_connections_steers_away_from_busy_nodes(self):
        lb = LoadBalancer(
            algorithm="LEAST_CONNECTIONS",
            nodes=[("10.0.0.1", 80), ("10.0.0.2", 80)],
            bind_listener=False,
        )
        # Node 1 gets 3 active connections
        lb.nodes[0].active_connections = 3
        # Node 2 has 0 active connections
        lb.nodes[1].active_connections = 0

        # Next selection MUST pick Node 2
        selected = lb.select_node("192.168.1.10")
        self.assertEqual(selected.host, "10.0.0.2")

    def test_ip_hash_consistency(self):
        lb = LoadBalancer(
            algorithm="IP_HASH",
            nodes=[("10.0.0.1", 80), ("10.0.0.2", 80), ("10.0.0.3", 80)],
            bind_listener=False,
        )
        client_a = "192.168.1.50"
        client_b = "172.16.0.25"

        first_pick_a = lb.select_node(client_a).host
        for _ in range(5):
            self.assertEqual(lb.select_node(client_a).host, first_pick_a)

        first_pick_b = lb.select_node(client_b).host
        for _ in range(5):
            self.assertEqual(lb.select_node(client_b).host, first_pick_b)


if __name__ == "__main__":
    unittest.main()
