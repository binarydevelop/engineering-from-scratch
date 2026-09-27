# Lesson 75: CPU-Bound Work

> **Motto**: CPU-intensive computations monopolize the processor; running them inside an async event loop or web process stalls the server.

---

## Motto
"CPU-intensive computations monopolize the processor; running them inside an async event loop or web process stalls the server."

## Problem
Calculating password hashes, resizing images, or parsing massive CSV files inside route handlers degrades API response times.

## Prediction
Offloading CPU-bound tasks to a `ProcessPoolExecutor` or dedicated background workers keeps web servers responsive.

## Why this matters
Understanding CPU vs I/O boundaries ensures that heavy calculations are isolated from interactive web requests.

## First principles
I/O Bound: Time spent waiting for network/disk -> Asyncio. CPU Bound: Time spent executing instructions -> Multiprocessing.

## Mental model
```text
Web Request -> Offload to ProcessPoolExecutor (Worker Process on CPU Core 2) -> Event Loop remains unblocked
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: FastAPI endpoint offloading CPU tasks to multiprocessing worker pools.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/75-cpu-bound-work/tests/ -v
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
- **Failure Injection**: Trigger an intensive CPU calculation in an async route; observe concurrent health checks time out.
- Execute the experiment script:
```bash
python phases/75-cpu-bound-work/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Refactor to `run_in_executor(ProcessPoolExecutor)`: observe health check responds in 2ms while CPU runs on separate core.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Size process pools based on physical CPU cores (`os.cpu_count()`) to avoid excessive context switching.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: CPU-heavy endpoints are primary targets for Denial of Service attacks; enforce strict rate limits and input size bounds.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: For sustained heavy computation, move work completely out of the API process into asynchronous queues (Celery/ARQ).
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why does `asyncio.to_thread()` fail to parallelize CPU-bound work in standard CPython?
2. How does `ProcessPoolExecutor` bypass the Python GIL for heavy computational tasks?
3. What Denial of Service risk is created by exposing an un-throttled CPU-heavy endpoint?

## What comes next
Having understood cpu-bound work, we next discover its inherent boundaries and transition to **Backpressure**.
