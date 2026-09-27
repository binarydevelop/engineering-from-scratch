# Part 05: Alerting & On-Call Engineering (Phases 64 – 72)

> **Motto**: Understand it. Instrument it. Measure it. Break it. Detect it. Debug it. Recover it. Automate it. Improve it. Operate it.

---

## Overview

Part 05 treats alerting as a critical human-system interface. Every paging alert is an interruption of an engineer's life; if an alert is not actionable, it is operational debt.

---

## Core Principles in Part 05

### 1. The Alert Actionability Invariant (Phase 66)
Every paging alert must answer:
1. What is broken from the customer's perspective?
2. What is the business impact?
3. What is the immediate first action the on-call engineer should take?
4. What is the direct link to the operational runbook?

If the answer to question 3 is "nothing, it will resolve itself", **IT MUST NEVER PAGE**.

### 2. Alertmanager Routing Trees (Phase 67)
Routing alerts by `severity` and `tier`:
* Critical paging alerts -> PagerDuty / OpsGenie.
* Warnings -> Team Slack channel.
* Informational -> Ticket backlog.

### 3. Alert Grouping & Inhibition (Phases 68 & 69)
* **Grouping**: When 100 API instances fail due to a database restart, Alertmanager collapses all 100 alerts into a single consolidated notification.
* **Inhibition**: If `DatabaseDown` is already firing, Alertmanager automatically inhibits all downstream `ServiceHighErrorRate` alerts, preventing notification storms.

### 4. Runbooks as Code (Phase 72)
Every alert rule in `alerts/prometheus-rules.yaml` contains an immutable `runbook_url`. Runbooks document triage steps, diagnostic commands, and safe rollback procedures.
