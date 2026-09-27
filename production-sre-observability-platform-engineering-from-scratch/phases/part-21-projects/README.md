# Part 21: Substantial Engineering Projects (Phases 224 – 235)

> **Motto**: Understand it. Instrument it. Measure it. Break it. Detect it. Debug it. Recover it. Automate it. Improve it. Operate it.

---

## Overview

Part 21 contains 12 substantial milestone engineering projects spanning OpenTelemetry, Prometheus, SRE platforms, chaos simulators, and internal developer platforms.

See the complete project code and specifications in **[`projects/`](../../projects/)**.

---

## Projects Directory

* **Phase 224 (Project 01)**: **Instrument a Backend Service from Scratch** (OTel SDK, structured logging, RED metrics, traceparent propagation).
* **Phase 225 (Project 02)**: **Production OTel Collector Pipeline** (Receivers, memory limiter, batch processor, multi-backend exporters).
* **Phase 226 (Project 03)**: **Production Observability Dashboard Suite** (RED, USE, and Four Golden Signals in Grafana).
* **Phase 227 (Project 04)**: **SLO Platform Lite** (Error budget calculator, compliance evaluator, and burn rate alert generator).
* **Phase 228 (Project 05)**: **Production Alerting System** (Prometheus rules, Alertmanager grouping, and inhibition trees).
* **Phase 229 (Project 06)**: **Interactive Incident Simulator** (Automated failure injector, timeline generator, and postmortem validator).
* **Phase 230 (Project 07)**: **Production Capacity Planner** (`planner.py`: modeling peak traffic, Little's Law concurrency, and headroom).
* **Phase 231 (Project 08)**: **Production Readiness CLI** (Automated PRR linter auditing services for health probes, limits, and telemetry).
* **Phase 232 (Project 09)**: **Service Bootstrap Platform** (`platform new-service`: scaffolding observable microservices).
* **Phase 233 (Project 10)**: **Internal Developer Platform Lite** (Declarative `service.yaml` generating container infrastructure).
* **Phase 234 (Project 11)**: **Microservice Software Catalog** (Metadata parser, ownership directory, and dependency mapper).
* **Phase 235 (Project 12)**: **End-to-End Golden Path** (Zero to deployed, observable, compliant production service).
