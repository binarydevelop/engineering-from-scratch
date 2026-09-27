# Lesson 199: LSM-Tree MemTable and SSTable

> **Motto**: An LSM-Tree converts random disk writes into high-speed sequential writes by buffering in a MemTable and flushing immutable Sorted String Tables (SSTables).

---

## The Problem
B-Tree in-place updates require random disk I/O, causing write amplification and poor throughput under heavy write workloads.

## First Principles
In distributed backend systems, relying on high-level abstractions without understanding the mechanical realities of consensus quorums, binary wire protocols, storage engine compaction, and cryptographic verification inevitably leads to catastrophic production failures.

## Implementation Guide
- Explore `code/main.py` for the first-principles implementation.
- Run tests via `pytest phases/199-lsm-memtable-and-sstable/tests/test_phase.py`.
