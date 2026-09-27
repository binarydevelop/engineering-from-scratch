# Lesson 148: First Service Extraction

> **Motto**: Extracting a service moves a module across a physical network boundary, incurring network, serialization, and deployment costs.

---

## Motto
"Extracting a service moves a module across a physical network boundary, incurring network, serialization, and deployment costs."

## Problem
Developers expect extracting a service to be simple, and are shocked by the sudden explosion of network timeouts, DTOs, and deployments.

## Prediction
Extracting a clean subsystem (e.g. Notification Service) demonstrates the real-world operational costs of distributed systems.

## Why this matters
Experiencing service extraction firsthand teaches respect for network boundaries and distributed fallacies.

## First principles
In-Memory Call (0.01ms, 100% reliable) -> Network Call (15ms, JSON serialization, socket timeouts, partial failures).

## Mental model
```text
Monolith -> Extract Notifications -> Monolith calls Notification Service over HTTP/Queue -> New Deployment, New Monitoring!
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Microservice client adapters and independent service deployments.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/148-first-service-extraction/tests/ -v
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
- **Failure Injection**: Benchmark latency and failure modes before extraction (in-memory) vs after extraction (HTTP network hop).
- Execute the experiment script:
```bash
python phases/148-first-service-extraction/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Observe end-to-end latency increases by 12ms; observe network drops now require retry logic and timeouts.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Implement backward-compatible API contracts between the calling monolith and the extracted service.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: The extracted service must have its own independent Git repository, CI/CD pipeline, and database.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Service extraction requires establishing correlation ID propagation and distributed tracing across the new boundary.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What immediate performance and reliability costs are incurred when extracting an in-memory module into an HTTP service?
2. Why must an extracted microservice possess its own dedicated database rather than sharing the monolith's database?
3. What new observability tools become mandatory once a system crosses its first network boundary?

## What comes next
Having understood first service extraction, we next discover its inherent boundaries and transition to **Remote Call Is Not a Function Call**.
