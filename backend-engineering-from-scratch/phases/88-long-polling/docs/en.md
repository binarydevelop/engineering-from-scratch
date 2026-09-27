# Lesson 88: Long Polling

> **Motto**: Long polling simulates real-time push updates over standard HTTP by holding a request open until new data is available.

---

## Motto
"Long polling simulates real-time push updates over standard HTTP by holding a request open until new data is available."

## Problem
Standard short polling sends continuous HTTP requests every second, creating massive server load and empty response waste.

## Prediction
Holding the HTTP request open on the server until an event occurs returns data immediately while minimizing redundant traffic.

## Why this matters
Understanding long polling explains the historical evolution of real-time web protocols and fallback mechanisms.

## First principles
Client sends GET -> Server has no data: Holds request open -> Data arrives: Server responds -> Client immediately sends next GET.

## Mental model
```text
Client GET /updates ──[Holds open 30s]──> Data Arrives at second 12 -> Returns 200 with Data -> Client immediately loops
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: FastAPI long polling endpoint with timeout management.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/88-long-polling/tests/ -v
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
- **Failure Injection**: Send request; verify it holds for up to 5 seconds if no data is published, returning 204/empty; then publish data and observe instant response.
- Execute the experiment script:
```bash
python phases/88-long-polling/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Measure server connection hold behavior and client re-connection loops.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Always enforce a server-side timeout on long-polling connections (e.g. 30 seconds) to prevent gateway timeouts.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Long polling generates high connection churn and HTTP header overhead compared to persistent WebSockets or SSE.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Long polling remains valuable as a universal zero-infrastructure fallback when WebSockets are blocked by proxies.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. How does Long Polling reduce server load compared to naive Short Polling?
2. Why must a long-polling request always enforce a maximum timeout window?
3. What overhead does Long Polling incur that persistent WebSockets eliminate?

## What comes next
Having understood long polling, we next discover its inherent boundaries and transition to **Logging**.
