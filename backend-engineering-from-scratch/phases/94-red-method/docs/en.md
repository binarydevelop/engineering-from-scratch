# Lesson 94: RED Method

> **Motto**: The RED Method monitors microservices through three essential operational lenses: Rate, Errors, and Duration.

---

## Motto
"The RED Method monitors microservices through three essential operational lenses: Rate, Errors, and Duration."

## Problem
Monitoring hundreds of arbitrary metrics creates dashboard fatigue without clarifying whether users are impacted.

## Prediction
Standardizing every service on Rate (RPS), Errors (failed requests), and Duration (latency) provides instant operational clarity.

## Why this matters
The RED Method is the industry standard operational framework for service-oriented backend architectures.

## First principles
Rate: Requests per second. Errors: Number of failing requests. Duration: Time taken to serve requests.

## Mental model
```text
Service Dashboard: [Rate: 2,400 RPS] | [Errors: 0.02% (HTTP 5xx)] | [Duration: p50 15ms, p99 85ms]
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Prometheus RED metrics dashboard and alert configuration.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/94-red-method/tests/ -v
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
- **Failure Injection**: Simulate a traffic spike with injected 500 errors; inspect real-time RED method calculations.
- Execute the experiment script:
```bash
python phases/94-red-method/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Verify that Rate rises to 100 RPS, Errors rise to 10%, and Duration p99 shifts dynamically.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Set alert thresholds on RED signals: alert on Error Rate > 1% and Duration p99 > target SLA.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: RED method focuses strictly on user-facing symptoms; use resource metrics (USE method: Utilization, Saturation, Errors) for hardware.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Every microservice in an organization should have an identical RED dashboard format for consistent on-call triage.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What do the three letters in the RED Method stand for?
2. How does the RED Method differ from the USE Method (Utilization, Saturation, Errors)?
3. Why should on-call alerting be based on RED signals rather than host CPU utilization?

## What comes next
Having understood red method, we next discover its inherent boundaries and transition to **Health Endpoints**.
