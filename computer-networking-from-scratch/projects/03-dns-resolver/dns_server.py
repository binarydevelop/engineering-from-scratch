#!/usr/bin/env python3
"""
projects/03-dns-resolver/dns_server.py
An RFC 1035 wire-compatible educational DNS server listening over UDP.
Demonstrates:
  - Decoding DNS wire format queries (ID, Flags, QNAME, QTYPE, QCLASS)
  - Caching resolved records in-memory with TTL expiration
  - Encoding standard DNS A-record responses that tools like 'dig' can parse
"""

import socket
import struct
import sys
import time
from typing import Dict, Optional, Tuple

DEFAULT_PORT = 5353


def parse_dns_name(data: bytes, offset: int = 12) -> Tuple[str, int]:
    """Parses a length-prefixed DNS name from wire bytes."""
    labels = []
    curr = offset
    while curr < len(data):
        length = data[curr]
        if length == 0:
            curr += 1
            break
        curr += 1
        labels.append(data[curr : curr + length].decode("ascii", errors="replace"))
        curr += length
    return ".".join(labels), curr


def build_dns_response(query_packet: bytes, qname: str, resolved_ip: Optional[str], ttl: int = 60) -> bytes:
    """Constructs an RFC 1035 DNS response packet."""
    tx_id = query_packet[:2]

    if resolved_ip is None:
        # NXDOMAIN: Flags = 0x8183 (Response, Recursion Desired/Available, RCODE=3)
        flags = struct.pack("!H", 0x8183)
        header = tx_id + flags + struct.pack("!HHHH", 1, 0, 0, 0)
        # Echo question section
        return header + query_packet[12:]

    # Success (NOERROR): Flags = 0x8180 (Response, Recursion Available, RCODE=0)
    flags = struct.pack("!H", 0x8180)
    qdcount = 1
    ancount = 1
    nscount = 0
    arcount = 0
    header = tx_id + flags + struct.pack("!HHHH", qdcount, ancount, nscount, arcount)

    # Question section from query
    _, qend = parse_dns_name(query_packet, 12)
    question_section = query_packet[12 : qend + 4]  # Name + QTYPE (2) + QCLASS (2)

    # Answer section:
    # Use compression pointer to QNAME (offset 12 = 0x0C -> 0xC00C)
    ans_name = struct.pack("!H", 0xC00C)
    ans_type = struct.pack("!H", 1)       # Type A
    ans_class = struct.pack("!H", 1)      # Class IN
    ans_ttl = struct.pack("!I", ttl)      # TTL seconds
    ans_rdlen = struct.pack("!H", 4)      # IPv4 is 4 bytes
    ans_rdata = socket.inet_aton(resolved_ip)

    answer_section = ans_name + ans_type + ans_class + ans_ttl + ans_rdlen + ans_rdata
    return header + question_section + answer_section


class DNSServer:
    def __init__(self, host: str = "127.0.0.1", port: int = DEFAULT_PORT):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))
        self.running = True

        # In-memory zone records
        self.records: Dict[str, Tuple[str, int]] = {
            "example.com": ("93.184.216.34", 120),
            "api.internal": ("10.0.1.50", 300),
            "db.local": ("10.0.2.100", 60),
            "localhost": ("127.0.0.1", 3600),
        }
        # In-memory cache: name -> (ip, expires_at)
        self.cache: Dict[str, Tuple[str, float]] = {}

    def lookup(self, name: str) -> Optional[Tuple[str, int]]:
        now = time.time()
        name_lower = name.lower()

        # Check Cache
        if name_lower in self.cache:
            ip, expires_at = self.cache[name_lower]
            if now < expires_at:
                return ip, int(expires_at - now)
            else:
                del self.cache[name_lower]

        # Check Zone file
        if name_lower in self.records:
            ip, ttl = self.records[name_lower]
            self.cache[name_lower] = (ip, now + ttl)
            return ip, ttl

        return None

    def handle_one_query(self, timeout: float = 1.0) -> None:
        self.sock.settimeout(timeout)
        try:
            query, client_addr = self.sock.recvfrom(4096)
            if len(query) < 12:
                return

            qname, _ = parse_dns_name(query, 12)
            result = self.lookup(qname)

            if result:
                ip, ttl = result
                response = build_dns_response(query, qname, ip, ttl=ttl)
                print(f"[DNS] Resolved '{qname}' -> {ip} (TTL={ttl}s) for {client_addr}")
            else:
                response = build_dns_response(query, qname, None)
                print(f"[DNS] NXDOMAIN for '{qname}' from {client_addr}")

            self.sock.sendto(response, client_addr)
        except socket.timeout:
            pass

    def run(self):
        print(f"RFC 1035 DNS Server listening on {self.host}:{self.port} (UDP)")
        print("Zone records:")
        for k, v in self.records.items():
            print(f"  {k:<15} -> {v[0]} (TTL {v[1]}s)")
        print("\nTest with:")
        print(f"  dig @{self.host} -p {self.port} example.com")

        try:
            while self.running:
                self.handle_one_query(timeout=1.0)
        except KeyboardInterrupt:
            print("\nDNS Server stopped.")
        finally:
            self.close()

    def close(self):
        self.running = False
        try:
            self.sock.close()
        except Exception:
            pass


if __name__ == "__main__":
    p = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PORT
    server = DNSServer(port=p)
    server.run()
