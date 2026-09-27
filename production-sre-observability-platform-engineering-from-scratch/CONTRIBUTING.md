# Contributing to Production SRE & Platform Engineering from Scratch

We welcome contributions from engineers, educators, SREs, and platform practitioners.

---

## 1. Core Teaching Philosophy

Before contributing any lesson, lab, simulation, or platform feature, internalize the **Core Learning Loop**:

```text
MOTTO
 ↓
PROBLEM
 ↓
PREDICT
 ↓
FIRST PRINCIPLES
 ↓
MENTAL MODEL
 ↓
BUILD SIMPLE VERSION
 ↓
USE REAL TOOL
 ↓
OBSERVE
 ↓
MEASURE
 ↓
BREAK
 ↓
DETECT
 ↓
DEBUG
 ↓
RECOVER
 ↓
AUTOMATE
 ↓
EVIDENCE
```

### Critical Rules
1. **Never teach tools first**: Always establish the real production failure or developer friction before introducing a tool or configuration.
2. **First principles before frameworks**: Build or walk through the underlying mechanism in standard code (e.g. Python stdlib sockets, headers, time-series math) before showing the tool abstraction.
3. **Evidence-driven completion**: A lesson is never complete merely because a command succeeded or a dashboard rendered. The learner must collect empirical measurements and explain the failure mechanism.
4. **Strict Semantic Conventions**: Use current, stable OpenTelemetry semantic conventions (v1.26.0+). Never introduce deprecated attributes like `http.method` or `http.status_code`.

---

## 2. Directory Structure Conventions

* `phases/`: 22 Parts containing 244 phases (Phases 00 to 243).
* `services/`: Production microservices (`api-gateway`, `checkout-service`, `inventory-service`, `payment-service`, `notification-worker`).
* `instrumentation/`: Telemetry libraries, manual loggers, metric aggregators, and OTel SDK configurations.
* `otel/`: OpenTelemetry Collector pipelines (receivers, processors, exporters).
* `dashboards/`: Declarative JSON dashboards for Grafana.
* `alerts/`: Prometheus alerting rules and Alertmanager routing/inhibition policies.
* `slo-labs/`: SLI/SLO calculations, error budget tracking, and burn rate simulations.
* `incidents/`: 30+ interactive incident simulations and playbooks.
* `broken-systems/`: 40+ broken production scenarios with setup, symptoms, hints, and separated solutions in `broken-systems/solutions/`.
* `projects/`: 12 comprehensive milestone projects.
* `capstones/`: 7 production capstones culminating in the Final Production Engineering Challenge.
* `docs/`: Reference mental models, guides, and architecture documentation.

---

## 3. Contribution Workflow

1. Fork or branch from `main`.
2. Follow `LESSON_TEMPLATE.md` for new lessons.
3. Ensure all code adheres to Python 3.11+, includes type hints, and passes unit and integration tests.
4. Run tests before submitting:
   ```bash
   make test
   make lint
   ```
5. Ensure failure injection scripts specify a clear blast radius and automated abort condition per `SAFETY.md`.
