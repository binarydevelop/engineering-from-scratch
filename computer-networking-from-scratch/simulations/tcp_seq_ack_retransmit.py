#!/usr/bin/env python3
"""
simulations/tcp_seq_ack_retransmit.py
Simulates byte-stream sequence numbering, cumulative ACKs, packet loss detection,
and retransmission (RTO timeout and Fast Retransmit).
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass
class Segment:
    seq_num: int
    payload: bytes
    length: int

    def __init__(self, seq_num: int, payload: bytes):
        self.seq_num = seq_num
        self.payload = payload
        self.length = len(payload)


@dataclass
class AckPacket:
    ack_num: int  # Cumulative ACK: next expected byte


class SimplifiedTCPSender:
    def __init__(self, initial_seq: int = 1000):
        self.isn = initial_seq
        self.next_seq_num = initial_seq
        self.unacknowledged_segments: Dict[int, Segment] = {}  # seq_num -> Segment
        self.duplicate_ack_count = 0
        self.last_ack_received = initial_seq
        self.retransmitted_count = 0

    def send_data(self, data: bytes, chunk_size: int = 10) -> List[Segment]:
        """Segments a byte stream and returns packets to transmit."""
        segments = []
        for i in range(0, len(data), chunk_size):
            chunk = data[i : i + chunk_size]
            seg = Segment(self.next_seq_num, chunk)
            self.unacknowledged_segments[self.next_seq_num] = seg
            self.next_seq_num += seg.length
            segments.append(seg)
        return segments

    def receive_ack(self, ack: AckPacket) -> Optional[Segment]:
        """
        Processes incoming cumulative ACK.
        Returns retransmitted segment if 3 duplicate ACKs trigger Fast Retransmit.
        """
        if ack.ack_num > self.last_ack_received:
            # New acknowledgment: advance window
            self.last_ack_received = ack.ack_num
            self.duplicate_ack_count = 0
            # Remove all acknowledged segments from buffer
            acked_seqs = [s for s in self.unacknowledged_segments if s + self.unacknowledged_segments[s].length <= ack.ack_num]
            for s in acked_seqs:
                del self.unacknowledged_segments[s]
            return None
        elif ack.ack_num == self.last_ack_received:
            # Duplicate ACK
            self.duplicate_ack_count += 1
            if self.duplicate_ack_count == 3:
                # FAST RETRANSMIT: Resend the missing segment immediately!
                missing_seq = ack.ack_num
                if missing_seq in self.unacknowledged_segments:
                    self.retransmitted_count += 1
                    return self.unacknowledged_segments[missing_seq]
        return None

    def trigger_timeout(self) -> Optional[Segment]:
        """Simulates RTO timer expiration; retransmits oldest unACKed segment."""
        if not self.unacknowledged_segments:
            return None
        oldest_seq = min(self.unacknowledged_segments.keys())
        self.retransmitted_count += 1
        return self.unacknowledged_segments[oldest_seq]


class SimplifiedTCPReceiver:
    def __init__(self, initial_seq: int = 1000):
        self.expected_seq_num = initial_seq
        self.received_stream = bytearray()
        self.out_of_order_buffer: Dict[int, Segment] = {}  # seq -> segment

    def receive_segment(self, seg: Segment) -> AckPacket:
        """Processes segment and returns cumulative ACK."""
        if seg.seq_num == self.expected_seq_num:
            # In-order segment received
            self.received_stream.extend(seg.payload)
            self.expected_seq_num += seg.length

            # Check if buffered out-of-order segments can now be drained
            while self.expected_seq_num in self.out_of_order_buffer:
                buffered = self.out_of_order_buffer.pop(self.expected_seq_num)
                self.received_stream.extend(buffered.payload)
                self.expected_seq_num += buffered.length

        elif seg.seq_num > self.expected_seq_num:
            # Out-of-order segment received: buffer it!
            self.out_of_order_buffer[seg.seq_num] = seg

        # Always return cumulative ACK for next expected byte
        return AckPacket(ack_num=self.expected_seq_num)


if __name__ == "__main__":
    sender = SimplifiedTCPSender(initial_seq=1000)
    receiver = SimplifiedTCPReceiver(initial_seq=1000)

    message = b"ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"  # 36 bytes
    segments = sender.send_data(message, chunk_size=10)
    print(f"Original message: {message.decode()} ({len(message)} bytes)")
    print(f"Divided into {len(segments)} segments:")
    for s in segments:
        print(f"  Seq {s.seq_num}: {s.payload.decode()!r} ({s.length} bytes)")
    print("=" * 65)

    # Simulate network transmission: Drop segment 1 (index 1: "KLMNOPQRST")
    print("Transmitting segments: Simulating DROP of Segment 1 (Seq 1010)...")
    transmitted = [segments[0], segments[2], segments[3]]  # Seg 1 dropped!

    # Receiver processes Seg 0
    ack0 = receiver.receive_segment(segments[0])
    sender.receive_ack(ack0)
    print(f"Receiver got Seg 0 (1000) -> Generated ACK: {ack0.ack_num}")

    # Receiver processes Seg 2 (out of order!)
    ack2 = receiver.receive_segment(segments[2])
    print(f"Receiver got Seg 2 (1020) -> Buffered out-of-order, Generated Dup ACK: {ack2.ack_num}")
    retrans = sender.receive_ack(ack2)

    # Receiver processes Seg 3 (out of order!)
    ack3 = receiver.receive_segment(segments[3])
    print(f"Receiver got Seg 3 (1030) -> Buffered out-of-order, Generated Dup ACK: {ack3.ack_num}")
    retrans = sender.receive_ack(ack3)

    # Now simulate timeout or 3rd dup ack
    print("\nTriggering RTO Timeout on Sender for missing byte 1010...")
    timeout_seg = sender.trigger_timeout()
    assert timeout_seg is not None
    print(f"Sender retransmitted: Seq {timeout_seg.seq_num} ({timeout_seg.payload.decode()!r})")

    # Receiver receives retransmitted Seg 1
    recovery_ack = receiver.receive_segment(timeout_seg)
    print(f"Receiver received missing Seg 1 -> Drains buffer -> Cumulative ACK: {recovery_ack.ack_num}")
    sender.receive_ack(recovery_ack)

    print("\nFinal Reconstructed Stream at Receiver:")
    print(f"  {receiver.received_stream.decode()!r}")
    assert receiver.received_stream == message, "Stream corruption!"
    assert sender.retransmitted_count >= 1, "Retransmit was not counted!"
    print("SUCCESS: TCP sequence numbers, cumulative ACKs, and retransmission verified.")
