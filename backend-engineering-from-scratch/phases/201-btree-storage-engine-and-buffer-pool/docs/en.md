# Lesson 201: B+ Tree Storage Engine and Buffer Pool

> **Motto**: B+ Trees store all payload data in linked leaf pages, keeping internal navigation nodes small so huge fanouts allow terabytes of data in 3-4 disk hops.

---

## The Problem
Naive memory caching causes memory exhaustion. Database storage engines require a fixed-size Buffer Pool Manager that evicts clean/dirty pages via LRU policies.

## First Principles
In distributed backend systems, relying on high-level abstractions without understanding the mechanical realities of consensus quorums, binary wire protocols, storage engine compaction, and cryptographic verification inevitably leads to catastrophic production failures.

## Implementation Guide
- Explore `code/main.py` for the first-principles implementation.
- Run tests via `pytest phases/201-btree-storage-engine-and-buffer-pool/tests/test_phase.py`.
