# Lesson 103: Load Testing

> **Motto**: Load testing subjects a backend service to realistic concurrent traffic to measure capacity, throughput, and latency limits.

---

## Motto
"Load testing subjects a backend service to realistic concurrent traffic to measure capacity, throughput, and latency limits."

## Problem
Assuming a service will handle 500 RPS without testing guarantees surprise outages during launch day traffic surges.

## Prediction
Generating sustained concurrent traffic reveals where latency percentiles degrade and where resource bottlenecks appear.

## Why this matters
Never claim a backend is fast without empirical, reproducible load test measurements under documented conditions.

## First principles
Load Generator -> Generates Concurrent Users (RPS) -> Measures Response Codes & Latency -> Reports p50, p95, p99.

## Mental model
```text
Load Generator (20 Virtual Users) ──[HTTP POST /orders]──> Target Backend ──> Monitor RPS, p99 Latency, Error Rate
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Locust / K6 load testing scripts and execution benchmarks.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/103-load-testing/tests/ -v
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
- **Failure Injection**: Run load test starting at 50 RPS and ramp up to 500 RPS; record RPS, p50, p95, and p99 latency.
- Execute the experiment script:
```bash
python phases/103-load-testing/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Observe latency remain flat until 250 RPS; observe p99 latency spike and errors appear as capacity limit is breached.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Document exact hardware baseline: CPU cores, RAM, network bandwidth, and database configuration.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Load testing production requires careful coordination to avoid triggering DDoS protections or exhausting external APIs.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Stress testing pushes past capacity to measure recovery: does the service recover gracefully when load subsides?
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What is the difference between Load Testing, Stress Testing, and Soak Testing?
2. Why must load testing measure latency percentiles (p95/p99) rather than just average latency?
3. What symptoms indicate that a backend service has reached its maximum sustainable capacity?

## What comes next
Having understood load testing, we next discover its inherent boundaries and transition to **First Bottleneck**.
