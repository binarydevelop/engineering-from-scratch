# Lesson 205: Zero-Trust PASETO and Service Identity

> **Motto**: Never allow token algorithms to be chosen by callers; PASETO eliminates JWT header injection attacks through rigid versioned cryptographic primitives.

---

## The Problem
JWT's infamous `alg: none` vulnerability and key-confusion attacks allow attackers to forge tokens. Modern architectures require cryptographically strict tokens and SPIFFE IDs.

## First Principles
In distributed backend systems, relying on high-level abstractions without understanding the mechanical realities of consensus quorums, binary wire protocols, storage engine compaction, and cryptographic verification inevitably leads to catastrophic production failures.

## Implementation Guide
- Explore `code/main.py` for the first-principles implementation.
- Run tests via `pytest phases/205-zero-trust-paseto-and-service-identity/tests/test_phase.py`.
