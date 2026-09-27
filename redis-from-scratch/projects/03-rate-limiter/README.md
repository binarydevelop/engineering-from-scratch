# Project 03: Distributed Rate Limiting Engines

A comprehensive implementation and systems comparison of three distributed rate-limiting architectures.

---

## Algorithm Comparison Matrix

| Property | Fixed Window | Sliding Window Log | Token Bucket (Lua) |
| :--- | :--- | :--- | :--- |
| **Redis Primitive** | `INCR` + `EXPIRE` | Sorted Set (`ZSET`) | Hash + Lua Script (`EVAL`) |
| **Time Complexity** | $O(1)$ | $O(\log N + M)$ | $O(1)$ |
| **Memory Footprint** | ~60 bytes per key | Scales with request count (high) | ~120 bytes per key |
| **Burst Boundary Spike** | **Vulnerable** (2x limit at window edges) | None (perfect sliding window) | Smooth (controlled burst capacity) |
| **Concurrency Race Safety** | Safe | Potential race without MULTI | **100% Atomic** via Lua script |

---

## How to Run

```bash
make up
python3 projects/03-rate-limiter/limiter.py
```
