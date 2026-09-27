# Lesson 54: Worker Architecture

> **Motto**: Worker architecture separates the stateless HTTP request-serving tier from background job-processing consumer processes.

---

## Motto
"Worker architecture separates the stateless HTTP request-serving tier from background job-processing consumer processes."

## Problem
Running heavy background tasks on the same processes handling HTTP requests degrades web throughput and responsiveness.

## Prediction
Decoupling web API processes from worker processes allows independent scaling, deployment, and resource allocation.

## Why this matters
Worker architectures allow backend systems to handle millions of background jobs without impacting web user experience.

## First principles
Web Tier: High concurrency, fast I/O, low latency. Worker Tier: Heavy compute, long-running tasks, retry loops.

## Mental model
```text
Client -> Web API Server (Scale by RPS) -> Task Queue -> Worker Processes (Scale by Queue Depth)
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Production worker pools using Celery, RQ, or ARQ.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/54-worker-architecture/tests/ -v
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
- **Failure Injection**: Saturate worker queue with 1,000 image-processing jobs; verify that the web API continues serving requests at < 10ms.
- Execute the experiment script:
```bash
python phases/54-worker-architecture/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Observe web response latency remains unaffected while worker CPU scales independently.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Scale worker processes based on queue depth metrics: $\text{Workers} = \frac{\text{Queue Depth}}{\text{Target Processing Time}}$.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Worker processes often run with different operating system permissions and network firewalls than web frontends.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Separate process memory ensures a memory leak in a background report generator does not crash the web server.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why should background worker processes run in separate operating system processes from web API servers?
2. What operational metrics dictate when to scale the worker tier versus the web API tier?
3. How does process isolation protect web servers from memory leaks in background tasks?

## What comes next
Having understood worker architecture, we next discover its inherent boundaries and transition to **Retry**.
