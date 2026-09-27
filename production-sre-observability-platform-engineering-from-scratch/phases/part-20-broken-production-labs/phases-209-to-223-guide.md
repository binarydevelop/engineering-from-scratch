# Phases 209 – 223: Broken Production Labs Execution Guide

> **Motto**: Understand it. Instrument it. Measure it. Break it. Detect it. Debug it. Recover it. Automate it. Improve it. Operate it.

---

## Overview

Phases 209 through 223 guide you through the 42 interactive broken-production labs in `broken-systems/`. In each lab, you start with an active failure, ambiguous symptoms, and incomplete clues.

---

## Lab Execution Protocol

For every broken lab:
1. **Navigate to the lab directory**: E.g., `cd broken-systems/lab-01-broken-alert-cpu-paging`.
2. **Read the scenario**: Review customer symptoms, error codes, and architectural background in `README.md`.
3. **Inspect the broken artifact**: Examine the broken configuration or code file.
4. **Formulate your hypothesis**: What underlying physical, networking, or architectural mechanism caused this symptom?
5. **Implement the fix**: Modify the code or configuration to restore production invariants.
6. **Verify the fix**: Run the automated test or verify with Prometheus/Tempo.
7. **Compare against the solution**: Open `broken-systems/solutions/complete-solutions-guide.md` to review the blameless postmortem, the exact fix, and the platform prevention guardrail.

---

## Matrix of Broken Labs (Phases 209 – 223)

* **Phase 209 (Lab 01)**: CPU Paging vs User Experience (Alerting)
* **Phase 210 (Lab 02)**: 40 Graphs with No Diagnostic Flow (Dashboards)
* **Phase 211 (Lab 03)**: Missing Trace Context (OpenTelemetry)
* **Phase 212 (Lab 04)**: High Cardinality `user_id` Metric (Prometheus TSDB)
* **Phase 213 (Lab 05)**: DEBUG Logging Disk Explosion (Logging)
* **Phase 214 (Lab 06)**: Collector Memory Overload (OTel Collector)
* **Phase 215 (Lab 07)**: Pod Uptime vs Checkout Success (SLOs)
* **Phase 216 (Lab 08)**: 120-Page Database Alert Storm (Alertmanager)
* **Phase 217 (Lab 09)**: Liveness Probe Death Loop (Kubernetes)
* **Phase 218 (Lab 10)**: Cascading Retry Storm (Reliability)
* **Phase 219 (Lab 11)**: Autoscaling Overwhelms Database (Capacity)
* **Phase 220 (Lab 12)**: Noisy Neighbor Thread Starvation (Bulkheads)
* **Phase 221 (Lab 13)**: Leaky Platform YAML Generator (Platform Abstractions)
* **Phase 222 (Lab 14)**: Manual Jira Ticket Gatekeeper (Platform Self-Service)
* **Phase 223 (Labs 15–42)**: Full 28-scenario enterprise failure suite (connection pool leaks, circuit breaker traps, DNS poisoning, cgroup throttling, deadlocks, backup failures, etc.).
