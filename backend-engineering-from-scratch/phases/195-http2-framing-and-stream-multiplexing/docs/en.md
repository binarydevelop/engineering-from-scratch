# Lesson 195: HTTP/2 Framing and Stream Multiplexing

> **Motto**: HTTP/2 multiplexes hundreds of concurrent logical request/response streams across a single long-lived TCP connection using 9-byte binary frame headers.

---

## The Problem
HTTP/1.1 suffers from Head-of-Line (HoL) blocking where a slow response stalls all subsequent requests on that TCP socket.

## First Principles
In distributed backend systems, relying on high-level abstractions without understanding the mechanical realities of consensus quorums, binary wire protocols, storage engine compaction, and cryptographic verification inevitably leads to catastrophic production failures.

## Implementation Guide
- Explore `code/main.py` for the first-principles implementation.
- Run tests via `pytest phases/195-http2-framing-and-stream-multiplexing/tests/test_phase.py`.
