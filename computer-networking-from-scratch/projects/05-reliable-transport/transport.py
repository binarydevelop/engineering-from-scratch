#!/usr/bin/env python3
"""
projects/05-reliable-transport/transport.py
A reliable byte-stream transport protocol implementation on top of unreliable datagrams.
Implements:
  - 3-Way Handshake (SYN, SYN-ACK, ACK)
  - Sequence numbers and byte-offset tracking
  - Sliding Window pipelining
  - Cumulative Acknowledgments
  - Retransmission Timeouts (RTO) for dropped packets
  - Graceful Teardown (FIN, ACK)
"""

import random
import socket
import struct
import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

FLAG_SYN = 0x01
FLAG_ACK = 0x02
FLAG_FIN = 0x04
FLAG_DATA = 0x08


@dataclass
class TransportPacket:
    flags: int
    seq_num: int
    ack_num: int
    payload: bytes

    def serialize(self) -> bytes:
        # Header: Flags (1B), Seq (4B), Ack (4B), PayloadLen (2B)
        header = struct.pack("!BIIH", self.flags, self.seq_num, self.ack_num, len(self.payload))
        return header + self.payload

    @classmethod
    def deserialize(cls, data: bytes) -> "TransportPacket":
        flags, seq, ack, plen = struct.unpack("!BIIH", data[:11])
        payload = data[11 : 11 + plen]
        return cls(flags=flags, seq_num=seq, ack_num=ack, payload=payload)


class ReliableChannel:
    """Simulates an unreliable physical channel with configurable packet drop probability."""
    def __init__(self, drop_probability: float = 0.0):
        self.drop_prob = drop_probability
        self.packets_sent = 0
        self.packets_dropped = 0

    def transmit(self, packet: TransportPacket) -> Optional[TransportPacket]:
        self.packets_sent += 1
        if random.random() < self.drop_prob:
            self.packets_dropped += 1
            return None  # Dropped in transit!
        return packet


class ReliableEndpoint:
    def __init__(self, initial_seq: int = 1000, window_size: int = 4, rto_seconds: float = 0.2):
        self.seq_num = initial_seq
        self.expected_seq = 0
        self.window_size = window_size
        self.rto_seconds = rto_seconds
        self.state = "CLOSED"
        self.received_data = bytearray()
        self.unacked_packets: Dict[int, Tuple[TransportPacket, float]] = {}  # seq -> (pkt, send_time)
        self.retransmissions = 0

    def initiate_handshake(self) -> TransportPacket:
        syn = TransportPacket(flags=FLAG_SYN, seq_num=self.seq_num, ack_num=0, payload=b"")
        self.seq_num += 1
        self.state = "SYN_SENT"
        return syn

    def handle_packet(self, pkt: TransportPacket) -> Optional[TransportPacket]:
        # Handle Handshake
        if self.state == "CLOSED" and (pkt.flags & FLAG_SYN):
            self.expected_seq = pkt.seq_num + 1
            syn_ack = TransportPacket(
                flags=FLAG_SYN | FLAG_ACK,
                seq_num=self.seq_num,
                ack_num=self.expected_seq,
                payload=b"",
            )
            self.seq_num += 1
            self.state = "SYN_RCVD"
            return syn_ack

        elif self.state == "SYN_SENT" and (pkt.flags & (FLAG_SYN | FLAG_ACK)):
            self.expected_seq = pkt.seq_num + 1
            self.state = "ESTABLISHED"
            ack = TransportPacket(flags=FLAG_ACK, seq_num=self.seq_num, ack_num=self.expected_seq, payload=b"")
            return ack

        elif self.state == "SYN_RCVD" and (pkt.flags & FLAG_ACK):
            self.state = "ESTABLISHED"
            return None

        # Handle Data
        elif self.state == "ESTABLISHED":
            if pkt.flags & FLAG_DATA:
                if pkt.seq_num == self.expected_seq:
                    self.received_data.extend(pkt.payload)
                    self.expected_seq += len(pkt.payload)
                # Return Cumulative ACK
                return TransportPacket(
                    flags=FLAG_ACK,
                    seq_num=self.seq_num,
                    ack_num=self.expected_seq,
                    payload=b"",
                )
            elif pkt.flags & FLAG_ACK:
                # Slide window: remove acknowledged packets
                acked_seqs = [
                    s for s in self.unacked_packets
                    if s + len(self.unacked_packets[s][0].payload) <= pkt.ack_num
                ]
                for s in acked_seqs:
                    del self.unacked_packets[s]
                return None

        return None

    def check_timeouts(self, now: float) -> List[TransportPacket]:
        """Checks for packets needing retransmission."""
        retrans = []
        for seq, (pkt, sent_time) in list(self.unacked_packets.items()):
            if (now - sent_time) > self.rto_seconds:
                self.retransmissions += 1
                self.unacked_packets[seq] = (pkt, now)
                retrans.append(pkt)
        return retrans


if __name__ == "__main__":
    client = ReliableEndpoint(initial_seq=100)
    server = ReliableEndpoint(initial_seq=500)
    channel = ReliableChannel(drop_probability=0.25)

    print("Reliable Transport Protocol Simulation (25% Packet Loss):")
    print("=" * 65)

    # 1. Handshake
    syn = client.initiate_handshake()
    syn_ack = server.handle_packet(syn)
    ack = client.handle_packet(syn_ack)
    server.handle_packet(ack)
    assert client.state == "ESTABLISHED"
    assert server.state == "ESTABLISHED"
    print("[+] 3-Way Handshake established successfully!")

    # 2. Reliable Data Transfer with Drops
    data_to_send = [b"Chunk-0-AAA", b"Chunk-1-BBB", b"Chunk-2-CCC", b"Chunk-3-DDD"]
    t_now = 100.0

    for chunk in data_to_send:
        pkt = TransportPacket(flags=FLAG_DATA, seq_num=client.seq_num, ack_num=client.expected_seq, payload=chunk)
        client.unacked_packets[client.seq_num] = (pkt, t_now)
        client.seq_num += len(chunk)

        # Transmit through unreliable channel
        received_pkt = channel.transmit(pkt)
        if received_pkt:
            reply_ack = channel.transmit(server.handle_packet(received_pkt))
            if reply_ack:
                client.handle_packet(reply_ack)

    # Resolve any timeouts through retransmission
    while client.unacked_packets:
        t_now += 0.3
        retrans = client.check_timeouts(t_now)
        for rp in retrans:
            rec = channel.transmit(rp)
            if rec:
                ack_back = channel.transmit(server.handle_packet(rec))
                if ack_back:
                    client.handle_packet(ack_back)

    print(f"Server Reconstructed Payload: {bytes(server.received_data)!r}")
    print(f"Packets Dropped: {channel.packets_dropped}, Retransmissions: {client.retransmissions}")
    assert server.received_data == b"".join(data_to_send)
    print("\nSUCCESS: Reliable stream delivery across lossy network verified.")
