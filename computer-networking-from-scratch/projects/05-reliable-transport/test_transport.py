#!/usr/bin/env python3
"""
projects/05-reliable-transport/test_transport.py
Automated test suite verifying the scratch reliable transport layer.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from transport import (
    ReliableEndpoint,
    ReliableChannel,
    TransportPacket,
    FLAG_SYN,
    FLAG_ACK,
    FLAG_DATA,
)


class TestReliableTransport(unittest.TestCase):
    def test_three_way_handshake(self):
        client = ReliableEndpoint(initial_seq=100)
        server = ReliableEndpoint(initial_seq=500)

        syn = client.initiate_handshake()
        self.assertEqual(client.state, "SYN_SENT")

        syn_ack = server.handle_packet(syn)
        self.assertIsNotNone(syn_ack)
        self.assertEqual(server.state, "SYN_RCVD")
        self.assertEqual(syn_ack.ack_num, 101)

        ack = client.handle_packet(syn_ack)
        self.assertEqual(client.state, "ESTABLISHED")
        self.assertEqual(ack.ack_num, 501)

        server.handle_packet(ack)
        self.assertEqual(server.state, "ESTABLISHED")

    def test_loss_recovery_and_retransmission(self):
        client = ReliableEndpoint(initial_seq=100)
        server = ReliableEndpoint(initial_seq=500)

        # Handshake
        syn = client.initiate_handshake()
        syn_ack = server.handle_packet(syn)
        ack = client.handle_packet(syn_ack)
        server.handle_packet(ack)
        self.assertEqual(server.state, "ESTABLISHED")

        chunk = b"DATA-CHUNK-1"
        pkt = TransportPacket(flags=FLAG_DATA, seq_num=101, ack_num=501, payload=chunk)
        client.unacked_packets[101] = (pkt, 10.0)

        # Timeout occurs at t=10.5 (RTO = 0.2s)
        retrans = client.check_timeouts(10.5)
        self.assertEqual(len(retrans), 1)
        self.assertEqual(retrans[0].seq_num, 101)

        # Server receives retransmitted packet
        ack_reply = server.handle_packet(retrans[0])
        self.assertEqual(ack_reply.ack_num, 101 + len(chunk))
        self.assertEqual(server.received_data, chunk)


if __name__ == "__main__":
    unittest.main()
