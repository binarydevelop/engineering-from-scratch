#!/usr/bin/env python3
"""
simulations/mac_switch.py
Simulates a Layer-2 Ethernet learning switch (learning bridge).
Maintains CAM table: MAC Address -> Port
Demonstrates:
  1. Source MAC Learning
  2. Unknown Unicast Flooding (flood to all ports except ingress)
  3. Known Unicast Forwarding (direct delivery to learned port)
  4. Broadcast Delivery (always flood to all ports except ingress)
  5. MAC Table Aging / Expiration
"""

import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple


@dataclass
class EthernetFrame:
    src_mac: str
    dst_mac: str
    payload: str


@dataclass
class CAMEntry:
    port: int
    last_seen_time: float


class Layer2Switch:
    def __init__(self, num_ports: int = 4, aging_time_seconds: float = 300.0):
        self.num_ports = num_ports
        self.aging_time_seconds = aging_time_seconds
        # CAM Table: MAC Address -> CAMEntry
        self.cam_table: Dict[str, CAMEntry] = {}

    def clean_aged_entries(self, current_time: Optional[float] = None) -> int:
        """Removes entries older than aging_time_seconds."""
        now = current_time if current_time is not None else time.time()
        expired = [
            mac for mac, entry in self.cam_table.items()
            if (now - entry.last_seen_time) > self.aging_time_seconds
        ]
        for mac in expired:
            del self.cam_table[mac]
        return len(expired)

    def process_frame(
        self, ingress_port: int, frame: EthernetFrame, current_time: Optional[float] = None
    ) -> Tuple[str, List[int]]:
        """
        Processes an incoming Ethernet frame on ingress_port.
        Returns: (Action Description, List of egress ports)
        """
        if ingress_port < 1 or ingress_port > self.num_ports:
            raise ValueError(f"Invalid ingress port {ingress_port}. Must be 1..{self.num_ports}")

        now = current_time if current_time is not None else time.time()

        # Step 1: Source MAC Address Learning
        learned = False
        if frame.src_mac not in self.cam_table or self.cam_table[frame.src_mac].port != ingress_port:
            learned = True
        self.cam_table[frame.src_mac] = CAMEntry(port=ingress_port, last_seen_time=now)

        # Step 2: Destination Forwarding Decision
        all_other_ports = [p for p in range(1, self.num_ports + 1) if p != ingress_port]

        # Case A: Broadcast Frame (ff:ff:ff:ff:ff:ff)
        if frame.dst_mac.lower() == "ff:ff:ff:ff:ff:ff":
            action = f"BROADCAST -> Flooded to all other ports: {all_other_ports}"
            return action, all_other_ports

        # Case B: Known Unicast (Destination MAC in CAM Table)
        if frame.dst_mac in self.cam_table:
            target_port = self.cam_table[frame.dst_mac].port
            if target_port == ingress_port:
                # Source and dest are on same port (filter / drop)
                action = f"FILTER -> Destination {frame.dst_mac} on same port {ingress_port}; frame dropped"
                return action, []
            else:
                action = f"FORWARD -> Direct unicast to Port {target_port}"
                return action, [target_port]

        # Case C: Unknown Unicast (Destination MAC not in CAM Table)
        action = f"FLOOD -> Unknown destination {frame.dst_mac}; flooded to ports {all_other_ports}"
        return action, all_other_ports


if __name__ == "__main__":
    switch = Layer2Switch(num_ports=4)

    mac_a = "52:54:00:11:11:11"  # Connected to Port 1
    mac_b = "52:54:00:22:22:22"  # Connected to Port 2
    mac_c = "52:54:00:33:33:33"  # Connected to Port 3

    print("Initial CAM Table:", switch.cam_table)
    print("=" * 65)

    # Frame 1: Host A sends to Host B (B's MAC not yet learned)
    f1 = EthernetFrame(src_mac=mac_a, dst_mac=mac_b, payload="Hello Host B")
    action, ports = switch.process_frame(ingress_port=1, frame=f1)
    print(f"1. Host A (Port 1) -> Host B ({mac_b}):")
    print(f"   {action}")
    print(f"   CAM Table: {list(switch.cam_table.keys())}")

    # Frame 2: Host B replies to Host A (A's MAC is now known on Port 1)
    f2 = EthernetFrame(src_mac=mac_b, dst_mac=mac_a, payload="Hello Host A")
    action, ports = switch.process_frame(ingress_port=2, frame=f2)
    print(f"\n2. Host B (Port 2) -> Host A ({mac_a}):")
    print(f"   {action}")
    assert ports == [1], f"Expected direct unicast to [1], got {ports}"

    # Frame 3: Host A sends to Host B again (Both MACs now learned)
    f3 = EthernetFrame(src_mac=mac_a, dst_mac=mac_b, payload="How are you?")
    action, ports = switch.process_frame(ingress_port=1, frame=f3)
    print(f"\n3. Host A (Port 1) -> Host B ({mac_b}):")
    print(f"   {action}")
    assert ports == [2], f"Expected direct unicast to [2], got {ports}"

    # Frame 4: Broadcast ARP Request from Host C
    f4 = EthernetFrame(src_mac=mac_c, dst_mac="ff:ff:ff:ff:ff:ff", payload="ARP Request: Who has 10.0.0.1?")
    action, ports = switch.process_frame(ingress_port=3, frame=f4)
    print(f"\n4. Host C (Port 3) Broadcast:")
    print(f"   {action}")
    assert ports == [1, 2, 4], f"Expected flood to [1, 2, 4], got {ports}"

    print("\nSUCCESS: Layer-2 learning switch logic validated.")
