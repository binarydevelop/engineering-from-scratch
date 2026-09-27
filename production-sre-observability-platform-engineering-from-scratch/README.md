# Production SRE, Observability & Platform Engineering from Scratch

<p align="center">
  <b>Understand it. Instrument it. Measure it. Break it. Detect it. Debug it. Recover it. Automate it. Improve it. Operate it.</b>
</p>

<p align="center">
  <a href="VERSIONS.md"><img src="https://img.shields.io/badge/OpenTelemetry-v1.34.0-3553ff?style=flat-square" alt="OpenTelemetry"></a>
  <a href="VERSIONS.md"><img src="https://img.shields.io/badge/Prometheus-v2.53.0-3553ff?style=flat-square" alt="Prometheus"></a>
  <a href="ROADMAP.md"><img src="https://img.shields.io/badge/phases-244-3553ff?style=flat-square" alt="244 Phases"></a>
  <a href="ROADMAP.md"><img src="https://img.shields.io/badge/parts-22-3553ff?style=flat-square" alt="22 Parts"></a>
  <a href="broken-systems/"><img src="https://img.shields.io/badge/broken_labs-40+-e02424?style=flat-square" alt="Broken Labs"></a>
  <a href="projects/"><img src="https://img.shields.io/badge/projects-12-059669?style=flat-square" alt="Projects"></a>
  <a href="capstones/"><img src="https://img.shields.io/badge/capstones-7-7c3aed?style=flat-square" alt="Capstones"></a>
</p>

---

> ### This is NOT a Grafana tutorial.
> ### This is NOT a Kubernetes operations cheat sheet.
> ### This is NOT a collection of SRE vocabulary.
> ### This is a course in operating reliable production systems.

---

## The Target Mental Model

The goal of this curriculum is to take you from writing isolated code to operating real distributed systems under production conditions.

When a user clicks checkout, a request flows through the entire stack:

```text
user request
     ↓
load balancer / reverse proxy
     ↓
API Gateway
     ↓
Checkout Service
     ↓
Payment Service  ───► External Payment Provider
     ↓
Inventory Service
     ↓
PostgreSQL Database / Redis Cache
     ↓
HTTP 200 OK / Response Payload
```

As a production engineer, Site Reliability Engineer (SRE), or platform engineer, you do not just write code or look at dashboards. You simultaneously reason about:

```text
logs · metrics · traces · resource usage · SLOs · alerts · dependencies · capacity · failure domains · deployments
```

And when something goes wrong at 3:00 AM, you are trained to immediately answer:

```text
Is the user affected?
How badly?
Since when?
What changed?
Which component is responsible?
Is this a symptom or a cause?
Is the service overloaded?
Is the dependency unhealthy?
Did a deployment cause it?
Can we mitigate safely?
How do we prevent recurrence?
Can this operational task be automated?
Should the platform make this failure harder to create?
```

The target mental model is:

> **Production engineering is the discipline of making systems understandable, reliable, recoverable, scalable, and operable under real-world conditions.**

---

## The Progression

```text
Service
  ↓
Production Signals
  ↓
Metrics / Logs / Traces
  ↓
OpenTelemetry SDK & OTLP
  ↓
OpenTelemetry Collector Pipelines
  ↓
SLIs & SLOs
  ↓
Error Budgets & Multi-Window Burn Rates
  ↓
Alertmanager & Actionable Runbooks
  ↓
Incident Response & Rapid Mitigation
  ↓
Blameless Postmortems & Systemic Actions
  ↓
Capacity Planning & Little's Law
  ↓
Overload Engineering & Circuit Breakers
  ↓
Deployment Safety & Automated Rollback
  ↓
Kubernetes Production Operations
  ↓
Chaos Engineering & Fault Injection
  ↓
Production Readiness Reviews
  ↓
Internal Developer Platforms & Golden Paths
  ↓
Operable Production Systems
```

---

## The Three Converging Tracks

```text
Track A: Production SRE ──────────────┐
Track B: OpenTelemetry & Observability ┼──► Reliable, Observable, Operable Production Systems
Track C: Platform Engineering ────────┘
```

