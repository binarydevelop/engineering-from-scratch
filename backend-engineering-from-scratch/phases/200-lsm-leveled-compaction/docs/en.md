# Lesson 200: LSM-Tree Leveled Compaction

> **Motto**: Compaction bounds read amplification and reclaims disk space by merging overlapping SSTables and eliminating deleted tombstones.

---

## The Problem
As SSTables accumulate on disk, point queries must search dozens of files (read amplification) and obsolete versions waste storage space.

## First Principles
In distributed backend systems, relying on high-level abstractions without understanding the mechanical realities of consensus quorums, binary wire protocols, storage engine compaction, and cryptographic verification inevitably leads to catastrophic production failures.

## Implementation Guide
- Explore `code/main.py` for the first-principles implementation.
- Run tests via `pytest phases/200-lsm-leveled-compaction/tests/test_phase.py`.
