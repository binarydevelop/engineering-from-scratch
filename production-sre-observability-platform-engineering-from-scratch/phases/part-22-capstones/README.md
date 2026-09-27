# Part 22: Capstones & Final Challenges (Phases 236 – 243)

> **Motto**: Understand it. Instrument it. Measure it. Break it. Detect it. Debug it. Recover it. Automate it. Improve it. Operate it.

---

## Overview

Part 22 presents 7 comprehensive production capstones culminating in the **Staff Production Engineering Challenge** (Phase 243). These capstones test your ability to design, instrument, operate, triage, mitigate, automate, and build platforms for complex distributed systems under real-world scaling and outage pressures.

See the complete capstone specifications and playbooks in **[`capstones/`](../../capstones/)**.

---

## Capstones Directory

* **Phase 236 (Capstone 1)**: **The Resilient Production Service**: Multi-tier architecture (Gateway, Checkout, Inventory, Payment, DB, Cache) with full OTel instrumentation, Prometheus metrics, SLOs, alerts, and graceful shutdown.
* **Phase 237 (Capstone 2)**: **Failure-Driven SRE Challenge**: Injecting 8 live failures (DB slowdown, network drop, memory pressure, bad deploy) under load; detecting, mitigating, and authoring postmortems.
* **Phase 238 (Capstone 3)**: **Kubernetes Production Platform**: Running multi-service workloads with CPU requests/limits, deep probes, HPA, PodDisruptionBudgets, and OTel Collector DaemonSets.
* **Phase 239 (Capstone 4)**: **The Self-Service Internal Developer Platform**: Declarative developer API (`service.yaml`) provisioning compute, database, and telemetry with zero tickets.
* **Phase 240 (Capstone 5)**: **Platform Product Evaluation**: Measuring developer TTFD, cognitive load reduction, and developer satisfaction via surveys and telemetry.
* **Phase 241 (Capstone 6)**: **The Major Outage War Room**: Simulated multi-system cascading SEV-1 incident with noisy, incomplete evidence under time pressure.
* **Phase 242 (Capstone 7)**: **Enterprise Reliability Program**: Designing a 6-month SRE and Observability transformation for a 30-service organization.
* **Phase 243 (Final Challenge)**: **The Staff Production Engineering Challenge**: Complete audit, architecture overhaul, and platform construction for an 80-service SaaS company.
