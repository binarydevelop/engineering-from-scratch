# The Complete 22-Part Curriculum Directory

> **Motto**: Understand it. Instrument it. Measure it. Break it. Detect it. Debug it. Recover it. Automate it. Improve it. Operate it.

---

```text
Track A: Production SRE ──────────────┐
Track B: OpenTelemetry & Observability ┼──► Reliable, Observable, Operable Production Systems
Track C: Platform Engineering ────────┘
```

---

## Curriculum Map: 22 Parts · 244 Phases

### [Part 01: Production Foundations](part-01-production-foundations/) (Phases 00 – 10)
*Operating system processes, TCP listen sockets, request lifecycles, and baseline system dynamics without telemetry.*
* **Phase 00**: Production Laboratory (`client` -> `API` -> `PostgreSQL` via Docker Compose)
* **Phase 01**: What Does Production Mean? (Real users, real state, real consequences)
* **Phase 02**: Development vs Production (1 req vs 10k concurrent requests, stateful recovery)
* **Phase 03**: Production Failure Model (10 fundamental failure domains)
* **Phase 04**: Users Experience Symptoms (Separating causes from user symptoms)
* **Phase 05**: Availability (Request-based availability vs ping uptime)
* **Phase 06**: Latency (p50, p95, p99, p99.9 quantiles; skewed tail behavior)
* **Phase 07**: Throughput (Separating request rate from system capacity)
* **Phase 08**: Saturation (Finding the first constrained resource under load)
* **Phase 09**: Queueing Dynamics (Why latency explodes non-linearly past 75% utilization)
* **Phase 10**: Little's Law ($L = \lambda W$ intuition and capacity implications)

### [Part 02: Observability From First Principles](part-02-observability-from-first-principles/) (Phases 11 – 30)
*Deriving logs, metrics, and traces from scratch before introducing third-party tools.*
* **Phase 11**: Monitoring vs Observability (Known-knowns vs unknown-unknowns)
* **Phase 12**: Signals (Metrics, logs, traces, profiles as specific answers)
* **Phase 13**: Logs From First Principles (Why raw `print()` fails in production)
* **Phase 14**: Structured Logging (Machine-queryable JSON format)
* **Phase 15**: Log Levels (DEBUG, INFO, WARN, ERROR operational semantics)
* **Phase 16**: Correlation IDs (Propagating request identity across services)
* **Phase 17**: Logging Failure Modes (Disk exhaustion, sensitive PII leaks)
* **Phase 18**: Metrics From First Principles (Counting events without string bloat)
* **Phase 19**: Counters (Monotonic rate tracking)
* **Phase 20**: Gauges (Measuring queues, concurrency, and pool limits)
* **Phase 21**: Histograms (Cumulative buckets and latency distributions)
* **Phase 22**: Metric Labels (Dimensional filtering and slicing)
* **Phase 23**: Cardinality (The exponential time-series explosion trap)
* **Phase 24**: The RED Method (Rate, Errors, Duration for services)
* **Phase 25**: The USE Method (Utilization, Saturation, Errors for hosts)
* **Phase 26**: Four Golden Signals (Latency, Traffic, Errors, Saturation)
* **Phase 27**: Distributed Tracing Motivation (Why logs fail cross-service causal chains)
* **Phase 28**: Spans (Representing operations as timed spans with attributes)
* **Phase 29**: Trace Context (W3C `traceparent` serialization over HTTP)
* **Phase 30**: The Distributed Trace (First-principles cross-service trace visualizer)

### [Part 03: OpenTelemetry](part-03-opentelemetry/) (Phases 31 – 54)
*Modern OpenTelemetry Specification, SDKs, Stable Semantic Conventions, and Collector pipelines.*
* **Phases 31–34**: Why OpenTelemetry?, Architecture (API vs SDK vs Collector), Resources, Instrumentation Scope
* **Phases 35–40**: Manual & Auto Tracing, Semantic Conventions (HTTP, DB, Messaging)
* **Phases 41–46**: OTel Metrics, Logs Bridge, Baggage Tradeoffs, Sampling (Head vs Tail), OTLP Protocol
* **Phases 47–54**: Collector from Scratch, Pipelines (Receivers, Processors, Exporters), Failure Recovery, Deployment Topologies, Pipeline Capacity

