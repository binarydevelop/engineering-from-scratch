#!/usr/bin/env python3
"""
simulations/encapsulation.py
Demonstrates packet encapsulation and decapsulation from first principles.
Wraps application payload down the stack:
  HTTP Payload ──► TCP Segment ──► IPv4 Packet ──► Ethernet II Frame
Then decapsulates in reverse up the stack.
"""

import socket
import struct
from dataclasses import dataclass
from typing import Tuple


def mac_to_bytes(mac: str) -> bytes:
    """Converts 'AA:BB:CC:DD:EE:FF' to 6 bytes."""
    return bytes.fromhex(mac.replace(":", "").replace("-", ""))


def bytes_to_mac(b: bytes) -> str:
    """Converts 6 bytes to 'AA:BB:CC:DD:EE:FF'."""
    return ":".join(f"{x:02x}" for x in b)


def compute_ip_checksum(header: bytes) -> int:
    """Computes standard Internet Checksum (RFC 1071) over 16-bit words."""
    if len(header) % 2 != 0:
        header += b"\x00"
    checksum = 0
    for i in range(0, len(header), 2):
        word = (header[i] << 8) + header[i + 1]
        checksum += word
        while checksum >> 16:
            checksum = (checksum & 0xFFFF) + (checksum >> 16)
    return ~checksum & 0xFFFF


@dataclass
class DecapsulatedFrame:
    src_mac: str
    dst_mac: str
    ethertype: int
    src_ip: str
    dst_ip: str
    ip_proto: int
    ttl: int
    src_port: int
    dst_port: int
    tcp_seq: int
    tcp_ack: int
    tcp_flags: int
    application_payload: bytes


def encapsulate(
    src_mac: str,
    dst_mac: str,
    src_ip: str,
    dst_ip: str,
    src_port: int,
    dst_port: int,
    payload: bytes,
    seq: int = 1000,
    ack: int = 0,
    flags: int = 0x18,  # PSH | ACK
) -> bytes:
    """Encapsulates application payload into a raw Ethernet II frame."""

    # 1. Transport Layer: TCP Header (20 bytes)
    # Header format: !HHIIBBHHH (20 bytes)
    data_offset_and_reserved = (5 << 4)  # 5 32-bit words = 20 bytes
    window_size = 65535
    tcp_checksum = 0
    urgent_ptr = 0

    tcp_header = struct.pack(
        "!HHIIBBHHH",
        src_port,
        dst_port,
        seq,
        ack,
        data_offset_and_reserved,
        flags,
        window_size,
        tcp_checksum,
        urgent_ptr,
    )
    tcp_segment = tcp_header + payload

    # 2. Network Layer: IPv4 Header (20 bytes)
    # Format: !BBHHHBBH4s4s
    version_ihl = (4 << 4) | 5  # Version 4, IHL 5 (20 bytes)
    tos = 0
    total_length = 20 + len(tcp_segment)
    packet_id = 54321
    flags_fragment = 0x4000  # DF (Don't Fragment) bit set
    ttl = 64
    proto = 6  # TCP
    src_ip_bytes = socket.inet_aton(src_ip)
    dst_ip_bytes = socket.inet_aton(dst_ip)

    # Initial zero-checksum header for calculation
    ip_header_pre = struct.pack(
        "!BBHHHBBH4s4s",
        version_ihl,
        tos,
        total_length,
        packet_id,
        flags_fragment,
        ttl,
        proto,
        0,
        src_ip_bytes,
        dst_ip_bytes,
    )
    ip_checksum = compute_ip_checksum(ip_header_pre)

    ip_header = struct.pack(
        "!BBHHHBBH4s4s",
        version_ihl,
        tos,
        total_length,
        packet_id,
        flags_fragment,
        ttl,
        proto,
        ip_checksum,
        src_ip_bytes,
        dst_ip_bytes,
    )
    ip_packet = ip_header + tcp_segment

    # 3. Data Link Layer: Ethernet II Header (14 bytes)
    # Format: !6s6sH
    ethertype = 0x0800  # IPv4
    eth_header = struct.pack(
        "!6s6sH",
        mac_to_bytes(dst_mac),
        mac_to_bytes(src_mac),
        ethertype,
    )

    frame = eth_header + ip_packet
    return frame


def decapsulate(frame: bytes) -> DecapsulatedFrame:
    """Decapsulates a raw Ethernet II frame up to application payload."""
    if len(frame) < 14 + 20 + 20:
        raise ValueError("Frame too short to contain Ethernet + IP + TCP headers.")

    # 1. Unpack Ethernet Header (14 bytes)
    dst_mac_raw, src_mac_raw, ethertype = struct.unpack("!6s6sH", frame[:14])
    if ethertype != 0x0800:
        raise ValueError(f"Unsupported EtherType 0x{ethertype:04x}; expected 0x0800 (IPv4).")

    # 2. Unpack IPv4 Header (20 bytes)
    ip_raw = frame[14:34]
    version_ihl, tos, total_length, pkt_id, flags_frag, ttl, proto, chk, src_ip_raw, dst_ip_raw = (
        struct.unpack("!BBHHHBBH4s4s", ip_raw)
    )
    ihl = (version_ihl & 0x0F) * 4
    ip_payload = frame[14 + ihl : 14 + total_length]

    # 3. Unpack TCP Header (20 bytes)
    tcp_raw = ip_payload[:20]
    src_port, dst_port, seq, ack, data_offset, flags, window, chk, urg = struct.unpack(
        "!HHIIBBHHH", tcp_raw
    )
    tcp_hl = (data_offset >> 4) * 4
    app_payload = ip_payload[tcp_hl:]

    return DecapsulatedFrame(
        src_mac=bytes_to_mac(src_mac_raw),
        dst_mac=bytes_to_mac(dst_mac_raw),
        ethertype=ethertype,
        src_ip=socket.inet_ntoa(src_ip_raw),
        dst_ip=socket.inet_ntoa(dst_ip_raw),
        ip_proto=proto,
        ttl=ttl,
        src_port=src_port,
        dst_port=dst_port,
        tcp_seq=seq,
        tcp_ack=ack,
        tcp_flags=flags,
        application_payload=app_payload,
    )


if __name__ == "__main__":
    payload = b"GET /index.html HTTP/1.1\r\nHost: example.com\r\n\r\n"
    print("Application Data:")
    print(f"  {payload.decode().strip()!r} ({len(payload)} bytes)\n")

    frame = encapsulate(
        src_mac="52:54:00:12:34:56",
        dst_mac="52:54:00:ab:cd:ef",
        src_ip="192.168.1.10",
        dst_ip="93.184.216.34",
        src_port=54321,
        dst_port=80,
        payload=payload,
    )

    print(f"Encapsulated Frame ({len(frame)} bytes total):")
    print(f"  Hex: {frame[:32].hex()} ... {frame[-16:].hex()}\n")

    d = decapsulate(frame)
    print("Decapsulated Fields Verification:")
    print(f"  [L2] Ethernet: {d.src_mac} -> {d.dst_mac} (Type 0x{d.ethertype:04x})")
    print(f"  [L3] IPv4:     {d.src_ip} -> {d.dst_ip} (TTL={d.ttl}, Proto={d.ip_proto})")
    print(f"  [L4] TCP:      Port {d.src_port} -> {d.dst_port} (Seq={d.tcp_seq}, Ack={d.tcp_ack})")
    print(f"  [L7] Payload:  {d.application_payload.decode().strip()!r}")
    assert d.application_payload == payload, "Payload mismatch!"
    print("\nSUCCESS: Complete encapsulation and decapsulation round-trip verified.")
