# Phases 236 – 243: Capstone Challenges & Final Production Mastery

> **Motto**: Understand it. Instrument it. Measure it. Break it. Detect it. Debug it. Recover it. Automate it. Improve it. Operate it.

---

## Phase 236 (Capstone 1): The Resilient Production Service

### Challenge
Build and operate the complete Tier 1 production stack:
* Reverse proxy (`api-gateway`), business orchestrator (`checkout-service`), relational store (`inventory-service` + PostgreSQL), downstream mock (`payment-service`), and async consumer (`notification-worker` + Redis).
* Every service must emit OpenTelemetry traces, Prometheus RED metrics, structured JSON logs, and handle `SIGTERM` with zero dropped requests.

---

## Phase 237 (Capstone 2): Failure-Driven SRE Challenge

### Challenge
Run `load-tests/load_generator.py` at 50 RPS. Sequentially inject the 8 failure modes using `scripts/inject-failure.sh`:
1. Slow Database Latency (2,000ms query lag)
2. Sudden Database Termination (`SIGKILL` postgres)
3. Cache Cluster Flush & Stampede
4. Upstream DNS Resolution Blackout
5. Host CPU Saturation (100% burn across all cores)
6. Progressive Memory Leak (approaching cgroup limit)
7. Connection Pool Exhaustion (holding transactions idle)
8. Regressed Deployment (`checkout-service:v1.4.2` with bug)

**For every scenario**: Document your prediction, observe detection in Alertmanager, triage in Grafana, execute safe mitigation, and author a postmortem in `outputs/`.

---

## Phase 238 (Capstone 3): Kubernetes Production Platform

### Challenge
Deploy the microservice suite to a local Kubernetes cluster (k3d or kind).
Configure:
* Accurate CPU/Memory requests based on load test data.
* Deep startup, liveness, and readiness probes.
* Horizontal Pod Autoscaling (HPA) with warm headroom.
* PodDisruptionBudgets (`minAvailable: 2`).
* OpenTelemetry Collector deployed as a DaemonSet with node enrichment.

---

## Phase 239 (Capstone 4): The Self-Service Internal Developer Platform

### Challenge
A developer runs:
> *"I need a new microservice that listens on port 8088 and connects to a private PostgreSQL database."*
Without filing an infrastructure ticket, the developer uses `platform-cli new-service` and declarative `service.yaml` to spin up the service, database, CI/CD pipeline, and Grafana dashboard in under 5 minutes.

---

## Phase 240 (Capstone 5): Platform Product Evaluation

### Challenge
Simulate 3 different product squads onboarding to the platform:
1. Squad A builds a standard REST API (Golden Path).
2. Squad B builds a high-throughput event worker (Golden Path variant).
3. Squad C builds a C++ machine learning inference service (Escape Hatch).
Measure Time to First Deploy (TTFD), configuration burden, and escape-hatch friction.

---

## Phase 241 (Capstone 6): The Major Outage War Room

### Challenge
Execute the multi-system cascading SEV-1 incident simulation:
* A 3x traffic surge occurs simultaneously with a bad deployment to payment service, which triggers a retry storm from the API gateway, completely exhausting database connection slots.
* Responders receive noisy, conflicting evidence.
* Execute incident command, stabilize the database, trip circuit breakers, roll back the deployment, shed excess load, and restore customer checkouts within 20 minutes.

---

## Phase 242 (Capstone 7): Enterprise Reliability Program

### Challenge
Design a comprehensive 6-month SRE transformation plan for a fictional company with 30 microservices, frequent midnight pages, no SLOs, and manual deployments. Prioritize investments based on risk reduction and engineering leverage.

---

## Phase 243: The Staff Production Engineering Challenge

Execute the full audit, architecture overhaul, and platform construction for *HyperScale Cloud Solutions* (80 services, high on-call noise, ticket bottlenecks, rising cloud spend) detailed in **[`capstones/final-challenge-production-engineering.md`](../../capstones/final-challenge-production-engineering.md)**.
