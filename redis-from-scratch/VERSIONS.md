# Redis Version Discipline and Reference Specifications

> **Motto:** Understand it. Build it. Measure it. Break it. Fix it. Scale it. Ship it.

This repository enforces strict version discipline. Systems programming education fails when instructors mix observable abstractions with outdated internal implementation details.

---

## 1. Pinned Reference Release

| Component | Pinned Version | Docker Tag / Source Baseline | Notes |
| :--- | :--- | :--- | :--- |
| **Redis Server (Docker)** | **7.4.x** (specifically `7.4.11-alpine`) | `redis:7-alpine` | Official Linux container baseline |
| **Redis Server (Host/Local)** | **7.4.x - 8.4.x** | `redis-server` on macOS / Linux | Compatible observable commands |
| **Redis CLI** | **7.4.x+** | `redis-cli` | Supports RESP2 and RESP3 inspection |
| **Python Runtime** | **3.11+ / 3.12+ / 3.14** | `python3` | Uses standard library `socket`, `asyncio`, `time` |
| **Protocol Default** | **RESP2** (with RESP3 covered) | RESP2 (`*`, `$`, `+`, `-`, `:`) | Baseline wire protocol |

---

## 2. Public Redis Abstractions vs. Internal Implementation Details

A central tenet of this curriculum is distinguishing **what the client observes** from **how the engine is implemented**.

### A. Data Encodings (Redis 7.x vs Historical Versions)
* **Historical (< 7.0):** Redis historically used `ziplist` (compressed doubly linked list encoded in a single memory buffer) for small lists, hashes, and sorted sets.
* **Modern (7.0+ & 7.4+):** Redis replaced `ziplist` with **`listpack`** across hashes and sorted sets, and **`quicklist`** (a two-level doubly linked list of listpacks) for lists.
* **Observable CLI:** You can inspect this with `OBJECT ENCODING <key>`. You will observe `listpack` or `quicklist`, never `ziplist` on modern Redis.

### B. Memory Allocator
* On Linux (Docker), Redis is linked against **`jemalloc`** by default (`malloc=jemalloc-5.3.0`). This provides fine-grained allocation statistics and active defragmentation (`active-defrag`).
* On macOS (Homebrew / local), Redis is typically compiled against system **`libc malloc`** (`malloc=libc`).
* **Observable Difference:** `INFO memory` will report allocator metadata. Certain jemalloc-specific metrics (like `allocator_frag_ratio`) will only show meaningful values under jemalloc.

### C. Protocol: RESP2 vs. RESP3
* Redis 6.0 introduced RESP3 (which supports maps, sets, booleans, and attributes), but **RESP2 remains the default handshake** protocol for standard clients unless explicitly upgraded using `HELLO 3`.
* This course starts by building raw RESP2 parsers from first principles, then explores RESP3 enhancements.

### D. Single-Threaded Core vs. Multi-Threaded I/O
* **The Core:** The key-value execution engine, command dispatch, and data structure manipulation remain **single-threaded** per event loop. Atomicity of commands stems from this sequential execution.
* **Threaded I/O (Redis 6.0+):** Network socket reading, parsing of input buffers, and writing output buffers can be offloaded to background I/O threads when `io-threads` is enabled (> 1). However, command execution itself is never run concurrently across keys in the core engine.

---

## 3. Verification Commands

Run these commands to verify your local runtime matches the course expectations:

```bash
# Check Redis Server version and allocator
redis-server --version
# Expected output sample:
# Redis server v=7.4.11 sha=... malloc=jemalloc-5.3.0 bits=64

# Check Redis CLI version
redis-cli --version

# Check runtime memory and allocator in CLI
redis-cli INFO server | grep redis_version
redis-cli INFO memory | grep mem_allocator
```

If your local system runs Redis 8.x, all exercises remain 100% compatible. Any behavioral differences between versions are explicitly highlighted in the lesson notes.
