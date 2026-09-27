# Production Readiness Review (PRR) Template

> **Motto**: Hope is not an operational strategy. A service is not production-ready because its unit tests pass; it is production-ready when its failure modes are understood, observable, and recoverable.

---

## Service Metadata
* **Service Name**:
* **Owning Team / Lead**:
* **On-Call Rotation / Escalation Path**:
* **Target Production Date**:
* **Review Date & Reviewers**:

---

## 1. Ownership & Architecture
* [ ] **Clear Service Owner**: Primary team and slack channel documented.
* [ ] **Architecture Diagram**: Data flow, network boundaries, and synchronous vs asynchronous paths documented.
* [ ] **Tier / Criticality Classification**: Tier 1 (Direct user checkout / revenue critical), Tier 2 (Internal business), Tier 3 (Batch / reporting).

## 2. Service Level Objectives (SLOs) & Error Budgets
* [ ] **Critical User Journey Identified**: Defined in terms of user experience, not infrastructure metrics.
* [ ] **SLI Equations Documented**: Specification of Good Events / Total Events.
* [ ] **Target & Window**: e.g. 99.9% availability over rolling 30-day window.
* [ ] **Error Budget Policy**: Explicit agreement on what happens when the error budget is exhausted (freeze deployments vs reliability sprint).

## 3. Capacity, Sizing & Headroom
* [ ] **Baseline Traffic Forecast**: Expected RPS, peak RPS, and growth rate over 6 months.
* [ ] **Resource Sizing**: CPU requests/limits, memory limits, and thread/event-loop configurations based on load testing data.
* [ ] **Headroom Verified**: System operates at <= 60% capacity during peak load.
* [ ] **Connection Pools**: Database and HTTP client pool sizes mathematically bounded to prevent downstream starvation.

## 4. Health Checks & Lifecycle
* [ ] **Startup Probe**: Handles initialization, schema validation, and cache pre-warming without premature termination.
* [ ] **Readiness Probe**: Reflects actual ability to process requests (fails when overloaded or worker threads saturated).
* [ ] **Liveness Probe**: Detects deadlocks or unrecoverable event-loop crashes; does NOT fail on downstream transient dependency outages.
* [ ] **Graceful Shutdown**: Intercepts `SIGTERM`, stops accepting new requests, drains in-flight requests within timeout window (e.g., 30s), closes sockets cleanly.

## 5. Telemetry & Observability
* [ ] **Resource Identity**: Emits standard OTel resource attributes (`service.name`, `service.version`, `deployment.environment`, `service.instance.id`).
* [ ] **Structured Logging**: Emits JSON logs with standard levels (`INFO`, `WARN`, `ERROR`), `timestamp`, `correlation_id`, and `trace_id`. No unredacted PII or secrets.
* [ ] **RED / Golden Signal Metrics**: Emits request rate, error rate, and duration histograms (with low-cardinality labels).
* [ ] **Distributed Tracing**: Context propagated across HTTP/gRPC boundaries using W3C TraceContext headers (`traceparent`).

## 6. Alerting & Runbooks
* [ ] **Symptom-Based Paging Alerts**: Paging on-call engineers only for user-visible impairment or imminent error budget burn.
* [ ] **Alert Actionability**: Every alert answers: "What is broken? What is the user impact? What should on-call do first?"
* [ ] **Runbooks**: Direct URL in alert annotations linking to tested operational playbooks with triage steps and rollback commands.
* [ ] **Alert Grouping & Inhibition**: Rules configured to prevent alert storms when upstream or database dependencies fail.

## 7. Dependencies & Resilience Patterns
* [ ] **Dependency Inventory**: Catalog of all databases, caches, queues, and third-party APIs with timeout configs.
* [ ] **Timeout Budgets**: Every outbound network call has explicit connect and read timeouts (never infinite).
* [ ] **Retries with Jitter**: Retries restricted to idempotent endpoints with exponential backoff and randomized jitter to prevent retry storms.
* [ ] **Circuit Breakers & Bulkheads**: Isolates slow or failing dependencies so failure cannot cascade to the entire service.
* [ ] **Graceful Degradation**: Fallback responses defined for non-critical dependencies.

## 8. Backpressure & Overload Protection
* [ ] **Bounded Queues**: All in-memory and broker queues have maximum depth limits.
* [ ] **Rate Limiting / Load Shedding**: Ability to drop non-critical requests (HTTP 429 / 503) under severe resource exhaustion to prevent total collapse.

## 9. Security & Secret Hygiene
* [ ] **Least Privilege**: Service runs as non-root user in containers. Database credentials restricted to required tables.
* [ ] **Dynamic / Externalized Secrets**: No plaintext tokens, passwords, or certificates committed in repository or environment files.
* [ ] **Dependency Vulnerability Scanning**: Container images and language dependencies scanned in CI.

## 10. Deployment, Rollback & Change Safety
* [ ] **Zero-Downtime Rollouts**: Rolling updates or canary deployments configured with readiness checks.
* [ ] **One-Command Rollback**: Verified ability to roll back to previous image version within 2 minutes.
* [ ] **Feature Flags**: High-risk new business logic guarded behind runtime toggles.
* [ ] **Database Migration Safety**: Schema migrations decoupled from code deployment (expand-contract pattern).

## 11. Backup, Restore & Disaster Recovery (DR)
* [ ] **RPO & RTO Defined**: Recovery Point Objective and Recovery Time Objective signed off.
* [ ] **Automated Backups**: Regular snapshots of persistent state.
* [ ] **Restore Drill Verified**: Verified restore of database snapshot to a clean environment within the last 90 days.
* [ ] **Multi-Zone / Multi-Instance Redundancy**: Replicas spread across distinct fault domains.

---

## Sign-Off
* [ ] **Service Tech Lead**: ____________________ Date: _________
* [ ] **SRE / Platform Reviewer**: ________________ Date: _________
