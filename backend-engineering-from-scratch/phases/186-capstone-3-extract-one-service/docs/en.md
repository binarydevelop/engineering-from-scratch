# Lesson 186: Capstone 3: Extract One Service

> **Motto**: Extract the Notification Service from Capstone 1 into an independent microservice, implementing remote contracts and retries.

---

## Motto
"Extract the Notification Service from Capstone 1 into an independent microservice, implementing remote contracts and retries."

## Problem
Extracting microservices blindly introduces distributed failures; extracting a justified service demonstrates real trade-offs.

## Prediction
Moving the notification subsystem across a network boundary introduces HTTP/event interfaces, timeouts, and independent scaling.

## Why this matters
This capstone proves when and how to extract a service cleanly while comparing operational complexity before and after.

## First principles
Monolith (In-Memory Module) -> Service Extraction -> Monolith calls Notification Service over Network (HTTP/Queue).

## Mental model
```text
Monolith ──[Async Queue / HTTP Adapter with Timeout]──> Standalone Notification Service (Own DB, Own Workers, Own Deploy)
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Microservice extraction and inter-service communication.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/186-capstone-3-extract-one-service/tests/ -v
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
- **Failure Injection**: Run end-to-end checkout on the monolith; verify notification event is transmitted across network and processed by the extracted service.
- Execute the experiment script:
```bash
python phases/186-capstone-3-extract-one-service/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Simulate network failure between monolith and notification service; verify monolith continues operating without downtime.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Compare complexity before vs after: document new failure modes, deployment requirements, and latency overhead.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: The extracted service must own its own data store and deploy via an independent pipeline.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Use asynchronous event-driven communication (message queue) rather than synchronous HTTP whenever possible for decoupled services.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What new architectural failure modes were introduced when extracting the Notification Service?
2. Why is the monolith able to continue processing orders even when the extracted Notification Service is completely offline?
3. What operational overheads (deployments, monitoring, networks) did the service extraction introduce?

## What comes next
Having understood capstone 3: extract one service, we next discover its inherent boundaries and transition to **Capstone 4: Production Readiness Review**.
