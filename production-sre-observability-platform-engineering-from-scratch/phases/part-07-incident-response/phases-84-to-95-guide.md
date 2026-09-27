# Phases 84 – 95: Incident Command, Triage & Live Simulations

> **Motto**: Understand it. Instrument it. Measure it. Break it. Detect it. Debug it. Recover it. Automate it. Improve it. Operate it.

---

## Phase 84: What Is an Incident?

### Motto
"An incident is an unplanned disruption to customer experience or business operations that requires coordinated, non-standard engineering response."

### Severity Classification Matrix
* **SEV-1 (Critical)**: Core revenue-generating journey down. Zero workaround. Target MTTR < 30 mins.
* **SEV-2 (Major)**: Degraded customer experience, non-critical feature outage, or workaround exists. Target MTTR < 2 hours.
* **SEV-3 (Minor)**: Internal tooling failure, non-customer-facing bug. Addressed during business hours.

---

## Phase 85: Incident Roles & Structure

```text
Incident Commander (IC)  ──► Holds the baton. Controls communication flow. Makes final calls.
        │
        ├── Operations Lead (Ops)     ──► Directs hands-on technical investigation and rollbacks.
        ├── Communications Lead (Comms)► Updates status page and drafts executive communications.
        └── Scribe                    ──► Records actions, timestamps, and metric shifts in timeline.
```

---

## Phases 86 – 90: The Incident Lifecycle & Rapid Mitigation

### The 4 Immediate Triage Questions (Phase 87)
1. **What is the user impact?** (Check RED dashboard: error rate % and p99 latency).
2. **When did it start?** (Locate the exact timestamp of metric deviation).
3. **What changed?** (Review deployments, config maps, feature flags in the 30m prior).
4. **Which systems are involved?** (Inspect distributed trace waterfalls).

### Mitigate Before Root Cause (Phase 88)
> **The SRE Cardinal Rule**: If rolling back the last deployment will safely restore customer experience, execute the rollback immediately. Do not keep production broken while you run profilers or inspect stack traces.

---

## Phases 91 – 95: The 5 Live Incident Simulations

### Simulation I: Deployment Error Spike (Phase 91)
* **Trigger**: Release of v1.4.2 introduces `AttributeError`.
* **Symptom**: Checkout error rate jumps to 28%.
* **Mitigation**: `make rollback SERVICE=checkout-service VERSION=v1.4.1`.

### Simulation II: Database Lock Contention (Phase 92)
* **Trigger**: Long-running report transaction holds exclusive row lock on `inventory`.
* **Symptom**: Checkout p99 latency climbs to 4,500ms; thread pool saturates.
* **Mitigation**: Identify blocking PID in `pg_stat_activity` and execute `SELECT pg_terminate_backend(pid);`.

### Simulation III: Upstream DNS Failure (Phase 93)
* **Trigger**: CoreDNS lookup times out for payment provider.
* **Symptom**: HTTP 504 Gateway Timeouts across all checkouts.
* **Mitigation**: Reroute traffic via backup endpoint or fallback IP in gateway configuration.

### Simulation IV: Cache Stampede (Phase 94)
* **Trigger**: Redis cache cluster flushed; thousands of concurrent requests hit un-cached database keys.
* **Symptom**: PostgreSQL CPU saturates to 100%; queries queue up.
* **Mitigation**: Enable mutual exclusion (mutex lock) on cache miss and pre-warm hot keys.

### Simulation V: Silent Queue Backlog (Phase 95)
* **Trigger**: Background consumer thread deadlocks on external SMTP call.
* **Symptom**: 0 HTTP errors; worker processing lag climbs from 100ms to 45 minutes.
* **Mitigation**: Terminate hung consumer and restart worker process.