### [Part 04: Metrics & Prometheus](part-04-metrics-prometheus/) (Phases 55 – 63)
*Prometheus TSDB, pull-based scraping, PromQL from first principles, and operational dashboards.*
* **Phases 55–60**: Prometheus Mental Model, Pull Scraping, Time Series, PromQL, Counter Rates, Histograms
* **Phases 61–63**: Recording Rules, Dashboard Design, Dashboard Anti-Patterns

### [Part 05: Alerting](part-05-alerting/) (Phases 64 – 72)
*Alert philosophy, symptom-based alerting, Alertmanager routing trees, inhibition, and runbooks.*
* **Phases 64–66**: Why Alert?, Symptom vs Cause, Alert Actionability Invariant
* **Phases 67–72**: Alertmanager Architecture, Grouping, Inhibition, Silences, Fatigue Elimination, Runbooks as Code

### [Part 06: SLIs, SLOs & Error Budgets](part-06-slis-slos-error-budgets/) (Phases 73 – 83)
*User-centric reliability, mathematical error budgets, and multi-window burn-rate alerting.*
* **Phases 73–77**: Reliability as a Product, SLIs, SLOs, SLO vs SLA, Error Budgets
* **Phases 78–83**: Burn Rate Intuition, Multi-Window Multi-Burn-Rate Rules, Realistic Targets, Batch/Worker SLOs, Governance

### [Part 07: Incident Response](part-07-incident-response/) (Phases 84 – 95)
*Coordinated incident command, triage, rapid mitigation over root cause, and live simulations.*
* **Phases 84–90**: Incident Definition, ICS Roles, Incident Lifecycle, Triage Protocol, Mitigation First, Communication, Timelines
* **Phases 91–95**: Incident Simulations I – V (Deploy error spike, DB lock, DNS outage, Cache failure, Silent queue lag)

### [Part 08: Postmortems](part-08-postmortems/) (Phases 96 – 100)
*Blameless postmortem culture, multi-factor causality, and high-leverage corrective actions.*
* **Phases 96–100**: Blameless Culture, Swiss Cheese Causality, Hierarchy of Controls, Prioritization, Recurring Incident Patterns

### [Part 09: Capacity, Saturation & Overload](part-09-capacity-overload/) (Phases 101 – 114)
*Capacity modeling, load testing, connection pooling, queues, circuit breakers, and load shedding.*
* **Phases 101–107**: Capacity Planning, Headroom, Load Testing, Finding the Cliff, Connection Pools, Worker Starvation, Queue Drain Time
* **Phases 108–114**: Backpressure, Load Shedding, Retry Storms & Jitter, Timeout Budgets, Circuit Breakers, Bulkheads, Graceful Degradation

### [Part 10: Deployment Reliability](part-10-deployment-reliability/) (Phases 115 – 123)
*Change risk, health probes, graceful shutdown, rolling rollouts, canaries, and database migrations.*
* **Phases 115–123**: Deployments as Risk, Deep Health Checks, Graceful Shutdown, Rolling Rollouts, Rollback Watchers, Canaries, Blue/Green, Feature Flags, Schema Evolution

### [Part 11: Kubernetes in Production](part-11-kubernetes-in-production/) (Phases 124 – 136)
*Operating containerized production workloads, resource limits, OOMs, eviction, and disruption.*
* **Phases 124–130**: K8s as Substrate, Requests & Limits, CPU Throttling, OOMKilled Mechanics, Probe Traps, HPA, Autoscaling Lag
* **Phases 131–136**: Pod Disruption, PodDisruptionBudgets, Fault Domains, Events as Evidence, K8s Observability, Collector Topologies

### [Part 12: Reliability Engineering](part-12-reliability-engineering/) (Phases 137 – 147)
*Redundancy, failure domains, critical path analysis, fan-out probability, and disaster recovery.*
* **Phases 137–147**: Redundancy Fallacy, Fault Domains, Dependency Math, Critical Path, Fan-Out Tail Latency, Caching Traps, Replication Lag, RPO/RTO, Restore Drills, Multi-Zone, Multi-Region

