# Part 14: Production Readiness & Toil Elimination (Phases 158 – 165)

> **Motto**: Understand it. Instrument it. Measure it. Break it. Detect it. Debug it. Recover it. Automate it. Improve it. Operate it.

---

## Overview

Part 14 covers Production Readiness Reviews (PRRs) and operational toil elimination. Before a service receives production traffic, its failure modes, runbooks, SLOs, and resource limits must be verified.

---

## Key Topics & Invariants

### 1. The Production Readiness Review (Phase 158)
Evaluating services using `PRODUCTION_READINESS_TEMPLATE.md`:
* Ownership documented.
* Health endpoints (`/healthz`, `/ready`) tested.
* Resource requests and limits configured.
* Standard telemetry (RED metrics, structured logs, W3C trace context) verified.
* Paging alerts linked to actionable runbooks.
* Rollback procedures tested.

### 2. Operational Toil Discipline (Phases 163 – 165)
Google SRE defines **Toil** as work that is:
1. Manual
2. Repetitive
3. Automatable
4. Tactical / reactive
5. Devoid of enduring engineering value
6. Scales linearly as the service grows

### Toil Automation ROI
$$\text{ROI} = \frac{\text{Time Saved over 1 Year}}{\text{Engineering Time to Automate}}$$
Prioritize automating high-frequency, low-cognitive tasks (e.g. database schema migrations, secret rotation, service scaffolding).
