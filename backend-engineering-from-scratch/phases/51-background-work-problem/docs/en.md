# Lesson 51: Background Work Problem

> **Motto**: Executing slow, non-essential operations synchronously inside an HTTP request degrades latency and exhausts server capacity.

---

## Motto
"Executing slow, non-essential operations synchronously inside an HTTP request degrades latency and exhausts server capacity."

## Problem
Sending an email or generating a PDF synchronously inside an HTTP handler locks the worker thread for 5 seconds.

## Prediction
Offloading slow side effects to background execution returns immediate HTTP responses in 10ms while work finishes out-of-band.

## Why this matters
Synchronous external dependencies make your API latency hostage to third-party availability and network delays.

## First principles
Request -> Fast Domain Mutation -> Trigger Background Task -> Return HTTP 202/200 in 10ms -> Worker handles slow task.

## Mental model
```text
Synchronous (Bad): Client waits 5.2s (API + Email) -> Asynchronous (Good): Client receives 200 in 15ms; Worker sends Email
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: FastAPI BackgroundTasks and asynchronous task dispatching.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/51-background-work-problem/tests/ -v
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
- **Failure Injection**: Inject a 3-second network delay in a third-party email provider stub inside a route handler.
- Execute the experiment script:
```bash
python phases/51-background-work-problem/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Observe client request takes 3,015ms; refactor to background execution; observe client request takes 12ms.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Return HTTP 202 Accepted when a requested operation is accepted for background processing.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: In-process background tasks run in the same memory space and can consume application CPU/memory if unmanaged.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: If the application server crashes or restarts, in-process background tasks in memory are permanently lost.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why should sending transactional emails never be executed synchronously in an HTTP request handler?
2. What HTTP status code specifically signifies that a request has been accepted for background processing?
3. What happens to in-process background tasks if the application server process receives a SIGKILL or crashes?

## What comes next
Having understood background work problem, we next discover its inherent boundaries and transition to **In-Process Background Work**.
