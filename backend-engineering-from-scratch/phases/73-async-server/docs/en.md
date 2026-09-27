# Lesson 73: Async Server

> **Motto**: An asynchronous server uses non-blocking I/O multiplexing and a single-threaded event loop to handle thousands of concurrent connections.

---

## Motto
"An asynchronous server uses non-blocking I/O multiplexing and a single-threaded event loop to handle thousands of concurrent connections."

## Problem
Managing 10,000 concurrent long-polling connections with threads requires 80GB of RAM and crashes the server.

## Prediction
Using an event loop with non-blocking sockets (`select`/`epoll`/`kqueue`) handles 10,000 connections in under 50MB of RAM.

## Why this matters
Async architectures power high-performance modern web gateways, chat servers, and real-time streaming APIs.

## First principles
Event Loop: Polling OS `epoll` -> Socket ready for read -> Resume coroutine -> Yield on next I/O -> Zero thread context switches.

## Mental model
```text
Event Loop ──[Polls epoll]──┬──> Socket 1 (Ready) -> Resume Coroutine A
                            └──> Socket 2 (Waiting) -> Paused in RAM (few KB)
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: FastAPI running on Uvicorn ASGI event loop.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/73-async-server/tests/ -v
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
- **Failure Injection**: Send 1,000 concurrent requests to the async server with a 100ms simulated `asyncio.sleep` I/O delay.
- Execute the experiment script:
```bash
python phases/73-async-server/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: All 1,000 requests complete in ~105ms total time; throughput exceeds 9,000 RPS on a single CPU core.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Async only speeds up *waiting* (I/O-bound tasks); it does not speed up CPU-bound calculations.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Non-blocking sockets cannot be read synchronously; attempting to use blocking libraries in async handlers destroys the event loop.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Async server architectures are the standard foundation for modern real-time WebSockets and SSE pipelines.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. How does OS non-blocking I/O multiplexing (`epoll`/`kqueue`) allow one thread to manage 10,000 sockets?
2. Why does an async server complete 1,000 I/O requests in 105ms while a single-threaded sync server takes 100 seconds?
3. Why is async NOT faster than synchronous code for CPU-bound computations?

## What comes next
Having understood async server, we next discover its inherent boundaries and transition to **Blocking Inside Async**.
