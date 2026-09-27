# Phase 243: The Staff Production Engineering Challenge

> **Motto**: Understand it. Instrument it. Measure it. Break it. Detect it. Debug it. Recover it. Automate it. Improve it. Operate it.

---

## 1. The Real-World Production Problem

You have just joined *HyperScale Cloud Solutions* as Staff Production / Platform Engineer.

The company operates a fast-growing B2B SaaS platform that processed $450M in transactions last year.
The engineering organization consists of 140 software engineers spread across 18 product squads managing **80 microservices** running on Kubernetes.

### The Current Reality
* **Paging Nightmare**: Responders receive an average of **340 on-call pages per week**. Over 80% are acknowledged and immediately closed with no action taken (alert fatigue).
* **Telemetry Chaos**: 5 different logging formats exist. Some services use OpenTracing, some use vendor proprietary agents, and others use raw `print()` statements. Trace context breaks across 60% of service hops.
* **Incidents & MTTR**: Mean Time to Resolve (MTTR) for SEV-1 customer outages is **84 minutes**. Postmortems repeatedly state: *"Could not locate the slow database query because logs were missing and traces didn't correlate."*
* **Platform Bottleneck**: Product squads wait an average of **9 business days** for the central infrastructure team to fulfill Jira tickets to provision a new service, database, or Kafka topic.
* **Infrastructure Cost**: Cloud spending increased 180% year-over-year. Clusters run at an average of **11% CPU utilization** because developers assign massive arbitrary resource requests out of fear.
* **Deployment Fear**: Engineering leadership has instituted "Deployment Freeze Thursdays and Fridays" because Thursday deploys routinely cause weekend outages.

---

## 2. The Staff Engineer Mandate

You are not permitted to solve this by saying: *"Let's install an expensive vendor observability platform and rewrite everything."*

You must independently work through the **14-Step Systematic Production Engineering Transformation**:

```text
       1. User & Business Impact Analysis
                      ↓
       2. Comprehensive Service & Dependency Inventory
                      ↓
       3. Standardized Telemetry Baseline (OpenTelemetry)
                      ↓
       4. Critical User Journeys & SLI/SLO Hierarchy
                      ↓
       5. Alerting Overhaul & Fatigue Elimination
                      ↓
       6. Incident Command Lifecycle & Playbook Overhaul
                      ↓
       7. Capacity Modeling, Headroom & Sizing Optimization
                      ↓
       8. Progressive Delivery & Deployment Safety Guardrails
                      ↓
       9. Operational Toil Identification & Automation
                      ↓
       10. Internal Developer User Research & Pain Mapping
                      ↓
       11. The Golden Path Platform Capability Architecture
                      ↓
       12. True Self-Service API Contracts & Guardrails
                      ↓
       13. Six-Month Reliability & Velocity Roadmap
                      ↓
       14. Executive Metrics & Quantified Engineering ROI
```

---

## 3. Required Deliverables

To complete the Staff Production Engineering Challenge, submit the following engineering artifacts:

1. **Service Inventory & Tiering Matrix (`inventory_tiering.md`)**: Classify all 80 services into Tier 1, Tier 2, and Tier 3 with explicit SLO obligations.
2. **OpenTelemetry Telemetry Pipeline Blueprint (`telemetry_architecture.md`)**: Architecture of Agent vs Gateway Collector topologies, memory limiters, tail sampling rules, and stable v1.26+ semantic conventions.
3. **Core Journey SLO Documents (`checkout_slo_spec.yaml`)**: Complete SLO specification with good/total event PromQL queries, rolling 30-day windows, and multi-window burn rate alert rules.
4. **Alert Rationalization Audit (`alert_rationalization.md`)**: Plan to reduce 340 weekly pages to fewer than 15 actionable pages.
5. **Platform Capability Design (`platform_service_contract.yaml`)**: Declarative developer contract replacing the 9-day Jira ticket process with a 3-minute self-service CLI command (`platform new-service`).
6. **Executive ROI Summary (`executive_business_case.md`)**: Sizing calculation showing how right-sizing containers and eliminating idle headroom will save $1.2M in annual cloud spend while improving availability from 99.1% to 99.95%.

---

## 4. Evaluation Rubric

| Dimension | Unsatisfactory | Proficient (Senior SRE) | Exemplary (Staff Production Engineer) |
|:---|:---|:---|:---|
| **Problem Formulation** | Blames developers or tools. | Identifies technical symptoms. | Uncovers systemic incentives, missing guardrails, and business risk. |
| **Telemetry Design** | Emits high-cardinality metrics. | Configures standard OTel agents. | Designs governed telemetry pipeline with memory protection and tail-sampling. |
| **Alerting Quality** | Retains cause-based CPU alerts. | Shifts to basic error alerts. | Multi-window burn-rate alerts with automated runbooks and inhibition trees. |
| **Platform Strategy** | Builds a central approval gate. | Creates basic Helm charts. | Builds self-service Golden Paths with guardrails, scorecards, and escape hatches. |
