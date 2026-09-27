# Learning Guide: Production Systems, SRE & Platform Engineering

> **Motto**: Understand it. Instrument it. Measure it. Break it. Detect it. Debug it. Recover it. Automate it. Improve it. Operate it.

---

## 1. The Core Philosophy

Most engineers encounter production for the first time during an outage. They see an incomprehensible wall of Grafana dashboards, a cascade of confusing PagerDuty alerts, an esoteric Kubernetes deployment yaml, and senior engineers frantically executing shell commands they memorized over five years.

This leads to dangerous myths:
* Myth 1: *“SRE is just setting up Prometheus and Grafana dashboards.”*
* Myth 2: *“Observability is just installing an agent that collects everything.”*
* Myth 3: *“Platform Engineering is just writing Kubernetes Helm charts.”*
* Myth 4: *“Reliability means 100% uptime with zero failures.”*

This curriculum completely rejects these superficial views.

**Production engineering is the engineering discipline of making systems understandable, reliable, recoverable, scalable, and operable under real-world conditions.**

---

## 2. The Core Learning Loop

In every phase, lesson, lab, and capstone, you will follow the **13-Step Empirical Loop**:

```text
       ┌────────────────────────────────────────────────────────┐
       │                 1. USER-VISIBLE PROBLEM                │
       └───────────────────────────┬────────────────────────────┘
                                   ▼
       ┌────────────────────────────────────────────────────────┐
       │                 2. OPERATIONAL HYPOTHESIS              │
       │                   (Predict before acting)              │
       └───────────────────────────┬────────────────────────────┘
                                   ▼
       ┌────────────────────────────────────────────────────────┐
       │                 3. FIRST PRINCIPLES PREREQ             │
       │               (OS, Sockets, Protocols, Math)           │
       └───────────────────────────┬────────────────────────────┘
                                   ▼
       ┌────────────────────────────────────────────────────────┐
       │                 4. INSTRUMENT THE BEHAVIOR             │
       │                (Logs, Metrics, Traces, Spans)          │
       └───────────────────────────┬────────────────────────────┘
                                   ▼
       ┌────────────────────────────────────────────────────────┐
       │                 5. OBSERVE & MEASURE BASELINE          │
       │                 (RED, USE, p50/p95/p99 latency)        │
       └───────────────────────────┬────────────────────────────┘
                                   ▼
       ┌────────────────────────────────────────────────────────┐
       │                 6. BREAK THE SYSTEM                    │
       │          (Controlled failure & saturation injection)   │
       └───────────────────────────┬────────────────────────────┘
                                   ▼
       ┌────────────────────────────────────────────────────────┐
       │                 7. DETECT THE FAILURE                  │
       │                 (Symptom alert vs Cause alert)         │
       └───────────────────────────┬────────────────────────────┘
                                   ▼
       ┌────────────────────────────────────────────────────────┐
       │                 8. TRIAGE & FORM HYPOTHESIS            │
       │              (What changed? Who is impacted?)          │
       └───────────────────────────┬────────────────────────────┘
                                   ▼
       ┌────────────────────────────────────────────────────────┐
       │                 9. MITIGATE IMMEDIATELY                │
       │             (Stop the bleeding before debugging)       │
       └───────────────────────────┬────────────────────────────┘
                                   ▼
       ┌────────────────────────────────────────────────────────┐
       │                10. ROOT-CAUSE DEBUGGING                │
       │             (Correlate Traces -> Logs -> Metrics)      │
       └───────────────────────────┬────────────────────────────┘
                                   ▼
       ┌────────────────────────────────────────────────────────┐
       │                11. RESTORE & RECOVER STATE             │
       │            (Permanent fix & verify data integrity)     │
       └───────────────────────────┬────────────────────────────┘
                                   ▼
       ┌────────────────────────────────────────────────────────┐
       │                12. AUTOMATE RECURRING TOIL             │
       │               (Self-healing, rollback, scripts)        │
       └───────────────────────────┬────────────────────────────┘
                                   ▼
       ┌────────────────────────────────────────────────────────┐
       │           13. BUILD PLATFORM CAPABILITY / GUARDRAIL    │
       │           (Prevent this failure class structurally)    │
       └────────────────────────────────────────────────────────┘
```

