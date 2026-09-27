# Broken Production Systems Lab Suite (42 Interactive Labs)

> **Motto**: The only way to master production engineering is to debug real, broken systems. Real systems do not tell you the root cause; they only reveal symptoms.

---

## 1. How to Use the Broken Systems Labs

Each broken system lab is an isolated, realistic scenario reproducing a catastrophic or insidious production defect:

```text
┌───────────────────────────────┐
│     Broken Lab Scenario       │
│  - Scenario Description       │
│  - User Symptoms Observed     │
│  - Broken Configuration/Code  │
│  - Diagnostic Clues           │
└───────────────┬───────────────┘
                │
                ▼ (Investigate with Prometheus, Traces, Logs, CLI)
┌───────────────────────────────┐
│     Learner Investigation     │
│  1. What is the user symptom? │
│  2. Which signal proves it?   │
│  3. Is this cause or symptom? │
│  4. What changed?             │
└───────────────┬───────────────┘
                │
                ▼ (Verify fix against separated solution)
┌───────────────────────────────┐
│   broken-systems/solutions/   │
│  - Full Postmortem & RC       │
│  - Fixed Code & Config        │
│  - Platform Guardrail Design  │
└───────────────────────────────┘
```

---

## 2. Directory of Broken Production Labs

| Lab ID | Scenario Name | Primary Domain | Symptom Observed |
|:---|:---|:---|:---|
| **01** | `lab-01-broken-alert-cpu-paging` | Alerting | High CPU alert pages hourly while users experience 100% success |
| **02** | `lab-02-broken-dashboard-40-graphs` | Observability | 40 graphs on one screen; responders take 45 mins to find outage cause |
| **03** | `lab-03-missing-trace-context` | OpenTelemetry | Trace waterfall shows orphan child spans without parent linkage |
| **04** | `lab-04-high-cardinality-user-id` | Prometheus | Prometheus TSDB memory explodes to OOM after adding `user_id` label |
| **05** | `lab-05-logging-disk-explosion` | Logging | DEBUG logs exhaust container disk, causing database crash |
| **06** | `lab-06-collector-memory-overload` | OpenTelemetry | Collector killed by Linux OOM killer due to missing `memory_limiter` |
| **07** | `lab-07-bad-slo-pod-uptime` | SLOs | SLO dashboard reports 99.99% while customers cannot check out |
| **08** | `lab-08-alert-storm-100-pages` | Alertmanager | Database restart triggers 120 simultaneous pages to on-call engineer |
| **09** | `lab-09-liveness-probe-death-loop`| Kubernetes | Strict liveness probe terminates slow-starting pod in restart loop |
| **10** | `lab-10-cascading-retry-storm` | Reliability | Client retries without backoff multiply load 10x during recovery |
| **11** | `lab-11-autoscaling-db-bottleneck`| Capacity | HPA scales web pods to 30; PostgreSQL connection pool collapses |
| **12** | `lab-12-noisy-neighbor-starvation`| Reliability | Background reporting job exhausts shared thread pool, freezing API |
| **13** | `lab-13-broken-platform-abstraction`| Platform | Leaky manifest generator generates invalid ports and missing envs |
| **14** | `lab-14-platform-ticket-queue` | Platform | "Self-service" portal silently creates a manual Jira ticket to DevOps |
| **15** | `lab-15-unbounded-queue-memory-leak`| Capacity | Unbounded queue buffers 500,000 items until worker process OOMs |
| **16** | `lab-16-connection-pool-leak` | Database | Worker fails to return connection on error, exhausting pool |
| **17** | `lab-17-circuit-breaker-stuck-open`| Reliability | Circuit breaker timer never resets, permanently blocking traffic |
| **18** | `lab-18-proxy-timeout-mismatch`| Networking | Gateway times out in 2s while backend runs for 30s |
| **19** | `lab-19-deadlock-concurrent-updates`| Database | Concurrent checkouts update inventory rows in reverse order |
| **20** | `lab-20-dns-cache-poison-ttl` | Networking | HTTP client caches stale DNS forever after IP failover |
| **21** | `lab-21-missing-health-check-draining`| Deployment | Pod killed immediately on SIGTERM without draining in-flight TCP |
| **22** | `lab-22-head-sampling-dropping-errors`| OpenTelemetry | 1% head sampling misses 100% of rare 500 error traces |
| **23** | `lab-23-baggage-privacy-leak` | OpenTelemetry | Authorization header inadvertently forwarded in baggage |
| **24** | `lab-24-unindexed-table-scan` | Database | Full table scan locks table under concurrent load |
| **25** | `lab-25-stale-read-replica-lag`| Database | Replica lag causes user to see outdated order status |
| **26** | `lab-26-flapping-alert-hysteresis`| Alerting | Alert fires and resolves every 15s due to missing `for:` window |
| **27** | `lab-27-cgroup-cpu-quota-throttling`| Kubernetes | 100m CPU quota causes 800ms CFS latency spikes |
| **28** | `lab-28-histogram-bucket-explosion`| Prometheus | 250 histogram buckets per route exhaust Prometheus storage |
| **29** | `lab-29-missing-deadline-propagation`| SRE | Client cancels request, but downstream database query runs for 15s |
| **30** | `lab-30-slow-memory-leak-in-gc`| Capacity | In-memory cache dictionary never evicts keys |
| **31** | `lab-31-async-event-loop-blocked`| Reliability | Synchronous file read inside async route blocks entire server |
| **32** | `lab-32-missing-pod-disruption-budget`| Kubernetes | Node drain kills all API replicas simultaneously |
| **33** | `lab-33-stale-feature-flag-fallback`| Deployment | Feature flag fallback calls deprecated decommissioned endpoint |
| **34** | `lab-34-incomplete-canary-analysis`| Deployment | Canary tool only checks HTTP status; misses silent DB commit failure |
| **35** | `lab-35-split-brain-redundancy`| Reliability | Two databases accept writes independently after network partition |
| **36** | `lab-36-untested-backup-restore-fail`| Disaster Recovery| Database backup corrupted; restore drill fails during recovery |
| **37** | `lab-37-log-level-inversion` | Logging | Critical database error logged as DEBUG and filtered out |
| **38** | `lab-38-cascading-timeout-collapse`| SRE | Inverted timeout budgets cause upstream to abort before downstream finishes |
| **39** | `lab-39-collector-dropped-spans-queue`| OpenTelemetry | Collector buffer queue exhausted during network glitch |
| **40** | `lab-40-runbook-drift-outdated-cmds`| SRE | Runbook contains obsolete commands that fail during SEV-1 incident |
| **41** | `lab-41-multi-region-cross-call`| Networking | Service in us-west synchronously calls database in eu-central |
| **42** | `lab-42-golden-path-prison-override`| Platform | Platform enforces rigid framework that cannot support ML payload |

---

## 3. Solutions Separation

All comprehensive solutions, diagnostic walk-throughs, fixed configurations, and platform prevention strategies are located in **[`broken-systems/solutions/`](solutions/)**.
