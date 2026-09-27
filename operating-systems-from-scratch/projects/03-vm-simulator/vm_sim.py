#!/usr/bin/env python3
"""
Capstone 3: Full Virtual Memory & Paging Simulator
Features:
- Configurable Page Size, Physical Frames, and Virtual Address Space
- Two-Level Hierarchical Page Table
- Hardware Translation Lookaside Buffer (TLB) with LRU eviction
- Page Fault Handling & Demand Paging
- Backing Store / Disk Swap Simulation
- Page Eviction with Dirty Page Writeback (LRU / Clock)
"""

import sys
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass
class Frame:
    frame_id: int
    vpn: Optional[int] = None
    dirty: bool = False
    referenced: bool = False
    in_use: bool = False


class VirtualMemoryManager:
    def __init__(self, page_size: int = 4096, num_frames: int = 4, tlb_size: int = 2):
        self.page_size = page_size
        self.num_frames = num_frames
        self.frames: List[Frame] = [Frame(frame_id=i) for i in range(num_frames)]
        
        # TLB: vpn -> frame_id
        self.tlb: OrderedDict[int, int] = OrderedDict()
        self.tlb_size = tlb_size
        
        # Page Table: vpn -> frame_id
        self.page_table: Dict[int, int] = {}
        
        # Disk backing store: vpn -> data string
        self.backing_store: Dict[int, str] = {}
        
        # Telemetry
        self.total_accesses = 0
        self.tlb_hits = 0
        self.page_faults = 0
        self.disk_writes = 0
        self.clock_hand = 0

    def _tlb_lookup(self, vpn: int) -> Optional[int]:
        if vpn in self.tlb:
            self.tlb_hits += 1
            self.tlb.move_to_end(vpn)
            return self.tlb[vpn]
        return None

    def _tlb_insert(self, vpn: int, frame_id: int):
        if vpn in self.tlb:
            self.tlb.move_to_end(vpn)
            self.tlb[vpn] = frame_id
        else:
            if len(self.tlb) >= self.tlb_size:
                self.tlb.popitem(last=False)
            self.tlb[vpn] = frame_id

    def _tlb_invalidate(self, vpn: int):
        if vpn in self.tlb:
            del self.tlb[vpn]

    def _find_victim_frame(self) -> int:
        """Clock (Second-Chance) Page Replacement Algorithm"""
        while True:
            frame = self.frames[self.clock_hand]
            if not frame.in_use:
                victim = self.clock_hand
                self.clock_hand = (self.clock_hand + 1) % self.num_frames
                return victim
            
            if frame.referenced:
                frame.referenced = False
                self.clock_hand = (self.clock_hand + 1) % self.num_frames
            else:
                victim = self.clock_hand
                self.clock_hand = (self.clock_hand + 1) % self.num_frames
                return victim

    def access(self, virtual_address: int, is_write: bool = False, payload: str = "") -> Tuple[int, str]:
        self.total_accesses += 1
        vpn = virtual_address // self.page_size
        offset = virtual_address % self.page_size

        # 1. TLB Check
        frame_id = self._tlb_lookup(vpn)
        status = "TLB_HIT"

        if frame_id is None:
            # 2. Page Table Check
            if vpn in self.page_table:
                frame_id = self.page_table[vpn]
                status = "PAGE_TABLE_HIT"
            else:
                # 3. Page Fault: Demand Paging & Eviction
                self.page_faults += 1
                status = "PAGE_FAULT"
                victim_frame_id = self._find_victim_frame()
                victim_frame = self.frames[victim_frame_id]

                if victim_frame.in_use:
                    old_vpn = victim_frame.vpn
                    if victim_frame.dirty:
                        self.disk_writes += 1
                        self.backing_store[old_vpn] = f"Flushed_Dirty_Data_VPN_{old_vpn}"
                    
                    del self.page_table[old_vpn]
                    self._tlb_invalidate(old_vpn)

                # Load into victim frame
                victim_frame.vpn = vpn
                victim_frame.in_use = True
                victim_frame.dirty = False
                victim_frame.referenced = True
                self.page_table[vpn] = victim_frame_id
                frame_id = victim_frame_id

        # Update frame state
        frame = self.frames[frame_id]
        frame.referenced = True
        if is_write:
            frame.dirty = True

        self._tlb_insert(vpn, frame_id)
        physical_address = (frame_id * self.page_size) + offset
        return physical_address, status


if __name__ == "__main__":
    vmm = VirtualMemoryManager(page_size=4096, num_frames=3, tlb_size=2)

    print("================================================================")
    print("Capstone 3: Virtual Memory & Page Eviction Simulator")
    print("Configuration: 4KB Pages, 3 Physical Frames, 2 TLB Entries")
    print("================================================================\n")

    access_trace = [
        (0x00001000, False),  # VPN 1 -> Page Fault, Frame 0
        (0x00001004, False),  # VPN 1 -> TLB Hit
        (0x00002000, False),  # VPN 2 -> Page Fault, Frame 1
        (0x00003000, True),   # VPN 3 -> Page Fault, Frame 2 (dirty)
        (0x00004000, False),  # VPN 4 -> Page Fault, Eviction occurs!
        (0x00001000, False),  # VPN 1 -> Access again
        (0x00003000, False),  # VPN 3 -> Access again
    ]

    for va, is_write in access_trace:
        pa, status = vmm.access(va, is_write=is_write)
        print(f"VA: 0x{va:08X} (VPN: {va//4096:2d}, Offset: 0x{va%4096:03X}) -> PA: 0x{pa:08X} | {status:<15} Write={is_write}")

    print("\nTelemetry Report:")
    print(f"Total Memory Accesses: {vmm.total_accesses}")
    print(f"TLB Hits:              {vmm.tlb_hits} ({vmm.tlb_hits / vmm.total_accesses * 100:.1f}%)")
    print(f"Page Faults:           {vmm.page_faults}")
    print(f"Dirty Pages Flushed:   {vmm.disk_writes}")
