# Lesson Evidence: Phase 30 — Distributed Locks: Safety, TTLs, and Fencing Tokens

**Date:** [YYYY-MM-DD]
**Redis Version:** [e.g. 7.4.11 / 8.4.0]
**Environment:** macOS / Docker

### 1. Hypothesis & Prediction
* What catastrophic race occurs if Worker A takes a 10-second GC pause, its lock TTL expires, Worker B acquires the lock, and Worker A wakes up and executes `DEL lock`?

### 2. Execution Log
```text
[Paste terminal execution output here]
```

### 3. Measurements & Findings
* Latency / Throughput:
* Injected Failures:

### 4. What Was Broken & Diagnosed
* Failure:
* Fix:
