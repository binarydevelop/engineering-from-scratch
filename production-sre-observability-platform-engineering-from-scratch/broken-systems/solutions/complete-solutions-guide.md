# Comprehensive Solutions & Postmortems: Broken Production Systems Labs (Labs 01 – 42)

> **Motto**: A production postmortem is not complete when the code is fixed; it is complete when the system is architected so that class of failure cannot recur.

---

## Lab 01: Broken Alert — CPU Paging vs User Experience

### 1. Root Cause & Technical Mechanism
The alert rule was written against raw host CPU utilization (`process_cpu_seconds_total > 0.85`).
In high-throughput distributed architectures, compute saturation alone does not indicate customer impairment. A multi-threaded worker executing background compression or reporting can run at 95% CPU without degrading customer request latency or success rate. Paging a human on a cause rather than a symptom breeds alert fatigue and causes real outages to be ignored.

### 2. The Production Fix
Rewrite the alerting policy to page strictly on **symptom and error budget burn rate**. Move CPU saturation to a low-priority warning ticket or informational dashboard:

```yaml
# Fixed Alert Rule: Page on SLO Breach / High Error Rate
groups:
  - name: production_symptom_alerts
    rules:
      - alert: CheckoutHighErrorRate
        expr: |
          (
            sum(rate(http_requests_total{service="checkout-service", status=~"5.."}[2m]))
            /
            sum(rate(http_requests_total{service="checkout-service"}[2m]))
          ) > 0.01
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Checkout error rate > 1% (Paging Incident)"
          runbook_url: "https://runbooks.internal/checkout/error-spike"

      - alert: HostCPUHighInformational
        expr: process_cpu_seconds_total > 0.90
        for: 15m
        labels:
          severity: warning
        annotations:
          summary: "Host CPU high for > 15m (Informational Ticket)"
```

### 3. Platform Guardrail
The internal platform's alert linter must reject any alert tagged `severity: critical` that uses CPU or memory metrics without correlating with customer traffic or latency.

---

## Lab 02: Broken Dashboard — 40 Graphs with No Diagnostic Flow

### 1. Root Cause & Technical Mechanism
The dashboard was created organically by multiple teams adding arbitrary metric graphs (CPU, disk reads, network packets, JVM GC pauses, heap allocations, thread counts) with no visual hierarchy, no standard units, and no diagnostic pathway.
During an outage, responders experienced severe cognitive overload, taking 45 minutes to locate the failing database connection pool.

### 2. The Production Fix
Refactor the dashboard into an opinionated **RED (Rate, Errors, Duration) and USE (Utilization, Saturation, Errors)** hierarchy:
* **Top Row (Are users impacted?)**: Service RPS, 5xx Error Rate, p99 Latency.
* **Second Row (Where is the bottleneck?)**: In-flight concurrency, downstream dependency latency.
* **Third Row (What resource is saturated?)**: Database connection pool %, memory usage, CPU quota throttling.

### 3. Platform Guardrail
The platform's default dashboard template (`dashboards/red-metrics-dashboard.json`) auto-provisions this structure for every new service generated via `platform new-service`.

---

## Lab 03: Missing Trace Context — The Orphan Span Outage

### 1. Root Cause & Technical Mechanism
An upstream service generated a span but forwarded outgoing HTTP requests without serializing the active span context into the W3C `traceparent` header.
Downstream services inspected incoming HTTP headers, found no `traceparent`, and assumed they were receiving a root request, generating a new independent `trace_id`. The distributed trace was severed into isolated fragments.

### 2. The Production Fix
Extract the span context and format it as `00-{trace_id}-{span_id}-{flags}`:
```python
traceparent = f"00-{span.context.trace_id}-{span.context.span_id}-01"
headers["traceparent"] = traceparent
```

### 3. Platform Guardrail
The platform provides an HTTP client wrapper (`services.common.context.get_forward_headers`) that automatically injects W3C trace context into every outbound request.

---

## Lab 04: High Cardinality Metric — Prometheus OOM Crash Loop

### 1. Root Cause & Technical Mechanism
A developer added `user_id` or `order_id` as a label on `http_requests_total`.
With 1,000,000 active users, Prometheus generated 1,000,000 independent time-series memory chunks. The TSDB head block memory exploded, triggering the Linux kernel OOM killer and killing Prometheus.

### 2. The Production Fix
Remove high-cardinality identifiers from Prometheus metrics. Retain strictly bounded labels: `service`, `method`, `route` (parameterized template like `/orders/{id}`), and `status`. High-cardinality values belong exclusively in distributed trace span attributes or structured log fields:
```python
# CORRECT: Low-cardinality metric
HTTP_REQUESTS_TOTAL.labels(service="checkout", method="POST", route="/orders/{id}", status="200").inc()

# High-cardinality data placed in span attribute
span.set_attribute("user.id", user_id)
span.set_attribute("order.id", order_id)
```

### 3. Platform Guardrail
The platform CI pipeline inspects all Prometheus metric definitions with an AST linter to disallow variable user IDs or UUID patterns in label arrays.

---

