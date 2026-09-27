# Lesson Evidence: Phase 16 — Transactions: MULTI, EXEC, and Optimistic Locking (WATCH)

**Date:** [YYYY-MM-DD]
**Redis Version:** [e.g. 7.4.11 / 8.4.0]
**Environment:** macOS / Docker

### 1. Hypothesis & Prediction
* If a command inside a MULTI block encounters a type error (e.g. INCR on a string), does Redis roll back earlier commands in the transaction?

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
