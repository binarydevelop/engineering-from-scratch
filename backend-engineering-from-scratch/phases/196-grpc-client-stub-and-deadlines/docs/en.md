# Lesson 196: gRPC Client Stub and Deadline Propagation

> **Motto**: In distributed microservices, a client must propagate a strict timeout deadline downstream; otherwise orphaned workers burn server resources long after callers have disconnected.

---

## The Problem
Cascading timeouts occur when an upstream gateway aborts after 2s while downstream databases and workers continue computing for 30s.

## First Principles
In distributed backend systems, relying on high-level abstractions without understanding the mechanical realities of consensus quorums, binary wire protocols, storage engine compaction, and cryptographic verification inevitably leads to catastrophic production failures.

## Implementation Guide
- Explore `code/main.py` for the first-principles implementation.
- Run tests via `pytest phases/196-grpc-client-stub-and-deadlines/tests/test_phase.py`.
