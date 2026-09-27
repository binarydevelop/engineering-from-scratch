# Lesson 204: TLS Handshake and mTLS Verification

> **Motto**: Mutual TLS (mTLS) transforms the network perimeter into identity: both client and server cryptographically verify each other before transmitting a single byte.

---

## The Problem
Traditional firewalls and internal networks assume traffic within the VPC is trustworthy, leaving microservices defenseless against insider lateral movement.

## First Principles
In distributed backend systems, relying on high-level abstractions without understanding the mechanical realities of consensus quorums, binary wire protocols, storage engine compaction, and cryptographic verification inevitably leads to catastrophic production failures.

## Implementation Guide
- Explore `code/main.py` for the first-principles implementation.
- Run tests via `pytest phases/204-tls-handshake-and-mtls-verification/tests/test_phase.py`.