## Lab 05: Logging Disk Explosion — DEBUG in Production

### 1. Root Cause & Technical Mechanism
An engineer troubleshooting an issue in staging pushed code with `LOG_LEVEL=DEBUG` into production. Under 2,000 RPS, the application wrote 250 MB of raw log text per minute to the container scratch disk, filling the ephemeral partition, preventing the database from writing WAL logs, and crashing the host.

### 2. The Production Fix
1. Enforce default production log level `INFO`.
2. Configure dynamic log-level adjustment via admin endpoint with an automatic 15-minute expiration timer.
3. Configure container log rotation (`max-size: "50m"`, `max-file: "3"`).

---

## Lab 06: Collector Memory Overload — Missing Memory Limiter

### 1. Root Cause & Technical Mechanism
The OpenTelemetry Collector was deployed without the `memory_limiter` processor, or the `memory_limiter` was placed after the `batch` processor. Under a network slowdown, the Collector buffered millions of spans in memory until it exceeded container memory limits and crashed.

### 2. The Production Fix
Place `memory_limiter` as the very first processor in every pipeline:
```yaml
processors:
  memory_limiter:
    check_interval: 1s
    limit_percentage: 75
    spike_limit_percentage: 20
```

---

## Lab 07: Bad SLO — Measuring Pod Uptime Instead of User Journey

### 1. Root Cause & Technical Mechanism
The team defined their SLO as: "Kubernetes pods must report Ready 99.99% of the time."
During an outage, the payment gateway failed all credit card charges with HTTP 500. Because the pods were healthy and their basic `/healthz` probe returned 200, the SLO dashboard reported 100% compliance while 0% of customers could buy products.

### 2. The Production Fix
Anchor the SLI to the **Critical User Journey (CUJ)**:
$$\text{SLI} = \frac{\text{Successful Checkout HTTP POST requests with Latency} \le 500\text{ms}}{\text{Total Valid Checkout Attempts}}$$

---

## Lab 08: Alert Storm — Single Database Outage Triggers 120 Pages

### 1. Root Cause & Technical Mechanism
When PostgreSQL was restarted for maintenance, every single microservice and background worker emitted an independent critical alarm. The on-call engineer received 120 text messages in 2 minutes.

### 2. The Production Fix
Configure Alertmanager **Grouping** and **Inhibition**:
```yaml
inhibit_rules:
  - source_match:
      alertname: 'DatabaseDown'
    target_match:
      severity: 'critical'
    equal: ['environment']
```
When `DatabaseDown` fires, all downstream service failure alerts are automatically suppressed.

---

## Lab 09: Liveness Probe Death Loop — Slow Startup

### 1. Root Cause & Technical Mechanism
A service required 25 seconds on startup to load cache state from the database. The Kubernetes deployment had a liveness probe with `initialDelaySeconds: 5` and `periodSeconds: 5`.
After 15 seconds, Kubernetes determined the pod was dead, sent `SIGKILL`, and started a new pod, entering an infinite CrashLoopBackOff.

### 2. The Production Fix
Introduce a dedicated **`startupProbe`**:
```yaml
startupProbe:
  httpGet:
    path: /healthz
    port: 8080
  failureThreshold: 30
  periodSeconds: 2
livenessProbe:
  httpGet:
    path: /healthz
    port: 8080
  periodSeconds: 10
```
Kubernetes disables liveness checks until the startup probe has successfully passed.

---

## Lab 10: Cascading Retry Storm — Unbounded Client Retries

### 1. Root Cause & Technical Mechanism
Downstream payment service experienced a brief 2-second hiccup. Upstream checkout services retried immediately without backoff. The retries doubled incoming traffic to payment service, preventing it from recovering, causing further timeouts, triggering more retries, and collapsing the entire architecture.

### 2. The Production Fix
1. Implement **Exponential Backoff with Full Jitter**:
   $$\text{sleep} = \text{random}(0, \min(M, B \cdot 2^{\text{attempt}}))$$
2. Enforce a **Client-Side Circuit Breaker** that trips open after 5 consecutive failures, failing fast for 15 seconds.

---

## Labs 11 – 20 Summaries & Fixes

