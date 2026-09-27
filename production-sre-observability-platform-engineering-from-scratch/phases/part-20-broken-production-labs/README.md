# Part 20: Broken Production Labs (Phases 209 – 223)

> **Motto**: Understand it. Instrument it. Measure it. Break it. Detect it. Debug it. Recover it. Automate it. Improve it. Operate it.

---

## Overview

Part 20 contains 42 hands-on, interactive broken production systems. Rather than following tutorials where everything works, you are dropped into broken environments where alerts page, services crash, collectors drop data, metrics explode, or deployments fail.

See the complete lab suite in **[`broken-systems/`](../../broken-systems/)** and the verified fixes in **[`broken-systems/solutions/`](../../broken-systems/solutions/)**.

---

## Phase Matrix

* **Phase 209 (Lab 01)**: Broken Alert: Constant CPU paging while users are unaffected
* **Phase 210 (Lab 02)**: Broken Dashboard: 40 graphs on one screen with no diagnostic flow
* **Phase 211 (Lab 03)**: Missing Trace Context: Upstream gateway drops W3C traceparent
* **Phase 212 (Lab 04)**: High Cardinality Metric: `user_id` injected into Prometheus label
* **Phase 213 (Lab 05)**: Logging Explosion: DEBUG logging in production exhausts disk
* **Phase 214 (Lab 06)**: Collector Overload: Unbounded OTel Collector queue drops traces
* **Phase 215 (Lab 07)**: Bad SLO: Measuring pod uptime while checkout API is returning 500
* **Phase 216 (Lab 08)**: Alert Storm: Single PostgreSQL outage triggers 120 simultaneous pages
* **Phase 217 (Lab 09)**: Liveness Probe Death Loop: Slow startup causes restart loop
* **Phase 218 (Lab 10)**: Cascading Retry Storm: Client retries overwhelm recovering service
* **Phase 219 (Lab 11)**: Autoscaling Failure: HPA scales API pods but PostgreSQL saturates
* **Phase 220 (Lab 12)**: Noisy Neighbor: Background report generation starves checkout API
* **Phase 221 (Lab 13)**: Broken Platform Abstraction: Leaky YAML generator causes pod failure
* **Phase 222 (Lab 14)**: Platform Ticket Queue: "Self-service" platform requires manual ticket
* **Phase 223 (Labs 15–42)**: Complete Broken Systems Suite (Unbounded queues, pool leaks, circuit breaker traps, DNS poisoning, etc.)
