# Lesson 91: Metrics

> **Motto**: Metrics aggregate numerical telemetry over time, providing real-time visibility into system health, throughput, and error rates.

---

## Motto
"Metrics aggregate numerical telemetry over time, providing real-time visibility into system health, throughput, and error rates."

## Problem
Relying solely on logs to detect outages requires parsing millions of text lines while services are actively burning.

## Prediction
Instrumenting Counters, Gauges, and Histograms provides immediate numerical dashboards and automated alert triggers.

## Why this matters
Metrics answer high-level questions: Are requests succeeding? Is latency rising? Is memory stable?

## First principles
Metric Types: Counter (monotonically increasing), Gauge (current variable value), Histogram (statistical distributions).

## Mental model
```text
Request Handled -> Increment Counter(http_requests_total) + Observe Latency in Histogram(http_request_duration_seconds)
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Prometheus Python client and FastAPI instrumentation middleware.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/91-metrics/tests/ -v
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
- **Failure Injection**: Execute 50 successful requests and 5 failing requests; scrape the `/metrics` endpoint.
- Execute the experiment script:
```bash
python phases/91-metrics/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Verify that `http_requests_total{status='200'}` equals 50 and `http_requests_total{status='500'}` equals 5.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Keep metric label cardinality bounded: never use user IDs, email addresses, or raw URLs as metric label values.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: High-cardinality labels (millions of unique metric combinations) can crash Prometheus and monitoring databases.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Alerting rules (e.g. alert if 5xx rate > 1% for 2 minutes) are built directly on top of counter and rate metrics.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What is the difference between a Counter, a Gauge, and a Histogram in metrics instrumentation?
2. What is the 'metric label cardinality explosion' problem and how do you prevent it?
3. Why are metrics better suited for real-time alerting than log text searches?

## What comes next
Having understood metrics, we next discover its inherent boundaries and transition to **Latency Percentiles**.
