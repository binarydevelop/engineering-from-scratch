#!/usr/bin/env python3
"""
simulations/arp_cache.py
Simulates the Address Resolution Protocol (ARP) cache and resolution cycle.
Resolves: IPv4 Address ──► Link-Layer 48-bit MAC Address.

Lifecycle:
  1. Check local ARP cache
  2. If Hit: return MAC immediately
  3. If Miss:
     - Generate ARP Request frame (Broadcast MAC: ff:ff:ff:ff:ff:ff)
     - Target host detects its IP and replies with ARP Reply (Unicast)
     - Sender receives reply and inserts (IP -> MAC, TTL) into cache
"""

import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass
class ARPEntry:
    mac_address: str
    expiry_time: float
    state: str = "REACHABLE"


@dataclass
class ARPPacket:
    operation: str  # "REQUEST" or "REPLY"
    sender_mac: str
    sender_ip: str
    target_mac: str
    target_ip: str


class HostARPEngine:
    def __init__(self, host_name: str, ip_address: str, mac_address: str, default_ttl_sec: float = 60.0):
        self.host_name = host_name
        self.ip_address = ip_address
        self.mac_address = mac_address
        self.default_ttl_sec = default_ttl_sec
        # Cache table: IP Address -> ARPEntry
        self.cache: Dict[str, ARPEntry] = {}

    def lookup(self, target_ip: str, current_time: Optional[float] = None) -> Optional[str]:
        """Looks up an IP in the local ARP table; purges expired entries."""
        now = current_time if current_time is not None else time.time()
        if target_ip in self.cache:
            entry = self.cache[target_ip]
            if now < entry.expiry_time:
                return entry.mac_address
            else:
                del self.cache[target_ip]  # Expired
        return None

    def insert(self, ip: str, mac: str, current_time: Optional[float] = None) -> None:
        """Inserts or updates an entry in the local ARP cache."""
        now = current_time if current_time is not None else time.time()
        self.cache[ip] = ARPEntry(mac_address=mac, expiry_time=now + self.default_ttl_sec)

    def create_arp_request(self, target_ip: str) -> ARPPacket:
        """Builds an ARP Request packet (Broadcast)."""
        return ARPPacket(
            operation="REQUEST",
            sender_mac=self.mac_address,
            sender_ip=self.ip_address,
            target_mac="00:00:00:00:00:00",  # Unknown
            target_ip=target_ip,
        )

    def handle_incoming_arp(
        self, packet: ARPPacket, current_time: Optional[float] = None
    ) -> Optional[ARPPacket]:
        """
        Receives an ARP packet. Updates cache if relevant, and replies if packet targets this host.
        """
        now = current_time if current_time is not None else time.time()

        # Learn sender's mapping
        self.insert(packet.sender_ip, packet.sender_mac, now)

        if packet.operation == "REQUEST" and packet.target_ip == self.ip_address:
            # Build Unicast ARP Reply
            return ARPPacket(
                operation="REPLY",
                sender_mac=self.mac_address,
                sender_ip=self.ip_address,
                target_mac=packet.sender_mac,
                target_ip=packet.sender_ip,
            )
        return None


if __name__ == "__main__":
    host_a = HostARPEngine("HostA", "10.0.1.10", "52:54:00:11:11:11")
    host_b = HostARPEngine("HostB", "10.0.1.20", "52:54:00:22:22:22")

    print(f"Initial Host A ARP Cache: {host_a.cache}")
    target_ip = "10.0.1.20"

    # Step 1: Cache Miss
    mac = host_a.lookup(target_ip)
    print(f"Step 1: Lookup {target_ip} in Host A cache -> {mac} (Cache Miss)")
    assert mac is None

    # Step 2: Host A creates ARP Request
    request = host_a.create_arp_request(target_ip)
    print(f"Step 2: Host A broadcasts ARP Request: 'Who has {target_ip}? Tell {host_a.ip_address}'")

    # Step 3: Host B receives request and generates reply
    reply = host_b.handle_incoming_arp(request)
    assert reply is not None
    print(f"Step 3: Host B answers with ARP Reply: '{host_b.ip_address} is at {host_b.mac_address}'")

    # Step 4: Host A receives reply and inserts into cache
    host_a.handle_incoming_arp(reply)
    resolved_mac = host_a.lookup(target_ip)
    print(f"Step 4: Host A resolves {target_ip} -> {resolved_mac}")
    assert resolved_mac == host_b.mac_address

    print("\nSUCCESS: ARP request/reply resolution and cache cycle verified.")
