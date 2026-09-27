# Phase 49: CloudWatch

## Motto
> You cannot manage what you do not measure. Metrics are numerical telemetry; logs are structured event history.

**Type:** Hands-on Lab & Metrics Telemetry  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 02: AWS CLI, APIs, and Console  
**AWS Services Involved:** Amazon CloudWatch Metrics  
**Cost Vector:** First 10 custom metrics are free. $0.30 per custom metric per month thereafter. Be careful with dimension cardinality!  

---

## Problem
A production application is running, but operators cannot tell whether latency is 50ms or 5,000ms, or whether the system is 5 minutes away from running out of disk space.

---

## Prediction
Publishing custom metric data points to CloudWatch allows graphing numerical time-series data and aggregating by dimensions.

---

## Why this matters
CloudWatch is the primary observability backbone of AWS. Auto Scaling, billing alarms, and self-healing systems rely on its metrics.

---

## First principles
A metric is a time-ordered sequence of data points. Each data point contains: `Namespace` (container domain), `MetricName` (e.g. OrdersProcessed), `Dimensions` (key-value metadata tags for filtering), `Timestamp`, and `Value`. CloudWatch aggregates these points into statistical summaries (Average, Sum, Minimum, Maximum, p50, p95, p99).

---

## Mental model
```text
CloudWatch Telemetry Flow:
[ Application Process ] ──► PutMetricData(Namespace="Ecommerce", Metric="OrderValue", Value=99.0)
                                    │
                                    ▼
┌────────────────────────────────────────────────────────┐
│ Amazon CloudWatch Time-Series Metric Engine            │
│ Aggregations: Sum, Average, p95, p99 Latency           │
│ Dimensions: Environment=Prod, Service=Checkout         │
└──────────────────────────┬─────────────────────────────┘
                           │ Threshold Breached!
                           ▼
                  [ CloudWatch Alarm ] ──► Triggers SNS / Auto Scaling
```

---

## Architecture before AWS
Self-hosted Graphite, StatsD, Nagios, or Prometheus time-series monitoring clusters.

---

## Build the primitive
```python
# Simulating time-series metric data point
import time
metric_payload = {
    "Namespace": "LabApp",
    "MetricData": [{
        "MetricName": "LoginLatency",
        "Dimensions": [{"Name": "Region", "Value": "us-east-1"}],
        "Value": 42.5,
        "Unit": "Milliseconds",
        "Timestamp": time.time()
    }]
}
print("Telemetry Metric Payload:", metric_payload['MetricData'][0]['MetricName'])
```

---

## Use AWS
```bash
aws cloudwatch put-metric-data --namespace 'aws-from-scratch' --metric-name 'OrdersProcessed' --value 1 --unit Count
```

---

## Inspect it
```bash
aws cloudwatch list-metrics --namespace 'aws-from-scratch' --output table
```

---

## Measure it
Measure reporting delay: standard CloudWatch metrics arrive with 1-to-5 minute aggregation latency.

---

## Break it
Publish metric points with high-cardinality dimensions (e.g. using user UUID as a dimension).

---

## Diagnose it
CloudWatch creates a separate custom metric for every unique dimension combination, triggering massive monthly metric billing charges!

---

## Recover it
Use low-cardinality dimensions for metrics (Service, Region, Environment); put high-cardinality UUIDs into structured logs.

---

## Security
Applications must have IAM permission `cloudwatch:PutMetricData` to publish metrics.

---

## Cost
### Cost Warning
First 10 custom metrics are free. $0.30 per custom metric per month thereafter. Be careful with dimension cardinality!

### Resources Created
- Documented in lesson steps above.

### How to Verify Them
```bash
./scripts/list-lab-resources.sh
```

---

## Modify it
Experiment by tuning parameters, increasing capacity, changing timeouts, or tweaking security group rules. Observe metric changes in CloudWatch.

---

## Cleanup
```bash
# CloudWatch metrics automatically expire after 15 months; no manual deletion required.
```

---

## Verify cleanup
```bash
echo 'Metrics logged.'
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-49-evidence.md`.

---

## Questions for mastery
1. Why should you NEVER use user IDs or transaction IDs as CloudWatch metric dimensions?
2. What is the difference between average latency and p99 latency in a high-throughput API?
3. How does CloudWatch High-Resolution Metrics (1-second resolution) differ in cost and behavior from standard metrics?

---

## When to use this
Use CloudWatch Metrics for operational alerting, auto-scaling triggers, and high-level system dashboards.

---

## When not to use this
Do not use CloudWatch for distributed profiling traces or high-cardinality debugging (use OpenTelemetry or structured logs).

---

## What comes next
Phase 50: CloudWatch Logs — Centralized log management and retention.