---

## 3. The Signal Selection Framework

Observability is not about collecting infinite telemetry. It is about answering specific operational questions during degradation:

```text
┌───────────────────────────────────────┬─────────────────┬───────────────────────────────────────────┐
│ Operational Question                  │ Primary Signal  │ Diagnostic Mechanism                      │
├───────────────────────────────────────┼─────────────────┼───────────────────────────────────────────┤
│ Are users impacted right now?         │ Metrics (RED)   │ Error rate & p99 latency against SLO      │
│ Is overall traffic trending up?       │ Metrics         │ Counter rate aggregation over time        │
│ Which service or dependency is slow?  │ Traces          │ Distributed trace span waterfall duration │
│ What exact input caused the 500?      │ Logs            │ Structured JSON log with correlation ID   │
│ Why is this specific process slow?    │ Profile         │ CPU flame graph / memory allocation profile│
│ Is the database or host saturated?    │ Metrics (USE)   │ Connection pool / CPU / memory saturation │
└───────────────────────────────────────┴─────────────────┴───────────────────────────────────────────┘
```

---

## 4. The 15 Cardinal Principles of Production Engineering

1. **Start from the user symptom**: High CPU does not matter if users are 100% happy; low CPU is irrelevant if all checkouts return 500.
2. **Predict before measuring**: Formulate an operational hypothesis before looking at the dashboard or running a load test.
3. **Never alert on causes when you can alert on symptoms**: Don't page someone at 3 AM because a server hit 80% CPU. Page them when user requests fail or error budget burns.
4. **Actionability invariant**: Every paging alert must have a concrete operational runbook and an unambiguous action. If there is nothing for the human to do, it must not page.
5. **Mitigate before investigating root cause**: When production is burning, roll back or shed load first. Satisfy your intellectual curiosity after the customers are whole.
6. **Little's Law rules capacity**: Concurrency = Throughput × Latency ($L = \lambda W$). If dependency latency doubles, your in-flight requests double, and your thread/connection pools will collapse.
7. **Queues precede cliffs**: As resource utilization passes 70-80%, queue wait times increase non-linearly. System saturation exhibits cliff behavior, not gentle degradation.
8. **Retries without backoff and jitter are weaponized DDoS**: When a downstream service stumbles, uncoordinated client retries amplify traffic into a self-inflicted retry storm.
9. **Two copies is not automatic redundancy**: Redundancy without automated health checking, failover routing, and split-brain prevention creates two points of failure instead of one.
10. **A backup is only as good as its last restore drill**: An untested backup is not a backup; it is merely an unverified file on disk.
11. **Blameless systems thinking**: Saying "the engineer made a typo" is lazy thinking. Ask why the typo was possible, why CI didn't catch it, why canaries didn't abort it, and why rollback was slow.
12. **Toil is a tax on engineering velocity**: Measure repetitive, manual operational tasks. Automate tasks that have high frequency and low cognitive value.
13. **Platform engineering is product management**: Internal developers are users. A platform capability must solve a demonstrated, widespread friction point, not central-team ego.
14. **Golden paths, not golden cages**: The platform must make the right way the easiest way, while providing explicit escape hatches when unique business requirements demand it.
15. **Telemetry has a cost**: High-cardinality metrics, 100% un-sampled distributed traces, and unbounded debug logs will crash your collector and balloon your infrastructure bill. Design telemetry deliberately.

---

## 5. How to Complete a Phase

A phase is **NOT complete** because:
* A container started.
* A web page loaded.
* A test printed `PASSED`.

A phase is complete when:
1. You can explain the underlying operating system and networking mechanism without referencing high-level jargon.
2. You successfully predicted the failure behavior before running the experiment.
3. You gathered empirical evidence (saved in the phase `outputs/` directory) proving the state transition.
4. You can answer the **Questions for Mastery** in your own words.
5. You understand what platform capability or automation would eliminate this operational burden permanently.
