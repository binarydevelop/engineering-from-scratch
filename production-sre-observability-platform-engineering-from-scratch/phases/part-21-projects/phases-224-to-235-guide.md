# Phases 224 – 235: Engineering Projects Implementation Guide

> **Motto**: Understand it. Instrument it. Measure it. Break it. Detect it. Debug it. Recover it. Automate it. Improve it. Operate it.

---

## Overview

Phases 224 through 235 guide the implementation of the 12 substantial engineering projects in `projects/`. Each project builds a reusable production-grade tool, pipeline, platform capability, or framework.

---

## Projects Detailed Roadmap

### Phase 224 (Project 01): Instrument a Backend Service from Scratch
* **Objective**: Start with an un-instrumented HTTP service; add structured JSON logging with correlation IDs, atomic Prometheus counters and histograms, and OpenTelemetry spans using stable v1.26+ conventions.
* **Key Artifact**: `services/checkout-service/main.py`.

### Phase 225 (Project 02): Production OTel Collector Pipeline
* **Objective**: Build an out-of-process telemetry pipeline with OTLP receivers, `memory_limiter`, regex PII redaction, batching, and multi-backend export to Prometheus and Tempo.
* **Key Artifact**: `otel/otel-collector-config.yaml`.

### Phase 226 (Project 03): Production Observability Dashboard Suite
* **Objective**: Design declarative Grafana dashboards for RED metrics, USE resources, and Four Golden Signals with strict top-down diagnostic hierarchy.
* **Key Artifact**: `dashboards/red-metrics-dashboard.json`.

### Phase 227 (Project 04): SLO Platform Lite
* **Objective**: Implement an error budget calculation engine that parses declarative SLO manifests, computes 30-day compliance, calculates burn rates, and forecasts time to budget exhaustion.
* **Key Artifact**: `slo-labs/error_budget_calculator.py`.

### Phase 228 (Project 05): Production Alerting Engine
* **Objective**: Configure multi-window multi-burn-rate alerting rules in Prometheus and Alertmanager routing trees with grouping, inhibition, and runbooks.
* **Key Artifact**: `alerts/prometheus-rules.yaml` & `alerts/alertmanager-config.yaml`.

### Phase 229 (Project 06): Interactive Incident Simulator
* **Objective**: Build an automated failure injection harness that triggers controlled anomalies, measures telemetry impact, and records real-time incident timelines.
* **Key Artifact**: `scripts/inject-failure.sh`.

### Phase 230 (Project 07): Production Capacity Planner
* **Objective**: Build a Little's Law capacity planning tool that models peak RPS, latency distributions, CPU core demand with headroom, and database connection pool requirements.
* **Key Artifact**: `projects/project-07-capacity-planner/planner.py`.

### Phase 231 (Project 08): Production Readiness Review CLI
* **Objective**: Author an automated PRR linter evaluating service directories for health probes, resource limits, telemetry, and ownership compliance.
* **Key Artifact**: `platform/scorecards/evaluator.py`.

### Phase 232 (Project 09): Service Bootstrap Platform
* **Objective**: Build the Golden Path scaffolding CLI that generates production-ready microservices with Dockerfile, health probes, and OTel in under 3 seconds.
* **Key Artifact**: `platform/cli/main.py new-service`.

### Phase 233 (Project 10): Internal Developer Platform Lite
* **Objective**: Create a declarative developer contract (`service.yaml`) that translates high-level developer intent into hardened Kubernetes Deployments and Services.
* **Key Artifact**: `platform/cli/main.py generate-manifests`.

### Phase 234 (Project 11): Microservice Software Catalog
* **Objective**: Implement a software catalog parser tracking service metadata, owning teams, criticality tiers, and dependency topologies.
* **Key Artifact**: `platform/catalog/services.yaml`.

### Phase 235 (Project 12): End-to-End Golden Path
* **Objective**: Walk through the complete developer journey: from running `platform new-service` to local deployment, traffic generation, and verified Grafana telemetry.