1. **Track A — Production SRE**: Service -> Reliability Requirements -> SLIs -> SLOs -> Error Budgets -> Alerts -> On-Call -> Incident Response -> Capacity -> Failure Engineering -> Production Readiness.
2. **Track B — OpenTelemetry & Observability**: Application Behavior -> Instrumentation -> Logs / Metrics / Traces -> Context Propagation -> OpenTelemetry SDK -> OTLP -> Collector -> Processors -> Exporters -> Observability Backends -> Debugging.
3. **Track C — Platform Engineering**: Repeated Developer Pain -> Standard Capability -> Automation -> Platform API -> Golden Path -> Self-Service -> Guardrails -> Developer Experience -> Platform Product.

---

## Critical Teaching Rule: Never Teach Tools First

* **Bad**: *"Install Prometheus. Install Grafana. Create a dashboard."*
* **Better**: *"Users report checkout is slow. What signal would prove it? Instrument request latency -> collect measurements -> aggregate -> visualize -> define expected reliability -> alert only when action is required."*

* **Bad**: *"Add tracing."*
* **Better**: *"A request crosses 5 services. Latency is 2 seconds. Individual service logs do not explain where time went. Need causal request context -> derive distributed tracing from first principles."*

* **Bad**: *"Build an internal developer platform."*
* **Better**: *"20 teams independently configure service scaffolding, CI, metrics, deployment, secrets, and alerts. Repeated cognitive and operational burden -> derive a reusable, self-service platform capability."*

---

## Repository Structure

```text
production-sre-observability-platform-engineering-from-scratch/
├── README.md                          # Curriculum overview and philosophy
├── ROADMAP.md                         # Complete 22-part, 244-phase roadmap
├── LEARNING.md                        # Pedagogical methodology & empirical loop
├── LESSON_TEMPLATE.md                 # Universal template for all lessons
├── VERSIONS.md                        # Strict version discipline & semantic conventions
├── SAFETY.md                          # Chaos engineering invariants & safety guidelines
├── PRODUCTION_READINESS_TEMPLATE.md   # Production Readiness Review (PRR) checklist
├── SLO_TEMPLATE.md                    # Standard SLO design document
├── INCIDENT_TEMPLATE.md               # Real-time incident command state tracker
├── POSTMORTEM_TEMPLATE.md             # Blameless postmortem document
├── PLATFORM_PRODUCT_TEMPLATE.md       # Platform capability design document
├── CONTRIBUTING.md                    # Contribution guidelines
├── Makefile                           # Lab automation targets
├── docker-compose.yml                 # Complete local tier 1 lab environment
│
├── scripts/                           # Core operational automation
│   ├── check-environment.sh          # Verify host runtimes and dependencies
│   ├── start-lab.sh                  # Bootstrap microservices & observability stack
│   ├── stop-lab.sh                   # Graceful shutdown of lab containers
│   ├── inject-failure.sh             # Controlled chaos injection harness
│   └── reset-lab.sh                  # Restore clean baseline state
│
├── services/                          # Production microservice suite
│   ├── api-gateway/                  # Reverse proxy, rate limiting, correlation IDs
│   ├── checkout-service/             # Core business orchestrator, SLI/SLO emitter
│   ├── inventory-service/            # Relational inventory management with PostgreSQL
│   ├── payment-service/              # Downstream payment engine with circuit breakers
│   ├── notification-worker/          # Asynchronous queue consumer with Redis
│   └── common/                       # Shared telemetry, logging, and W3C context utilities
│
├── instrumentation/                   # Telemetry engines from scratch
│   ├── stdlib_tracing.py             # Distributed tracing from standard library
│   ├── stdlib_metrics.py             # Atomic counters, gauges, histograms
│   ├── structured_logging.py         # JSON logger with correlation & trace context
│   └── otel_sdk_setup.py             # OpenTelemetry SDK initialization (v1.26+ conventions)
│
├── otel/                              # OpenTelemetry Collector pipelines
│   ├── otel-collector-config.yaml    # Receivers, processors (batch, memory, filter), exporters
│   └── pipelines.md                  # Deep pipeline architectural documentation
│
├── dashboards/                        # Declarative Grafana dashboards
│   ├── red-metrics-dashboard.json    # Rate, Errors, Duration for HTTP services
│   ├── use-resources-dashboard.json  # Utilization, Saturation, Errors for hosts
│   ├── four-golden-signals-dashboard.json # Latency, Traffic, Errors, Saturation
│   └── slo-burn-rate-dashboard.json  # Error budget consumption and burn rates
│
├── alerts/                            # Prometheus & Alertmanager configs
│   ├── prometheus-rules.yaml         # Multi-window burn rate & symptom alert rules
│   ├── alertmanager-config.yaml      # Routing trees, grouping policies, inhibition rules
│   └── silences.yaml                 # Safe operational silence templates
│
├── slo-labs/                          # SLO and error budget calculation tools
│   ├── checkout_slo.yaml             # Declarative SLO specification
│   ├── error_budget_calculator.py    # Compliance & budget exhaustion math engine
│   └── burn_rate_simulator.py        # Multi-window burn-rate simulation runner
│
├── incidents/                         # 30+ Interactive incident simulations & playbooks
├── load-tests/                        # Concurrency, skew, burst, and tail-latency generators
├── chaos/                             # Production failure injection scripts (CPU, memory, DB, delay)
├── platform/                          # Complete Mini Developer Platform
│   ├── cli/                          # `platform-cli` (new-service, scorecard, generate)
│   ├── templates/                    # Production microservice scaffolding
│   ├── catalog/                      # Software catalog and dependency mapper
│   └── scorecards/                   # Production readiness automated evaluator
│
├── broken-systems/                    # 40+ Broken production systems & separate solutions
├── projects/                          # 12 Substantial milestone projects
├── capstones/                         # 7 Production capstones + Final Challenge
└── docs/                              # Deep mental models and reference guides
```

