# Lesson 107: Memory Leaks

> **Motto**: Memory leaks in Python occur when unneeded objects remain referenced in global data structures, evading garbage collection.

---

## Motto
"Memory leaks in Python occur when unneeded objects remain referenced in global data structures, evading garbage collection."

## Problem
An unconstrained global dictionary cache or circular reference structure causes process RAM to grow until the OS OOM-kills the server.

## Prediction
Diagnosing memory growth with `tracemalloc` and `gc` exposes objects retained in memory across requests.

## Why this matters
Fixing memory leaks prevents unexpected server restarts, keeps memory usage predictable, and lowers cloud hosting costs.

## First principles
Python uses Reference Counting + Generational Garbage Collection. Retained references in global scope cannot be freed.

## Mental model
```text
Request Arrives -> Appends user data to global list -> Request finishes -> Memory NEVER FREED -> Process OOM killed!
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Python `tracemalloc` and `psutil` process memory inspection.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/107-memory-leaks/tests/ -v
```

## Inspect it
Observe state directly using operating system, network, or database inspection:
- Inspect raw bytes, socket buffers, or table schemas
- Verify that request transformations match protocol specifications

## Measure it
Quantify latency and resource consumption:
- Measure response latency percentiles (p50, p95, p99)
- Profile memory allocations and database connection usage under load

## Break it
Inject an intentional failure to observe divergence from expected behavior:
- **Failure Injection**: Send 1,000 requests to an endpoint with an unbounded in-memory cache; observe memory RSS grow continuously.
- Execute the experiment script:
```bash
python phases/107-memory-leaks/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Run `tracemalloc.take_snapshot()`; diff snapshots to identify the exact line of code allocating retained memory.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Replace unbounded in-memory collections with bounded LRU caches (`cachetools.LRUCache`) or external Redis storage.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Memory leaks in containers trigger Linux Out-Of-Memory (OOM) killer; check `dmesg | grep -i oom` when containers die silently.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Be cautious with closures, event listeners, and global variables that capture large request context dictionaries.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. How does Python's reference counting garbage collector determine when an object's memory can be reclaimed?
2. What tools allow you to compare memory snapshots and identify leaking objects in a running Python backend?
3. Why should in-memory caches in long-running web servers always enforce a maximum size limit (LRU)?

## What comes next
Having understood memory leaks, we next discover its inherent boundaries and transition to **Connection Leaks**.
