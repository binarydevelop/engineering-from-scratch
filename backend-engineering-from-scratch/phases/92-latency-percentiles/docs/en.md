# Lesson 92: Latency Percentiles

> **Motto**: Arithmetic averages hide extreme latency tails; percentiles (p50, p95, p99) reveal the true user experience.

---

## Motto
"Arithmetic averages hide extreme latency tails; percentiles (p50, p95, p99) reveal the true user experience."

## Problem
An API with an 'average' latency of 25ms can easily have a p99 latency of 4,500ms, making 1 out of 100 users experience severe delays.

## Prediction
Calculating p50 (median), p95, and p99 percentile distributions exposes latency tail degradation and micro-outages.

## Why this matters
Percentiles are mandatory for defining and monitoring Service Level Objectives (SLOs) and customer SLAs.

## First principles
p50: 50% of requests are faster than this. p99: 99% of requests are faster than this; exactly 1% are slower.

## Mental model
```text
Skewed Data: 99 requests take 10ms; 1 request takes 10,000ms. Average = 109.9ms (Misleading!). p50 = 10ms. p99 = 10,000ms!
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Prometheus Histogram quantile calculations (`histogram_quantile(0.99, rate(...))`).
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/92-latency-percentiles/tests/ -v
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
- **Failure Injection**: Generate a skewed dataset of 1,000 request timings with a long tail; compare mean vs p50 vs p95 vs p99.
- Execute the experiment script:
```bash
python phases/92-latency-percentiles/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Observe how mean completely obscures the severe 5-second outliers that p99 exposes instantly.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: In microservice architectures, a single user request can trigger 50 internal calls; tail latency compounds exponentially: $P(\text{slow}) = 1 - (1 - p)^{50}$.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Set SLO alerts on p95 and p99 latency, never on arithmetic mean latency.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Tail latency is often driven by garbage collection pauses, connection pool acquisition, or database lock contention.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why is the arithmetic average (mean) dangerously misleading when evaluating API latency?
2. What does p99 latency represent in concrete operational terms?
3. Why does tail latency compound exponentially when a web request calls multiple internal microservices?

## What comes next
Having understood latency percentiles, we next discover its inherent boundaries and transition to **Tracing**.
