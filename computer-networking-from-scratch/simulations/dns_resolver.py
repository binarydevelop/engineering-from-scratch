#!/usr/bin/env python3
"""
simulations/dns_resolver.py
Simulates a recursive and caching Domain Name System (DNS) resolver.
Demonstrates:
  1. Stub resolver query to Recursive Resolver
  2. Recursive Resolver traversing Root -> TLD -> Authoritative Nameservers
  3. Caching with Time-To-Live (TTL) expiration
  4. Cache hits vs cache misses
"""

import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass
class DNSRecord:
    name: str
    record_type: str  # "A", "AAAA", "CNAME", "NS"
    value: str
    ttl_seconds: int


@dataclass
class CacheEntry:
    record: DNSRecord
    expires_at: float


class MockAuthoritativeServer:
    def __init__(self, zone: str, records: List[DNSRecord]):
        self.zone = zone
        self.records = {r.name.lower(): r for r in records}

    def query(self, name: str) -> Optional[DNSRecord]:
        return self.records.get(name.lower())


class RecursiveDNSResolver:
    def __init__(self):
        # Local Resolver Cache: Name -> CacheEntry
        self.cache: Dict[str, CacheEntry] = {}
        self.query_count = 0
        self.cache_hits = 0
        self.cache_misses = 0

        # Mock global hierarchy
        self.authoritative_servers = {
            "example.com": MockAuthoritativeServer("example.com", [
                DNSRecord("example.com", "A", "93.184.216.34", ttl_seconds=5),
                DNSRecord("api.example.com", "A", "93.184.216.35", ttl_seconds=3),
            ]),
            "github.com": MockAuthoritativeServer("github.com", [
                DNSRecord("github.com", "A", "140.82.121.4", ttl_seconds=10),
            ]),
        }

    def resolve(self, domain_name: str, current_time: Optional[float] = None) -> Tuple[Optional[str], str]:
        """
        Resolves domain_name to IP.
        Returns: (IP Address, Resolution Source: "CACHE_HIT" or "RECURSIVE_LOOKUP")
        """
        self.query_count += 1
        now = current_time if current_time is not None else time.time()
        name = domain_name.lower()

        # Step 1: Check Cache
        if name in self.cache:
            entry = self.cache[name]
            if now < entry.expires_at:
                self.cache_hits += 1
                return entry.record.value, "CACHE_HIT"
            else:
                # Expired TTL: evict
                del self.cache[name]

        # Step 2: Cache Miss -> Perform Recursive Lookup
        self.cache_misses += 1

        # Match against authoritative zones
        resolved_rec: Optional[DNSRecord] = None
        for zone, server in self.authoritative_servers.items():
            if name == zone or name.endswith("." + zone):
                resolved_rec = server.query(name)
                if resolved_rec:
                    break

        if resolved_rec:
            # Store in cache with expiration
            self.cache[name] = CacheEntry(
                record=resolved_rec,
                expires_at=now + resolved_rec.ttl_seconds,
            )
            return resolved_rec.value, "RECURSIVE_LOOKUP"

        return None, "NXDOMAIN"


if __name__ == "__main__":
    resolver = RecursiveDNSResolver()
    t0 = 1000.0  # Synthetic epoch start

    print("DNS Recursive Resolution & Caching Simulation:")
    print("=" * 65)

    # 1. First Query: Cache Miss
    ip1, src1 = resolver.resolve("example.com", current_time=t0)
    print(f"Query 1: 'example.com' at t={t0:.1f}s -> {ip1} ({src1})")
    assert src1 == "RECURSIVE_LOOKUP"

    # 2. Second Query immediately after: Cache Hit!
    ip2, src2 = resolver.resolve("example.com", current_time=t0 + 2.0)
    print(f"Query 2: 'example.com' at t={t0+2.0:.1f}s -> {ip2} ({src2})")
    assert src2 == "CACHE_HIT"

    # 3. Third Query after TTL expires (TTL=5s, t=t0 + 6s): Cache Miss & Re-fetch
    ip3, src3 = resolver.resolve("example.com", current_time=t0 + 6.0)
    print(f"Query 3: 'example.com' at t={t0+6.0:.1f}s (TTL expired) -> {ip3} ({src3})")
    assert src3 == "RECURSIVE_LOOKUP"

    # 4. Unknown domain
    ip4, src4 = resolver.resolve("nonexistent.invalid", current_time=t0 + 6.0)
    print(f"Query 4: 'nonexistent.invalid' -> {ip4} ({src4})")
    assert src4 == "NXDOMAIN"

    print(f"\nStats: Total={resolver.query_count}, Hits={resolver.cache_hits}, Misses={resolver.cache_misses}")
    print("SUCCESS: DNS recursive resolution and TTL caching validated.")
