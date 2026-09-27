# Part 18: Delivery & Change Safety (Phases 195 – 200)

> **Motto**: Understand it. Instrument it. Measure it. Break it. Detect it. Debug it. Recover it. Automate it. Improve it. Operate it.

---

## Overview

Part 18 examines CI/CD pipelines as critical production infrastructure. We track the 4 DORA metrics, measure Change Failure Rate (CFR), optimize Mean Time to Rollback (MTTR), and build automated rollback controllers.

---

## Key Topics & Invariants

### 1. The CI/CD Pipeline is Production Infrastructure (Phase 195)
If your deployment pipeline fails, you cannot deploy emergency security patches or mitigate active production incidents. CI/CD runners must have their own SLOs, alerts, and capacity monitoring.

### 2. DORA Metrics (Phase 196)
1. **Deployment Frequency**: How often code is deployed to production.
2. **Lead Time for Changes**: Time from commit to running in production.
3. **Change Failure Rate**: Percentage of deployments requiring immediate hotfix or rollback.
4. **Time to Restore Service**: Time required to recover from an outage.

### 3. Automated Rollback Controllers (Phase 200)
Eliminating human reaction latency during bad releases:
* CI/CD triggers canary release (5% traffic).
* Automated metric analyzer queries Prometheus: `Canary 5xx rate > 0.5% for 60s`.
* If breached, controller automatically rolls back image tag to previous stable version without waiting for human intervention.
