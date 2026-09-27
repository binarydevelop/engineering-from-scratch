#!/usr/bin/env python3
"""
dns_lookup.py
Queries DNS resolution for hostnames and prints resolved IPv4 addresses.
Demonstrates client-side resolution inside container namespaces.
"""

import socket
import sys

def lookup(target: str):
    print(f"Resolving hostname: '{target}'...")
    try:
        ip = socket.gethostbyname(target)
        print(f"  [SUCCESS] {target} -> {ip}")
    except socket.gaierror as e:
        print(f"  [FAILURE] getaddrinfo failed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 dns_lookup.py <HOSTNAME>")
        sys.exit(1)
    lookup(sys.argv[1])
