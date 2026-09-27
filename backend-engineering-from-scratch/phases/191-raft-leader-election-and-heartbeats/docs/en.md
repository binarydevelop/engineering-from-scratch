# Lesson 191: Raft Leader Election and Heartbeats

> **Motto**: A Raft node transitions through Follower, Candidate, and Leader roles using randomized election timers to avoid split votes.

---

## The Problem
Without a deterministic election protocol, multiple nodes become masters simultaneously or elections loop indefinitely under symmetric timeouts.

## First Principles
In distributed backend systems, relying on high-level abstractions without understanding the mechanical realities of consensus quorums, binary wire protocols, storage engine compaction, and cryptographic verification inevitably leads to catastrophic production failures.

## Implementation Guide
- Explore `code/main.py` for the first-principles implementation.
- Run tests via `pytest phases/191-raft-leader-election-and-heartbeats/tests/test_phase.py`.
