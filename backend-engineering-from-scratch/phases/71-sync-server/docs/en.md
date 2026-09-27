# Lesson 71: Sync Server

> **Motto**: A synchronous server blocks the executing thread on every network and database I/O operation, capping concurrency.

---

## Motto
"A synchronous server blocks the executing thread on every network and database I/O operation, capping concurrency."

## Problem
A synchronous single-threaded server can only handle exactly one request at a time; all other requests queue up.

## Prediction
Measuring synchronous request processing under load demonstrates the physical limits of sequential I/O.

## Why this matters
Understanding sync servers reveals why multi-threading and asynchronous event loops were invented.

## First principles
Request 1 Arrives -> Sleep 100ms (I/O) -> Respond -> Request 2 Arrives -> Sleep 100ms... Total time = $N \times 100ms$.

## Mental model
```text
Client 1 [Processing...] -> Client 2 [Queued/Waiting...] -> Client 3 [Queued/Waiting...]
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: WSGI servers (Gunicorn sync workers) baseline performance.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/71-sync-server/tests/ -v
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
- **Failure Injection**: Send 50 concurrent requests to a sync server with a 100ms simulated database sleep.
- Execute the experiment script:
```bash
python phases/71-sync-server/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Observe total execution time takes 5.0 seconds (50 x 100ms); throughput is capped at 10 RPS.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Synchronous models require increasing worker processes to scale concurrency, consuming significant host RAM.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Slow client attacks (Slowloris) trivially exhaust sync servers by sending headers slowly and holding worker threads.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Legacy WSGI applications require large thread pools or dozens of worker processes to achieve modest concurrency.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why is a synchronous single-threaded server limited to $\frac{1}{\text{Latency}}$ requests per second?
2. What happens to incoming client connections when a sync server's listen backlog fills up?
3. How does Slowloris exploit synchronous request handling to perform denial of service?

## What comes next
Having understood sync server, we next discover its inherent boundaries and transition to **Threaded Server**.
