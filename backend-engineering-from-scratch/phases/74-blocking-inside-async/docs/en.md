# Lesson 74: Blocking Inside Async

> **Motto**: Invoking a blocking synchronous function inside an async handler halts the entire event loop, freezing all concurrent requests.

---

## Motto
"Invoking a blocking synchronous function inside an async handler halts the entire event loop, freezing all concurrent requests."

## Problem
Calling `time.sleep()`, a blocking DB driver, or a synchronous HTTP client inside an async endpoint freezes every other user on the server.

## Prediction
Offloading blocking calls to worker threads (`asyncio.to_thread`) keeps the event loop free to continue multiplexing.

## Why this matters
Blocking the event loop is the single most common cause of mysterious latency spikes in FastAPI/async backends.

## First principles
Event Loop is single-threaded: if one coroutine runs a blocking 2-second sleep, the ENTIRE loop halts for 2 seconds.

## Mental model
```text
Coroutine A: time.sleep(2.0) [BLOCKS WHOLE PROCESS] -> Coroutines B, C, D cannot process a single byte for 2.0s!
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: FastAPI standard `def` routes (run in threadpool) vs `async def` routes (run on event loop).
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/74-blocking-inside-async/tests/ -v
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
- **Failure Injection**: Send a fast ping request while another client triggers a 2-second blocking `time.sleep()` inside an `async def` route.
- Execute the experiment script:
```bash
python phases/74-blocking-inside-async/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Observe ping request latency spikes from 1ms to 2,001ms because the event loop was frozen.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Fix: Use `asyncio.to_thread(blocking_func)` or native async libraries (`httpx.AsyncClient`, `asyncpg`).
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: In FastAPI: define handlers with plain `def` if calling blocking libraries; FastAPI automatically runs them in a thread pool.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Monitor event loop lag in production: alert if event loop lag exceeds 50ms.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why does calling `time.sleep(5)` inside an `async def` route freeze requests for completely unrelated users?
2. How does FastAPI treat a route defined with `def` differently from a route defined with `async def`?
3. How does `asyncio.to_thread()` allow blocking legacy code to run safely in an async application?

## What comes next
Having understood blocking inside async, we next discover its inherent boundaries and transition to **CPU-Bound Work**.
