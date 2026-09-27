# Part 04: Metrics & Prometheus (Phases 55 – 63)

> **Motto**: Understand it. Instrument it. Measure it. Break it. Detect it. Debug it. Recover it. Automate it. Improve it. Operate it.

---

## Overview

Part 04 covers Prometheus from first principles: the pull model, TSDB block chunking, PromQL rate mathematics, histogram quantiles, recording rules, and operational dashboard design.

---

## Key Lessons in Part 04

### 1. Prometheus Mental Model (Phase 55 & 56)
Prometheus periodically scrapes targets defined in `prometheus.yml`. Pull-based scraping provides built-in liveness detection: if a target fails to respond to scrape, `up{job="checkout-service"} == 0` triggers immediately without waiting for a heartbeat.

### 2. PromQL Rates & Reset Handling (Phase 58 & 59)
Why do we never use raw counters directly?
When a container restarts, its counter resets from 50,000 back to 0. A naive subtraction would report a negative rate. PromQL `rate()` automatically detects counter resets and extrapolates rates cleanly over the range window:
```promql
# Rate of errors per second over a 5-minute lookback window
sum(rate(http_requests_total{status=~"5.."}[5m])) by (service)
```

### 3. Histogram Quantiles (Phase 60)
Computing percentiles across distributed fleets:
```promql
# Approximate p99 latency using histogram buckets
histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service))
```

### 4. Recording Rules (Phase 61)
Pre-calculating expensive queries every 15 seconds so dashboards and alerts evaluate instantaneously.

### 5. Dashboard Anti-Patterns (Phase 63)
Avoiding the "Wall of Confusion": 50 graphs with no units, no owners, and no clear diagnostic workflow.
