# Lesson 203: Symmetric Encryption and Authenticated Encryption (AEAD)

> **Motto**: Encryption without authentication is dangerous; AEAD (such as AES-GCM) encrypts plaintext and cryptographically guarantees data integrity with an auth tag.

---

## The Problem
Unauthenticated ciphertexts (like AES-CBC without MAC) are vulnerable to bit-flipping and padding oracle attacks where attackers alter payloads in transit.

## First Principles
In distributed backend systems, relying on high-level abstractions without understanding the mechanical realities of consensus quorums, binary wire protocols, storage engine compaction, and cryptographic verification inevitably leads to catastrophic production failures.

## Implementation Guide
- Explore `code/main.py` for the first-principles implementation.
- Run tests via `pytest phases/203-symmetric-encryption-aes-gcm/tests/test_phase.py`.
