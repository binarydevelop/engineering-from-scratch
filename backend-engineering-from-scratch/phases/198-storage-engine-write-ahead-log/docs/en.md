# Lesson 198: Storage Engine Write-Ahead Log

> **Motto**: Durability requires that an append-only WAL record is flushed to disk via fsync before modifying volatile in-memory state.

---

## The Problem
Power outages and process crashes leave in-memory databases with corrupted or lost writes unless a deterministic replay log exists.

## First Principles
In distributed backend systems, relying on high-level abstractions without understanding the mechanical realities of consensus quorums, binary wire protocols, storage engine compaction, and cryptographic verification inevitably leads to catastrophic production failures.

## Implementation Guide
- Explore `code/main.py` for the first-principles implementation.
- Run tests via `pytest phases/198-storage-engine-write-ahead-log/tests/test_phase.py`.
