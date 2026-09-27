#!/usr/bin/env python3
"""
Tiny LSM Tree Storage Engine From Scratch
Implements the core storage mechanics of Apache Cassandra and RocksDB:
- Volatile in-memory Memtable (sorted data buffer)
- Append-only Write-Ahead Log (WAL / Commit Log)
- Immutable on-disk Sorted String Tables (SSTables)
- Probabilistic Bloom Filters for disk-seek pruning
- Soft deletes using Tombstones
- Leveled/Size-Tiered Compaction merging SSTables and reclaiming dead space
"""

import os
import json
import hashlib
from typing import Dict, List, Optional, Tuple, Any

class BloomFilter:
    def __init__(self, size: int = 1000, num_hashes: int = 4):
        self.size = size
        self.num_hashes = num_hashes
        self.bitset = [0] * size

    def _hashes(self, item: str) -> List[int]:
        hashes = []
        for i in range(self.num_hashes):
            h = int(hashlib.md5(f"{item}:{i}".encode('utf-8')).hexdigest(), 16)
            hashes.append(h % self.size)
        return hashes

    def add(self, item: str):
        for h in self._hashes(item):
            self.bitset[h] = 1

    def contains(self, item: str) -> bool:
        # False negatives are impossible; false positives are possible
        return all(self.bitset[h] == 1 for h in self._hashes(item))

TOMBSTONE = "__LSM_TOMBSTONE__"

class SSTable:
    def __init__(self, sstable_id: int, entries: List[Tuple[str, Any]]):
        self.sstable_id = sstable_id
        # Entries must be sorted strictly by key
        self.entries = sorted(entries, key=lambda x: x[0])
        self.bloom_filter = BloomFilter()
        for k, v in self.entries:
            self.bloom_filter.add(k)

    def get(self, key: str) -> Tuple[bool, Optional[Any]]:
        # Step 1: Check Bloom Filter. If not present, key is DEFINITELY not in this SSTable!
        if not self.bloom_filter.contains(key):
            return False, None

        # Step 2: Binary search through sorted entries
        low, high = 0, len(self.entries) - 1
        while low <= high:
            mid = (low + high) // 2
            mid_key = self.entries[mid][0]
            if mid_key == key:
                return True, self.entries[mid][1]
            elif mid_key < key:
                low = mid + 1
            else:
                high = mid - 1
        return False, None

class TinyLSM:
    def __init__(self, memtable_threshold: int = 4):
        self.memtable_threshold = memtable_threshold
        self.memtable: Dict[str, Any] = {}
        self.sstables: List[SSTable] = []
        self.sstable_counter = 0
        self.commit_log: List[Tuple[str, Any]] = []

    def put(self, key: str, value: Any):
        # Step 1: Append to Commit Log for crash durability
        self.commit_log.append((key, value))
        # Step 2: Write to in-memory Memtable
        self.memtable[key] = value

        # Step 3: Flush to SSTable if threshold exceeded
        if len(self.memtable) >= self.memtable_threshold:
            self.flush()

    def delete(self, key: str):
        # In LSM Trees, a delete is an APPEND of a Tombstone!
        self.put(key, TOMBSTONE)

    def flush(self):
        if not self.memtable:
            return
        self.sstable_counter += 1
        sorted_entries = sorted(self.memtable.items())
        new_sstable = SSTable(self.sstable_counter, sorted_entries)
        # Newest SSTables are prepended to the list
        self.sstables.insert(0, new_sstable)
        self.memtable.clear()
        self.commit_log.clear()
        print(f" [FLUSH] Memtable flushed to SSTable #{new_sstable.sstable_id} ({len(sorted_entries)} keys)")

    def get(self, key: str) -> Optional[Any]:
        # Step 1: Check Memtable (most recent mutations)
        if key in self.memtable:
            val = self.memtable[key]
            return None if val == TOMBSTONE else val

        # Step 2: Check SSTables from newest to oldest
        for sstable in self.sstables:
            found, val = sstable.get(key)
            if found:
                return None if val == TOMBSTONE else val

        return None

    def compact(self):
        """Major Compaction: Merge all SSTables, discarding tombstones and stale versions"""
        if len(self.sstables) < 2:
            print(" [COMPACTION] Insufficient SSTables to compact.")
            return

        merged: Dict[str, Any] = {}
        # Iterate from oldest to newest SSTable so newer entries overwrite older
        for sstable in reversed(self.sstables):
            for k, v in sstable.entries:
                merged[k] = v

        # Discard tombstones during compaction!
        surviving = [(k, v) for k, v in merged.items() if v != TOMBSTONE]
        self.sstable_counter += 1
        compacted_sstable = SSTable(self.sstable_counter, surviving)

        old_count = len(self.sstables)
        self.sstables = [compacted_sstable]
        print(f" [COMPACTION] Merged {old_count} SSTables into 1 consolidated SSTable #{compacted_sstable.sstable_id} ({len(surviving)} live keys)")

def run_simulation():
    print("======================================================================")
    print(" TINY LSM TREE STORAGE ENGINE SIMULATION")
    print("======================================================================")

    lsm = TinyLSM(memtable_threshold=3)

    print("\n1. Writing keys to demonstrate Memtable flushes...")
    lsm.put("user:101", {"name": "Alice", "city": "Berlin"})
    lsm.put("user:102", {"name": "Bob", "city": "London"})
    lsm.put("user:103", {"name": "Charlie", "city": "Paris"})  # Triggers flush #1

    lsm.put("user:104", {"name": "Dana", "city": "Tokyo"})
    lsm.put("user:101", {"name": "Alice", "city": "Munich"})  # Update Alice in newer SSTable
    lsm.put("user:105", {"name": "Evan", "city": "Zurich"})  # Triggers flush #2

    print("\n2. Performing point lookups across Memtable & SSTables:")
    print("Get user:101 (Updated):", lsm.get("user:101"))
    print("Get user:102 (Flush 1):", lsm.get("user:102"))
    print("Get user:999 (Missing):", lsm.get("user:999"))

    print("\n3. Soft Deleting user:102 (Writing a Tombstone)...")
    lsm.delete("user:102")
    print("Get user:102 immediately after delete:", lsm.get("user:102"))
    lsm.flush()

    print(f"\n4. Pre-compaction state: {len(lsm.sstables)} SSTables exist.")
    for sst in lsm.sstables:
        print(f"   SSTable #{sst.sstable_id}: {[k for k, v in sst.entries]}")

    print("\n5. Running Compaction...")
    lsm.compact()
    print("Post-compaction keys:", [(k, v) for k, v in lsm.sstables[0].entries])
    print("Get user:102 after compaction:", lsm.get("user:102"))
    print("Conclusion: Tombstones purged, newest mutations preserved, single sequential file on disk.")

if __name__ == "__main__":
    run_simulation()
