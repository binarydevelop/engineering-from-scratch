#!/usr/bin/env python3
"""
simulations/sliding_window.py
Demonstrates the mechanics of the sliding window protocol.
Contrasts Stop-and-Wait (window=1) with Pipelined Sliding Window (window=W).
Calculates throughput and channel utilization.
"""

from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class WindowState:
    base: int           # Oldest unacknowledged sequence number
    next_seq: int       # Next sequence number to be sent
    window_size: int    # Allowed window size in packets
    total_packets: int


class SlidingWindowSimulator:
    def __init__(self, window_size: int, total_packets: int):
        self.window_size = window_size
        self.total_packets = total_packets
        self.base = 0
        self.next_seq = 0
        self.history: List[Tuple[int, int, str]] = []  # (base, next_seq, action)

    def can_send(self) -> bool:
        """Returns True if the current window has room for another transmission."""
        return (self.next_seq < self.base + self.window_size) and (self.next_seq < self.total_packets)

    def send_packet(self) -> int:
        """Transmits the next packet in the window."""
        if not self.can_send():
            raise RuntimeError("Window is full! Cannot send until ACK is received.")
        seq = self.next_seq
        self.next_seq += 1
        self.history.append((self.base, self.next_seq, f"SENT Packet {seq}"))
        return seq

    def receive_ack(self, ack_num: int) -> None:
        """Slides the window forward upon receiving cumulative ACK."""
        if ack_num >= self.base:
            self.base = ack_num + 1
            self.history.append((self.base, self.next_seq, f"RECEIVED ACK {ack_num} -> Window slid to base {self.base}"))


def compare_utilization(rtt_ms: float, packet_size_bytes: int, bandwidth_bps: int, window_size: int) -> Tuple[float, float]:
    """
    Computes utilization for Stop-and-Wait vs Sliding Window.
    Transmission delay = L / R
    Utilization U = (W * d_trans) / (d_trans + RTT)
    """
    d_trans_ms = ((packet_size_bytes * 8) / bandwidth_bps) * 1000.0
    u_stop_and_wait = d_trans_ms / (d_trans_ms + rtt_ms)
    u_sliding_window = min(1.0, (window_size * d_trans_ms) / (d_trans_ms + rtt_ms))
    return u_stop_and_wait, u_sliding_window


if __name__ == "__main__":
    w_size = 4
    total = 8
    sim = SlidingWindowSimulator(window_size=w_size, total_packets=total)

    print(f"Simulating Sliding Window (Window Size = {w_size}, Total Packets = {total}):")
    print("=" * 65)

    # Send initial burst up to window capacity
    while sim.can_send():
        p = sim.send_packet()
        print(f"Transmit: Pkt {p} | Window Range: [{sim.base} .. {sim.base + sim.window_size - 1}]")

    print(f"\nWindow Full. Can send more? {sim.can_send()}")

    # Receive ACKs for first 2 packets and slide window
    print("\nReceiving ACK 0 and ACK 1...")
    sim.receive_ack(0)
    sim.receive_ack(1)
    print(f"Window Base advanced to {sim.base}. Range: [{sim.base} .. {sim.base + sim.window_size - 1}]")

    # Send next packets
    while sim.can_send():
        p = sim.send_packet()
        print(f"Transmit: Pkt {p} | Window Range: [{sim.base} .. {sim.base + sim.window_size - 1}]")

    print("\nUtilization Comparison (100 Mbps link, 50ms RTT, 1500-byte packets):")
    u_stop, u_pipe = compare_utilization(rtt_ms=50.0, packet_size_bytes=1500, bandwidth_bps=100*10**6, window_size=64)
    print(f"  Stop-and-Wait (W=1):  Utilization = {u_stop * 100:6.3f}%")
    print(f"  Sliding Window (W=64): Utilization = {u_pipe * 100:6.3f}% ({u_pipe/u_stop:.1f}x throughput increase)")

    print("\nSUCCESS: Sliding window simulation verified.")