---

## Quick Start: Launching the Local Production Lab (Tier 1)

### 1. Verify Your Environment
```bash
./scripts/check-environment.sh
```

### 2. Start the Full Production Lab
```bash
make start-lab
# Or: ./scripts/start-lab.sh
```
This starts:
* `api-gateway` (Port 8000)
* `checkout-service` (Port 8001)
* `inventory-service` (Port 8002)
* `payment-service` (Port 8003)
* `notification-worker` (Port 8004)
* `PostgreSQL 16` (Port 5432)
* `Redis 7` (Port 6379)
* `OpenTelemetry Collector` (gRPC: 4317, HTTP: 4318, Prometheus metrics: 8889)
* `Prometheus` (Port 9090)
* `Alertmanager` (Port 9093)
* `Grafana` (Port 3000 - admin/admin)
* `Grafana Tempo` (Port 3200)

### 3. Generate Baseline Traffic
```bash
python3 load-tests/load_generator.py --rps 25 --duration 60
```

### 4. Inspect Production Telemetry
* **Check RED Metrics**: Visit `http://localhost:9090` (Prometheus) or `http://localhost:3000` (Grafana).
* **Inspect Distributed Trace**: Query `traceparent` across services in Tempo at `http://localhost:3000/explore`.
* **Inspect Structured Logs**: Examine correlated JSON output in container logs or `outputs/`.

### 5. Inject a Controlled Failure
```bash
./scripts/inject-failure.sh --scenario payment-latency --delay-ms 1500
```
Observe:
1. Upstream `checkout-service` latency climbs to p99 > 1500ms.
2. Connection pool saturation metric increases.
3. Multi-window burn rate alert fires in Alertmanager.
4. Circuit breaker trips to protect upstream resources.

### 6. Reset the Lab
```bash
./scripts/reset-lab.sh
```

---

## Ready to Begin?

Start at **[Phase 00: Production Laboratory](phases/part-01-production-foundations/phase-00-production-laboratory/)** or browse the **[Complete Roadmap](ROADMAP.md)**.
