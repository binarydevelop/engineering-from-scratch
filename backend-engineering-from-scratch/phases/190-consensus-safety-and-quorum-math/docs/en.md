# Lesson 190: Consensus Safety and Quorum Math

> **Motto**: In an asynchronous network with crash-recovery, a majority quorum is the only invariant that guarantees no two nodes commit contradictory truths.

---

## The Problem
In distributed systems, network partitions divide nodes into isolated clusters. If minority partitions accept writes, split-brain catastrophe occurs where two masters claim conflicting updates.

## First Principles
In distributed backend systems, relying on high-level abstractions without understanding the mechanical realities of consensus quorums, binary wire protocols, storage engine compaction, and cryptographic verification inevitably leads to catastrophic production failures.

## Implementation Guide
- Explore `code/main.py` for the first-principles implementation.
- Run tests via `pytest phases/190-consensus-safety-and-quorum-math/tests/test_phase.py`.
