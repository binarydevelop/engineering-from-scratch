# Lesson 202: Cryptographic Hashing and HMAC

> **Motto**: Never compare cryptographic hashes with standard string equality operators; timing variations leak secret bytes one character at a time.

---

## The Problem
Standard string equality checks (`==`) exit early on the first non-matching byte, enabling side-channel timing attacks that crack API signatures.

## First Principles
In distributed backend systems, relying on high-level abstractions without understanding the mechanical realities of consensus quorums, binary wire protocols, storage engine compaction, and cryptographic verification inevitably leads to catastrophic production failures.

## Implementation Guide
- Explore `code/main.py` for the first-principles implementation.
- Run tests via `pytest phases/202-cryptographic-hashing-and-hmac/tests/test_phase.py`.
