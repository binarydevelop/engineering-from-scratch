#!/usr/bin/env python3
"""
projects/03-dns-resolver/test_dns.py
Automated test suite verifying the scratch DNS resolver using binary wire queries.
"""

import os
import socket
import struct
import sys
import threading
import time
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from dns_server import DNSServer, parse_dns_name


def encode_dns_query(tx_id: int, qname: str) -> bytes:
    """Builds a standard 12-byte header + question section query."""
    header = struct.pack("!HHHHHH", tx_id, 0x0100, 1, 0, 0, 0)
    question = bytearray()
    for part in qname.split("."):
        question.append(len(part))
        question.extend(part.encode("ascii"))
    question.append(0)  # Terminal root label
    question.extend(struct.pack("!HH", 1, 1))  # QTYPE A, QCLASS IN
    return header + bytes(question)


class TestDNSServer(unittest.TestCase):
    def setUp(self):
        self.server = DNSServer(host="127.0.0.1", port=5359)
        self.thread = threading.Thread(target=self.server.run, daemon=True)
        self.thread.start()
        time.sleep(0.1)

    def tearDown(self):
        self.server.close()
        time.sleep(0.05)

    def test_dns_a_record_resolution(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(1.0)
            query = encode_dns_query(0x1234, "example.com")
            sock.sendto(query, ("127.0.0.1", 5359))

            resp, _ = sock.recvfrom(4096)
            self.assertGreaterEqual(len(resp), 32)
            tx_id, flags, qdcount, ancount = struct.unpack("!HHHH", resp[:8])
            self.assertEqual(tx_id, 0x1234)
            self.assertEqual(ancount, 1)

            # Check that 93.184.216.34 is present in the response rdata
            expected_ip = socket.inet_aton("93.184.216.34")
            self.assertIn(expected_ip, resp)

    def test_dns_nxdomain(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(1.0)
            query = encode_dns_query(0x5678, "invalid.notfound")
            sock.sendto(query, ("127.0.0.1", 5359))

            resp, _ = sock.recvfrom(4096)
            _, flags, _, ancount = struct.unpack("!HHHH", resp[:8])
            # RCODE is lower 4 bits of flags
            rcode = flags & 0x000F
            self.assertEqual(rcode, 3)  # NXDOMAIN = 3
            self.assertEqual(ancount, 0)


if __name__ == "__main__":
    unittest.main()
