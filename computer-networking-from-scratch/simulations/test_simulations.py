#!/usr/bin/env python3
"""
simulations/test_simulations.py
Automated test suite verifying all educational network simulations.
"""

import unittest
from simulations.transmission_delay import calculate_transmission_delay, compare_link_speeds
from simulations.latency_components import NetworkHop, simulate_path
from simulations.encapsulation import encapsulate, decapsulate
from simulations.mac_switch import Layer2Switch, EthernetFrame
from simulations.arp_cache import HostARPEngine
from simulations.routing_lpm import RoutingTable
from simulations.tcp_seq_ack_retransmit import SimplifiedTCPSender, SimplifiedTCPReceiver
from simulations.sliding_window import SlidingWindowSimulator, compare_utilization
from simulations.congestion_control import TCPCongestionSimulator
from simulations.dns_resolver import RecursiveDNSResolver
from simulations.token_bucket import TokenBucket
from simulations.queueing_bufferbloat import mm1_theoretical_delay, simulate_buffer_growth
from simulations.retries_exponential_backoff import calculate_delays, simulate_concurrent_clients
from simulations.idempotency_risk import PaymentServer, simulate_payment_attempt


class TestSimulations(unittest.TestCase):
    def test_transmission_delay(self):
        one_mb = 1024 * 1024
        delay = calculate_transmission_delay(one_mb, 10 * 1000 * 1000)
        self.assertAlmostEqual(delay, 0.83886, places=4)
        speeds = compare_link_speeds(one_mb)
        self.assertEqual(len(speeds), 6)

    def test_latency_components(self):
        hops = [NetworkHop("H1", 200_000, 10 * 10**9, 0.00001, 0.0001)]
        res = simulate_path(hops, 1500)
        # Propagation for 200km at 200,000 km/s is 1.0 ms
        self.assertAlmostEqual(res.propagation_ms, 1.0, places=2)
        self.assertGreater(res.estimated_rtt_ms, 2.0)

    def test_encapsulation_roundtrip(self):
        payload = b"PING-PONG-PAYLOAD-12345"
        frame = encapsulate(
            src_mac="00:11:22:33:44:55",
            dst_mac="66:77:88:99:aa:bb",
            src_ip="10.0.0.1",
            dst_ip="10.0.0.2",
            src_port=12345,
            dst_port=80,
            payload=payload,
        )
        d = decapsulate(frame)
        self.assertEqual(d.application_payload, payload)
        self.assertEqual(d.src_ip, "10.0.0.1")
        self.assertEqual(d.dst_ip, "10.0.0.2")
        self.assertEqual(d.src_port, 12345)
        self.assertEqual(d.dst_port, 80)

    def test_mac_switch_learning_and_flooding(self):
        sw = Layer2Switch(num_ports=4)
        f1 = EthernetFrame("00:00:00:00:00:01", "00:00:00:00:00:02", "hello")
        action, ports = sw.process_frame(1, f1)
        self.assertEqual(ports, [2, 3, 4])  # Flooded

        # Reply from port 2
        f2 = EthernetFrame("00:00:00:00:00:02", "00:00:00:00:00:01", "ack")
        action, ports = sw.process_frame(2, f2)
        self.assertEqual(ports, [1])  # Direct forward to port 1

    def test_arp_cache_resolution(self):
        host_a = HostARPEngine("A", "192.168.1.10", "aa:aa:aa:aa:aa:aa")
        host_b = HostARPEngine("B", "192.168.1.20", "bb:bb:bb:bb:bb:bb")
        self.assertIsNone(host_a.lookup("192.168.1.20"))
        req = host_a.create_arp_request("192.168.1.20")
        reply = host_b.handle_incoming_arp(req)
        self.assertIsNotNone(reply)
        host_a.handle_incoming_arp(reply)
        self.assertEqual(host_a.lookup("192.168.1.20"), "bb:bb:bb:bb:bb:bb")

    def test_routing_longest_prefix_match(self):
        rt = RoutingTable()
        rt.add_route("0.0.0.0/0", "192.168.1.1", "eth0")
        rt.add_route("10.0.0.0/8", "10.0.0.1", "eth1")
        rt.add_route("10.1.0.0/16", "10.1.0.1", "eth2")
        rt.add_route("10.1.2.0/24", None, "eth3")

        match = rt.lookup("10.1.2.50")
        self.assertEqual(match.destination_prefix, "10.1.2.0/24")
        self.assertEqual(match.interface, "eth3")

        match_fallback = rt.lookup("10.1.9.99")
        self.assertEqual(match_fallback.destination_prefix, "10.1.0.0/16")

    def test_tcp_retransmission(self):
        sender = SimplifiedTCPSender(1000)
        receiver = SimplifiedTCPReceiver(1000)
        msg = b"0123456789abcdefghij"  # 20 bytes
        segs = sender.send_data(msg, chunk_size=10)
        self.assertEqual(len(segs), 2)

        # Drop seg 0, send seg 1
        ack1 = receiver.receive_segment(segs[1])
        self.assertEqual(ack1.ack_num, 1000)  # Still expects 1000

        # Timeout retransmit
        re_seg = sender.trigger_timeout()
        self.assertEqual(re_seg.seq_num, 1000)
        ack2 = receiver.receive_segment(re_seg)
        self.assertEqual(ack2.ack_num, 1020)  # Received both
        self.assertEqual(receiver.received_stream, msg)

    def test_sliding_window(self):
        sim = SlidingWindowSimulator(window_size=3, total_packets=5)
        self.assertTrue(sim.can_send())
        p0 = sim.send_packet()
        p1 = sim.send_packet()
        p2 = sim.send_packet()
        self.assertFalse(sim.can_send())  # Window full
        sim.receive_ack(0)
        self.assertTrue(sim.can_send())

    def test_congestion_control(self):
        sim = TCPCongestionSimulator(initial_cwnd=1.0, initial_ssthresh=8.0)
        # Slow start
        sim.run_round(1)
        self.assertEqual(sim.cwnd, 2.0)
        sim.run_round(2)
        self.assertEqual(sim.cwnd, 4.0)
        sim.run_round(3)
        self.assertEqual(sim.cwnd, 8.0)
        # Reached ssthresh -> Congestion Avoidance
        sim.run_round(4)
        self.assertEqual(sim.cwnd, 9.0)

    def test_dns_caching(self):
        dns = RecursiveDNSResolver()
        ip, src = dns.resolve("example.com", current_time=100.0)
        self.assertEqual(src, "RECURSIVE_LOOKUP")
        ip2, src2 = dns.resolve("example.com", current_time=102.0)
        self.assertEqual(src2, "CACHE_HIT")
        self.assertEqual(ip, ip2)

    def test_token_bucket(self):
        tb = TokenBucket(rate_bytes_per_sec=1000, capacity_bytes=2000)
        ok, _ = tb.consume(1500, current_time=0.0)
        self.assertTrue(ok)
        ok2, _ = tb.consume(1000, current_time=0.0)
        self.assertFalse(ok2)  # Exhausted
        ok3, _ = tb.consume(1000, current_time=1.0)
        self.assertTrue(ok3)  # Replenished

    def test_idempotency_risk(self):
        srv = PaymentServer()
        deductions, balance = simulate_payment_attempt(srv, idempotency_key=None)
        self.assertEqual(deductions, 2)
        self.assertEqual(balance, 800.0)

        srv2 = PaymentServer()
        deductions2, balance2 = simulate_payment_attempt(srv2, idempotency_key="key-123")
        self.assertEqual(deductions2, 1)
        self.assertEqual(balance2, 900.0)


if __name__ == "__main__":
    unittest.main()