* **Lab 11 (Autoscaling DB Bottleneck)**: HPA scaled API pods, exhausting PostgreSQL connection limits. Fix: Set database connection pool ceilings and implement PgBouncer or connection multiplexing.
* **Lab 12 (Noisy Neighbor Thread Starvation)**: Background PDF generation ran in the default HTTP event thread pool. Fix: Use Bulkhead pattern with an isolated background worker thread pool.
* **Lab 13 (Broken Platform Abstraction)**: Manifest generator omitted container port declaration. Fix: Add schema validation against Kubernetes OpenAPI spec in `platform generate-manifests`.
* **Lab 14 (Platform Ticket Queue)**: "Self-service" required Jira approvals. Fix: Convert infrastructure approval into automated policy-as-code guardrails (Open Policy Agent).
* **Lab 15 (Unbounded Queue Memory Leak)**: Queue had no max capacity; producer overwhelmed consumer. Fix: Enforce bounded queue depth with drop-tail or HTTP 429 backpressure.
* **Lab 16 (Connection Pool Leak)**: DB connection not closed on exception. Fix: Wrap database cursor acquisitions in `try...finally` or context managers (`with db.connection()`).
* **Lab 17 (Circuit Breaker Stuck Open)**: Cooldown timer never decremented due to monotonic clock bug. Fix: Store `time.monotonic()` and check elapsed recovery duration before testing half-open state.
* **Lab 18 (Proxy Timeout Mismatch)**: Nginx timeout was 2s while backend worker timeout was 30s. Fix: Align timeout budgets so upstream timeout is always strictly greater than downstream timeout.
* **Lab 19 (Deadlock Concurrent Updates)**: Threads updated accounts A and B in opposite order. Fix: Enforce deterministic locking order (sort IDs before acquiring row locks).
* **Lab 20 (DNS Cache Poison TTL)**: Client cached DNS IP indefinitely. Fix: Set JVM/HTTP client DNS TTL to 30-60 seconds.

---

## Labs 21 – 42 Summaries & Fixes

* **Lab 21 (Missing Health Check Draining)**: Container dropped active TCP sockets on SIGTERM. Fix: Register SIGTERM signal handler, stop accepting new connections, and sleep 5s before process exit.
* **Lab 22 (Head Sampling Dropping Errors)**: 1% head sampling missed rare 500 error traces. Fix: Implement Tail-Based Sampling in the OpenTelemetry Collector to sample 100% of spans where `status.code == ERROR`.
* **Lab 23 (Baggage Privacy Leak)**: Authorization bearer token put in OTel Baggage. Fix: Redact credentials and enforce baggage attribute whitelists.
* **Lab 24 (Unindexed Database Scan)**: Missing index caused sequential scan on orders table. Fix: Run `EXPLAIN ANALYZE` and create composite index on `(user_id, created_at)`.
* **Lab 25 (Stale Read Replica Lag)**: Client read updated profile from lagging replica. Fix: Implement read-your-own-writes session token routing writes and immediate reads to primary database.
* **Lab 26 (Flapping Alert Hysteresis)**: Metric bounced around threshold every 10s. Fix: Add `for: 2m` evaluation hold window to Prometheus alert rule.
* **Lab 27 (cgroup CPU Quota Throttling)**: CFS quota throttled multi-threaded burst. Fix: Increase or remove CPU limits while keeping CPU requests accurate for scheduling.
* **Lab 28 (Histogram Bucket Explosion)**: 250 custom buckets per route. Fix: Consolidate to standard exponential buckets (10 buckets max).
* **Lab 29 (Missing Deadline Propagation)**: Cancelled requests continued running downstream queries. Fix: Propagate cancellation tokens via context deadline.
* **Lab 30 (Slow Memory Leak in GC)**: Global dict cached items without TTL or LRU eviction. Fix: Replace raw dict with an LRU cache with maxsize and TTL eviction.
* **Lab 31 (Async Event Loop Blocked)**: Synchronous `open().read()` blocked asyncio loop. Fix: Offload blocking I/O to threadpool via `asyncio.to_thread`.
* **Lab 32 (Missing PodDisruptionBudget)**: Cluster node drain evicted all pods simultaneously. Fix: Configure `PodDisruptionBudget` with `minAvailable: 2`.
* **Lab 33 (Stale Feature Flag Fallback)**: Flag evaluation default pointed to dead service. Fix: Audit and clean up retired feature flag code paths.
* **Lab 34 (Incomplete Canary Analysis)**: Canary passed HTTP 200 checks while failing DB commits. Fix: Extend canary analysis to evaluate business transactions and database error rates.
* **Lab 35 (Split-Brain Redundancy)**: Network partition created dual write masters. Fix: Implement Quorum consensus (Raft/Paxos) requiring $N/2 + 1$ votes for leader election.
* **Lab 36 (Untested Backup Restore Failure)**: Backup file was 0 bytes due to silent pipe failure. Fix: Schedule monthly automated backup restore verification drills to isolated staging DB.
* **Lab 37 (Log Level Inversion)**: Critical failure logged as `logger.debug()`. Fix: Correct log level to `logger.error(..., exc_info=True)`.
* **Lab 38 (Cascading Timeout Collapse)**: Timeout budgets configured backwards. Fix: Service A (10s) -> Service B (5s) -> Service C (2s).
* **Lab 39 (Collector Dropped Spans Queue Full)**: Collector buffer overflowed during network hiccup. Fix: Increase `queued_retry` buffer and implement tail-drop backpressure.
* **Lab 40 (Runbook Drift Outdated Commands)**: Runbook referenced decommissioned endpoints. Fix: Treat runbooks as code; execute them in CI against disposable staging environments.
* **Lab 41 (Multi-Region Cross-Call)**: Cross-continental network call added 200ms latency per request. Fix: Keep critical read/write path localized to single region with asynchronous cross-region replication.
* **Lab 42 (Golden Path Prison Override)**: Platform blocked custom Dockerfile needed for ML inference. Fix: Provide explicit platform escape hatch with container compliance test suite.
