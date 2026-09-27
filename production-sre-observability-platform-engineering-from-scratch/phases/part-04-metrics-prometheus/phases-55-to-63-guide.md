# Phases 55 – 63: Metrics, PromQL & Prometheus TSDB

> **Motto**: Understand it. Instrument it. Measure it. Break it. Detect it. Debug it. Recover it. Automate it. Improve it. Operate it.

---

## Phase 55: Prometheus Mental Model

### Motto
"Prometheus does not record events; it samples continuous time series in a high-density chunked ring buffer."

### Problem
Engineers often treat Prometheus like a general-purpose SQL database or an event log, attempting to write individual user transactions or queries. This results in disk bloat and performance degradation.

### First Principles
Prometheus stores data in an append-only time series database (TSDB). A time series is identified by a metric name and a set of key-value label pairs. Samples consist of a float64 value and a millisecond timestamp. Data is buffered in 2-hour memory blocks (Head chunks) and flushed to disk using Gorilla XOR floating-point compression.

```text
[ Scrape Target ]  ──HTTP GET /metrics──►  [ Head Block in RAM ]
                                                    │
                                                    ▼ (Flush every 2 hours)
                                           [ Immutable Disk Chunks ]
                                           [ WAL (Write-Ahead Log) ]
```

---

## Phase 56: Pull-Based Scraping

### Motto
"Pull gives you built-in liveness; push requires a heartbeat you cannot trust."

### Mechanics
In push systems, when an agent or service dies, it stops sending data. The central server cannot tell whether the service is dead, the network is partitioned, or the service is simply idle.
In pull-based Prometheus:
* If the target does not return HTTP 200 within `scrape_timeout`, Prometheus automatically sets:
  ```promql
  up{job="checkout-service", instance="checkout:8001"} == 0
  ```
* This provides instant, zero-configuration liveness monitoring across the entire fleet.

---

## Phase 57: Time Series Representation

### Mathematical Invariant
$$\text{Time Series} = \text{Metric Name} + \{ \text{Label}_1 = \text{Val}_1, \dots, \text{Label}_n = \text{Val}_n \}$$
Samples:
$$\{ (t_0, v_0), (t_1, v_1), (t_2, v_2), \dots \}$$

---

## Phase 58: PromQL Fundamentals

### Instant Vector vs Range Vector
* **Instant Vector**: A single sample per time series evaluated at the current instant:
  ```promql
  http_requests_total{service="checkout-service"}
  ```
* **Range Vector**: A buffer of historical samples over a duration window:
  ```promql
  http_requests_total{service="checkout-service"}[5m]
  ```
Range vectors cannot be graphed directly; they must be fed into rate or statistical aggregator functions (`rate`, `increase`, `avg_over_time`).

---

## Phase 59: Counter Rates & Resets

### Why Raw Counters Lie
A counter only measures cumulative events since process startup. When a container restarts, the counter drops from 100,000 to 0.
The `rate()` function in PromQL:
1. Calculates $\frac{\Delta v}{\Delta t}$ between adjacent samples in the range vector.
2. If $v_{i+1} < v_i$, it detects a counter reset and assumes the counter started over from 0, compensating cleanly.
3. Extrapolates the rate to the edges of the time window.

---

## Phase 60: Histograms & Quantiles in Prometheus

### The Quantile Calculation
```promql
histogram_quantile(
  0.99,
  sum(rate(http_request_duration_seconds_bucket{service="checkout-service"}[5m])) by (le)
)
```
### The Bucket Boundary Rule
`histogram_quantile()` uses linear interpolation within bucket intervals. If your buckets are spaced too far apart (e.g. 0.1s to 10s), your calculated p99 will be wildly inaccurate. Always concentrate bucket boundaries around your SLO thresholds (e.g. 100ms, 250ms, 500ms).

---

## Phase 61: Recording Rules

### Motto
"Do not make 50 dashboard viewers compute the same 1-hour quantile query every 5 seconds."

### Implementation in `alerts/prometheus-rules.yaml`:
```yaml
groups:
  - name: checkout_recording_rules
    interval: 15s
    rules:
      - record: job:http_request_duration_seconds:p99
        expr: |
          histogram_quantile(
            0.99,
            sum(rate(http_request_duration_seconds_bucket{job="checkout-service"}[5m])) by (le)
          )
```

---

## Phase 62: Dashboard Design

### The Operational Flow Rule
A dashboard is an operational diagnostic instrument, not modern art. Every dashboard must follow the top-down diagnostic path:
1. **Top Row**: Am I broken right now? (RPS, 5xx Error Rate, p99 Latency against SLO).
2. **Middle Row**: Where is the bottleneck? (Dependency response times, active concurrency).
3. **Bottom Row**: What resource is constrained? (Database pool saturation, CPU throttling, memory).

---

## Phase 63: Dashboard Anti-Patterns

| Anti-Pattern | Operational Consequence | Remediation |
|:---|:---|:---|
| **50 Uncurated Panels** | Responder spends 30 minutes scanning charts during SEV-1 outage | Restrict dashboards to max 8–12 diagnostic panels |
| **CPU Everywhere** | Paging on 85% CPU while customers experience 100% success | Replace CPU panels with user-centric RED metrics |
| **Unlabelled Units** | Is this duration in ms, seconds, or minutes? | Always enforce explicit units in Grafana panel options |
| **No Ownership Metadata** | Responders do not know who maintains the service | Include owning team and runbook URL in dashboard header |
