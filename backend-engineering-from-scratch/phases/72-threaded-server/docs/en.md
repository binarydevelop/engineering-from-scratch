# Lesson 72: Threaded Server

> **Motto**: A multi-threaded server spawns or pools operating system threads to process multiple I/O-bound requests concurrently.

---

## Motto
"A multi-threaded server spawns or pools operating system threads to process multiple I/O-bound requests concurrently."

## Problem
Spawning an unbounded number of threads per request causes OS thread exhaustion, high memory usage, and context switch thrashing.

## Prediction
Using a bounded thread pool allows concurrent request execution while preventing thread exhaustion.

## Why this matters
Multi-threaded architectures are standard for blocking I/O workloads where async drivers are unavailable.

## First principles
Each thread has its own call stack (8MB default on Linux) and is scheduled preemptively by the OS kernel.

## Mental model
```text
Thread Pool (Size: 20) -> Distributes 20 concurrent requests -> Threads execute in parallel across I/O waits
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Gunicorn gthread worker architecture.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/72-threaded-server/tests/ -v
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
- **Failure Injection**: Send 500 concurrent requests to a server with thread pool size = 10.
- Execute the experiment script:
```bash
python phases/72-threaded-server/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Observe 10 requests process concurrently; remaining 490 queue safely; system remains stable without crashing.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Size thread pools based on available RAM: $\text{Max Threads} = \frac{\text{Available RAM}}{\text{Thread Stack Size}}$.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Shared mutable state across threads requires thread synchronization (locks, mutexes) to avoid race conditions.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Preemptive context switching overhead increases exponentially when thread count exceeds hundreds per CPU core.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What causes thread thrashing when an operating system runs thousands of active threads?
2. Why must shared mutable memory be protected by mutexes in a multi-threaded server?
3. How does a bounded thread pool prevent Out-Of-Memory crashes under heavy traffic?

## What comes next
Having understood threaded server, we next discover its inherent boundaries and transition to **Async Server**.
