# Lesson 70: Concurrency Model

> **Motto**: Backend concurrency determines how a server handles multiple simultaneous requests: processes, threads, or event loops.

---

## Motto
"Backend concurrency determines how a server handles multiple simultaneous requests: processes, threads, or event loops."

## Problem
Choosing async for CPU-heavy tasks or threads for millions of idle sockets leads to catastrophic performance collapse.

## Prediction
Understanding the differences between OS processes, threads, and async event loops matches workloads to architectures.

## Why this matters
The Python GIL limits multi-threading for CPU-bound work, making multi-processing or asynchronous I/O necessary.

## First principles
Processes (Separate Memory, Heavy) vs OS Threads (Shared Memory, Preemptive) vs Asyncio (Single Thread, Cooperative).

## Mental model
```text
Processes: Fork Memory -> OS Threads: Context Switch Overhead -> Async: Non-blocking epoll event loop
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Uvicorn worker process management and asyncio concurrency.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/70-concurrency-model/tests/ -v
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
- **Failure Injection**: Spawn 10,000 idle tasks in threads vs 10,000 idle tasks in asyncio.
- Execute the experiment script:
```bash
python phases/70-concurrency-model/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Observe threads exhaust OS memory and throw `RuntimeError: can't start new thread`; asyncio handles 10,000 tasks in < 50MB RAM.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Use Asyncio for high-concurrency I/O-bound workloads; use multiprocessing for CPU-bound tasks.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Shared memory concurrency in threads introduces race conditions requiring mutexes; async eliminates race conditions across I/O awaits.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Modern Python backends typically run multiple worker processes (one per CPU core), each running an async event loop.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What is the physical memory and resource difference between an operating system thread and an asyncio task?
2. Why does the Python Global Interpreter Lock (GIL) prevent multi-threaded CPU parallelization?
3. When is an asynchronous event loop superior to a multi-threaded server architecture?

## What comes next
Having understood concurrency model, we next discover its inherent boundaries and transition to **Sync Server**.