### [Part 13: Chaos & Failure Engineering](part-13-chaos-failure-engineering/) (Phases 148 – 157)
*Controlled failure experiments, hypothesis validation, blast radius control, and emergency aborts.*
* **Phases 148–157**: Why Inject Failure?, Process Failure, Latency, Packet Loss, DB Outage, Cache Flush, Disk Full, CPU Burn, Memory Leak, Formal Experiment Design

### [Part 14: Production Readiness](part-14-production-readiness/) (Phases 158 – 165)
*Service ownership, dependency inventories, operational documentation, and toil reduction.*
* **Phases 158–165**: PRR Checklist, Service Ownership, Dependency Inventory, Operational Docs, Runbook Automation, Toil Definition, Toil Auditing, Automation ROI

### [Part 15: Platform Engineering Foundations](part-15-platform-engineering-foundations/) (Phases 166 – 174)
*Platform as a product, cognitive load reduction, golden paths, platform contracts, and self-service.*
* **Phases 166–174**: Why Platform Engineering?, Platform as Product, Platform vs Infra Team, Platform API, Self-Service, Golden Paths, Escape Hatches, Abstraction Leaks, Service Contracts

### [Part 16: Building a Mini Platform](part-16-building-a-mini-platform/) (Phases 175 – 188)
*Building a runnable developer platform from scratch: CLI, templates, CI, deployment, and catalogs.*
* **Phases 175–181**: Service Template, Bootstrap CLI, CI Golden Path, Declarative Deployments, Default OTel, Baseline Alerts, Secret Injection
* **Phases 182–188**: DB-as-a-Service, Queue-as-a-Service, Platform Portal, Software Catalog, Readiness Scorecards, Adoption Metrics, User Feedback

### [Part 17: Developer Experience](part-17-developer-experience/) (Phases 189 – 194)
*Measuring cognitive load, time to first deploy, reproducible dev environments, and support friction.*
* **Phases 189–194**: Cognitive Load Index, Time to First Deploy (TTFD), Reproducible Dev, Ephemeral Previews, Task-Oriented Docs, Support Burden

### [Part 18: Delivery & Change Safety](part-18-delivery-change-safety/) (Phases 195 – 200)
*CI/CD reliability, deployment metrics, progressive delivery, and automated rollbacks.*
* **Phases 195–200**: CI/CD as Production, DORA Metrics, Change Failure Rate, Mean Time to Rollback, Progressive Delivery, Automated Rollback Controllers

### [Part 19: Advanced Observability](part-19-advanced-observability/) (Phases 201 – 208)
*Trace-log correlation, exemplars, profiling, telemetry governance, privacy, and cost modeling.*
* **Phases 201–208**: Trace-to-Log, Trace-to-Metric, Exemplars, Continuous Profiling, Semantic Governance, PII Redaction, Telemetry Cost, Adaptive Sampling

### [Part 20: Broken Production Labs](part-20-broken-production-labs/) (Phases 209 – 223)
*42 Hands-on broken production scenarios where you diagnose and fix real failures.*
* **Phases 209–223**: Labs 01 to 42 (Alerts, Dashboards, Context Loss, Cardinality, Logging, Collectors, Probes, Retries, Platforms, etc.)

### [Part 21: Projects](part-21-projects/) (Phases 224 – 235)
*12 Substantial milestone projects.*
* **Phases 224–235**: Projects 01 to 12 (Instrument Service, Collector Pipeline, Dashboards, SLO Platform, Alerting Engine, Incident Simulator, Capacity Planner, PRR CLI, Bootstrap CLI, IDP Lite, Catalog, Golden Path)

### [Part 22: Capstones](part-22-capstones/) (Phases 236 – 243)
*Complete production engineering capstone projects.*
* **Phases 236–242**: Capstones 1 through 7 (Resilient Service, Failure-Driven SRE, Kubernetes Platform, Self-Service IDP, Platform Evaluation, Major Incident War Room, Enterprise Reliability Program)
* **Phase 243**: The Staff Production Engineering Challenge
