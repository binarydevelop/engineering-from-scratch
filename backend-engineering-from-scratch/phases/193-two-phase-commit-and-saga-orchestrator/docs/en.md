# Lesson 193: Two-Phase Commit and Saga Orchestrator

> **Motto**: 2PC provides atomic all-or-nothing consistency at the cost of blocking availability; Sagas provide high availability through forward actions and compensating rollbacks.

---

## The Problem
Microservices owning separate databases cannot perform local ACID transactions. Engineers must choose between blocking distributed locks (2PC) or asynchronous event-driven compensations (Saga).

## First Principles
In distributed backend systems, relying on high-level abstractions without understanding the mechanical realities of consensus quorums, binary wire protocols, storage engine compaction, and cryptographic verification inevitably leads to catastrophic production failures.

## Implementation Guide
- Explore `code/main.py` for the first-principles implementation.
- Run tests via `pytest phases/193-two-phase-commit-and-saga-orchestrator/tests/test_phase.py`.
