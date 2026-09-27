# Lesson 194: Protocol Buffers Wire Format and Varints

> **Motto**: Varints and ZigZag encoding pack variable-length integers into minimal bytes without sending padded zero bits across the network.

---

## The Problem
JSON serialization is verbose, text-based, and CPU-intensive to parse at scale. High-throughput distributed backends require bit-level binary serialization.

## First Principles
In distributed backend systems, relying on high-level abstractions without understanding the mechanical realities of consensus quorums, binary wire protocols, storage engine compaction, and cryptographic verification inevitably leads to catastrophic production failures.

## Implementation Guide
- Explore `code/main.py` for the first-principles implementation.
- Run tests via `pytest phases/194-protobuf-wire-format-and-varints/tests/test_phase.py`.
