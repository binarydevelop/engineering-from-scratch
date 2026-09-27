# Lesson 64: Timeouts

> **Motto**: Every outbound network call must have an explicit timeout; unbounded network calls guarantee cascading failure.

---

## Motto
"Every outbound network call must have an explicit timeout; unbounded network calls guarantee cascading failure."

## Problem
When an external payment gateway or database hangs, caller threads wait indefinitely, exhausting thread pools and crashing the server.

## Prediction
Configuring connection timeouts, read timeouts, and overall request deadlines ensures requests fail fast.

## Why this matters
Timeouts bound resource consumption, allowing services to survive downstream latency spikes without collapsing.

## First principles
Connect Timeout (time to establish TCP) + Read Timeout (max time between bytes) + Request Deadline (total budget).

## Mental model
```text
Application -> HTTP Request (Timeout: 2.0s) ──[Hangs for 30s]──> Client Timeout Triggers at 2.0s -> Thread Freed!
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: HTTPX / Requests timeout configurations (`httpx.Timeout(connect=2.0, read=5.0)`).
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/64-timeouts/tests/ -v
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
- **Failure Injection**: Make an outbound call to a mock endpoint that sleeps for 10 seconds with a 1-second timeout configured.
- Execute the experiment script:
```bash
python phases/64-timeouts/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Client raises `httpx.ReadTimeout` after exactly 1.0 second; thread is freed immediately.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Always set connect timeouts short (<= 2s); read timeouts should match expected SLA (<= 5-10s).
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Unbounded timeouts allow slowloris attacks and third-party outages to propagate upstream into total outages.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Propagate overall request deadlines across microservice chains so downstream services abort work when the deadline expires.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What is the difference between a TCP connect timeout and a socket read timeout?
2. What happens to application worker threads when outbound network calls lack explicit timeouts?
3. How do distributed request deadlines prevent wasted computation across microservices?

## What comes next
Having understood timeouts, we next discover its inherent boundaries and transition to **Retries**.
