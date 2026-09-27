#!/usr/bin/env python3
"""
Virtual Memory Translation Simulator
Simulates address translation from Virtual Address to Physical Address via:
- Multi-level Page Table (Two-level: Page Directory -> Page Table -> Frame)
- Translation Lookaside Buffer (TLB) cache with LRU eviction
- Page Fault detection and frame allocation
- Memory protection bits (Read / Write / Execute)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from collections import OrderedDict


@dataclass
class PageTableEntry:
    frame_number: int
    present: bool = True
    readable: bool = True
    writable: bool = True
    executable: bool = False
    dirty: bool = False
    accessed: bool = False


class TLB:
    """Translation Lookaside Buffer with LRU replacement."""
    def __init__(self, capacity: int = 4):
        self.capacity = capacity
        # maps vpn -> frame_number
        self.cache: OrderedDict[int, int] = OrderedDict()
        self.hits = 0
        self.misses = 0

    def lookup(self, vpn: int) -> Optional[int]:
        if vpn in self.cache:
            self.hits += 1
            self.cache.move_to_end(vpn)
            return self.cache[vpn]
        self.misses += 1
        return None

    def insert(self, vpn: int, frame_number: int):
        if vpn in self.cache:
            self.cache.move_to_end(vpn)
            self.cache[vpn] = frame_number
        else:
            if len(self.cache) >= self.capacity:
                self.cache.popitem(last=False)  # Evict oldest (LRU)
            self.cache[vpn] = frame_number

    def invalidate(self):
        self.cache.clear()


class VirtualMemorySystem:
    def __init__(self, page_size: int = 4096, tlb_size: int = 4, max_frames: int = 16):
        self.page_size = page_size
        self.tlb = TLB(capacity=tlb_size)
        self.max_frames = max_frames
        self.free_frames = list(range(max_frames))
        # Two-level page table: directory_idx -> (page_idx -> PageTableEntry)
        self.page_directory: Dict[int, Dict[int, PageTableEntry]] = {}
        self.page_faults = 0
        self.total_translations = 0

    def map_page(self, vpn: int, readable: bool = True, writable: bool = True, executable: bool = False) -> int:
        """Explicitly allocates a physical frame for a virtual page number."""
        dir_idx = (vpn >> 10) & 0x3FF
        tbl_idx = vpn & 0x3FF

        if dir_idx not in self.page_directory:
            self.page_directory[dir_idx] = {}

        if not self.free_frames:
            raise MemoryError("Physical memory exhausted! No free frames available.")

        frame = self.free_frames.pop(0)
        entry = PageTableEntry(
            frame_number=frame,
            present=True,
            readable=readable,
            writable=writable,
            executable=executable
        )
        self.page_directory[dir_idx][tbl_idx] = entry
        return frame

    def translate(self, virtual_address: int, is_write: bool = False) -> Tuple[int, str]:
        """
        Translates a virtual address into physical address.
        Returns: (physical_address, diagnostic_source)
        """
        self.total_translations += 1
        offset = virtual_address % self.page_size
        vpn = virtual_address // self.page_size

        # 1. Check TLB
        cached_frame = self.tlb.lookup(vpn)
        if cached_frame is not None:
            phys_addr = (cached_frame * self.page_size) + offset
            return phys_addr, "TLB_HIT"

        # 2. Page Table Walk
        dir_idx = (vpn >> 10) & 0x3FF
        tbl_idx = vpn & 0x3FF

        if dir_idx not in self.page_directory or tbl_idx not in self.page_directory[dir_idx]:
            # Page Fault! Demand page allocation simulation
            self.page_faults += 1
            allocated_frame = self.map_page(vpn, readable=True, writable=True)
            self.tlb.insert(vpn, allocated_frame)
            phys_addr = (allocated_frame * self.page_size) + offset
            return phys_addr, "PAGE_FAULT (Demand Allocated)"

        entry = self.page_directory[dir_idx][tbl_idx]
        if not entry.present:
            self.page_faults += 1
            allocated_frame = self.map_page(vpn)
            self.tlb.insert(vpn, allocated_frame)
            phys_addr = (allocated_frame * self.page_size) + offset
            return phys_addr, "PAGE_FAULT (Not Present)"

        if is_write and not entry.writable:
            raise PermissionError(f"Segmentation fault: write violation on read-only page (VPN: {vpn})")

        entry.accessed = True
        if is_write:
            entry.dirty = True

        # Insert translation into TLB for subsequent accesses
        self.tlb.insert(vpn, entry.frame_number)
        phys_addr = (entry.frame_number * self.page_size) + offset
        return phys_addr, "PAGE_TABLE_WALK"


if __name__ == "__main__":
    vmm = VirtualMemorySystem(page_size=4096, tlb_size=2, max_frames=8)

    print("================================================================")
    print("Virtual Memory Address Translation Simulation")
    print("Page size: 4096 bytes (12-bit offset). TLB capacity: 2 entries.")
    print("================================================================\n")

    access_trace = [
        (0x00001040, False),  # VPN 1, Offset 0x040 -> Page Fault (alloc frame 0)
        (0x00001080, False),  # VPN 1, Offset 0x080 -> TLB Hit
        (0x00002004, False),  # VPN 2, Offset 0x004 -> Page Fault (alloc frame 1)
        (0x00003010, False),  # VPN 3, Offset 0x010 -> Page Fault (alloc frame 2, evicts VPN 1 from TLB)
        (0x00001090, False),  # VPN 1, Offset 0x090 -> TLB Miss (Page Table Walk, frame 0)
        (0x00002010, True),   # VPN 2, Offset 0x010 -> Page Table Walk, write marked dirty
    ]

    for va, is_write in access_trace:
        pa, source = vmm.translate(va, is_write=is_write)
        print(f"VA: 0x{va:08X} (VPN: {va//4096:2d}, Offset: 0x{va%4096:03X}) -> PA: 0x{pa:08X} | {source}")

    print("\nSimulation Statistics:")
    print(f"Total Translations: {vmm.total_translations}")
    print(f"TLB Hits:           {vmm.tlb.hits}")
    print(f"TLB Misses:         {vmm.tlb.misses}")
    print(f"TLB Hit Ratio:      {vmm.tlb.hits / vmm.total_translations * 100:.1f}%")
    print(f"Page Faults:        {vmm.page_faults}")
