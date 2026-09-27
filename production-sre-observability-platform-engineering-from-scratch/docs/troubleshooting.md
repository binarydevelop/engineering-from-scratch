# Production Troubleshooting: The Diagnostic Workflow

> **Motto**: When production is burning, follow the diagnostic evidence tree, not your ungrounded intuition.

---

## 1. The Systematic Diagnostic Workflow

```text
1. Check the User Symptom (RED Metrics)
   - Is Error Rate > 1%?
   - Is p99 Latency > SLO threshold?
   - Is Request Rate dropping to zero?
           │
           ▼
2. Trace the Request Path (Distributed Tracing Waterfall)
   - Open Tempo / Jaeger trace for a failing request
   - Locate the span where duration exploded or status = ERROR
   - Identify whether the bottleneck is local compute, database query, or downstream HTTP call
           │
           ▼
3. Correlate with Detailed Context (Structured Logs)
   - Filter logs by the trace ID extracted from step 2
   - Identify exact exception class, payload error, or timeout event
           │
           ▼
4. Inspect Resource Saturation (USE Metrics)
   - CPU throttling / CFS quota exhausted?
   - Database connection pool slots exhausted?
   - Thread / event loop lag elevated?
           │
           ▼
5. Check Recent Changes (Deployments & Configs)
   - Compare timestamp of incident start with recent deployment logs or git commits
   - Execute safe rollback or traffic shift
```

---

## 2. Common Production Symptoms & Root Mechanisms

| Symptom Observed | Likely Underlying Mechanism | Immediate Verification |
|:---|:---|:---|
| **Sudden latency spike across all endpoints** | Database connection pool exhaustion or unindexed query lock | Inspect `pg_stat_activity` or connection pool gauge |
| **p99 latency is 10x p50 latency** | Thread starvation, garbage collection pause, or network queueing | Inspect histogram buckets and CPU throttling metrics |
| **All requests fail with HTTP 504 Gateway Timeout** | Downstream service hanging without connection/read timeouts | Inspect trace waterfall for hung child spans |
| **Error rate jumps immediately following release** | Code regression, unhandled null reference, or missing DB migration | Inspect deployment timestamp and rollback |
| **Trace waterfall shows disconnected spans** | Missing context propagation header (`traceparent`) in upstream client | Verify outgoing HTTP headers in client requests |
| **Prometheus OOM crash loop** | Metric cardinality explosion (e.g. `user_id` added to labels) | Inspect metric series count using `tsdb analyze` |
