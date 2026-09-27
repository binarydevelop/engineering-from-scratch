# Deployment Specification: [Deployment Name / ID]

> "Deployment is the operational act of installing a verified artifact into a target environment and exposing it to live network traffic under strict health observation."

---

## Environment
- **Target Name**: `staging` | `production-us-east` | `production-eu-west`
- **Environment Tier**: Tier-1 Production / Non-Production
- **Protection Rules**: Manual approval by on-call lead required; deployment window Tuesday-Thursday 10:00-14:00 UTC

---

## Artifact
- **Image / Bundle Digest**: `sha256:7f9b8c31e428a1...`
- **Source Git Commit**: `e4b3c2a19876543210fedcba0123456789abcdef`
- **Release Version**: `v2.4.1`
- **Provenance Verified**: Yes (Cosign signature validated against GitHub Actions OIDC identity)

---

## Previous Version
- **Running Image Digest**: `sha256:1a2b3c4d5e6f7a...`
- **Running Release Version**: `v2.4.0`
- **State of Prior Replicas**: 10 pods healthy, 0 restarts in prior 24 hours

---

## Deployment Strategy
- **Type**: `Canary` (Progressive Rollout) | `Blue/Green` | `Rolling Update` | `Recreate`
- **Traffic Stepping**:
  - Step 1: 1% traffic for 5 minutes
  - Step 2: 10% traffic for 10 minutes
  - Step 3: 50% traffic for 15 minutes
  - Step 4: 100% traffic promotion
- **Max Unavailable / Max Surge**: `maxUnavailable: 0`, `maxSurge: 25%`

---

## Preconditions
- [ ] Database migration pre-flight completed successfully
- [ ] Upstream API dependencies healthy and responsive
- [ ] Cloud infrastructure capacity confirmed (CPU/Memory headroom > 30%)
- [ ] On-call engineer active in incident war room

---

## Database Compatibility
- **Migration Required**: Yes (`db/migrations/003_add_order_status.sql`)
- **Compatibility Proof**: Both v2.4.0 and v2.4.1 can simultaneously read and write to the database during the 30-minute transition window without SQL exceptions.
- **Rollback Safety**: Tested in staging; reverting application to v2.4.0 does not break on modified schema.

---

## Capacity Requirement
- **Baseline Replicas**: 10
- **Surge Replicas**: +3 during rolling update
- **CPU / Memory Allocation**: 500m CPU, 512Mi RAM per replica

---

## Health Signals
- **Liveness Probe**: `GET /health/liveness` (HTTP 200 within 2s)
- **Readiness Probe**: `GET /health/readiness` (HTTP 200 within 1s, checks DB connectivity)
- **Key Performance Indicators (KPIs)**:
  - HTTP 5xx error rate < 0.05%
  - p99 request latency < 120ms
  - Process restart count = 0

---

## Verification
- **Automated Smoke Tests**: Execute `scripts/test-smoke.sh --target https://production.internal`
- **Synthetic Synthetic Transaction**: Test order placed and validated through Kafka consumer
- **Log Scrape Check**: No unhandled exception stack traces in stdout/stderr log stream

---

## Abort Condition
Immediate automated rollback triggered if any of the following occur during the canary phase:
1. HTTP 5xx error rate exceeds 0.2% over a 60-second sliding window
2. p99 latency exceeds 250ms for more than 2 consecutive minutes
3. Readiness probe fails on more than 2 canary replicas simultaneously
4. Critical business invariant violated (e.g., checkout payment drop > 5%)

---

## Rollback / Roll-Forward Plan
- **Primary Action (Rollback)**: Re-point traffic routing service to previous stable digest `sha256:1a2b3c4d5e6f7a...` within 30 seconds.
- **Secondary Action (Roll-Forward)**: If rollback is precluded by a subsequent data mutation, deploy pre-tested hotfix branch `hotfix/v2.4.2` following express validation pipeline.
- **Rollback Execution Command**:
  ```bash
  ./scripts/rollback.sh --target production --to-digest sha256:1a2b3c4d...
  ```

---

## Result
- **Deployment Status**: Succeeded | Rolled Back | Aborted
- **Total Rollout Duration**: 34 minutes
- **Final Deployed Digest**: `sha256:7f9b8c31e428a1...`
- **Incidents Triggered**: 0

---

## Post-Deployment Evidence
- **Metrics Dashboard Snapshot**: Link to Grafana / Datadog deployment dashboard
- **Canary Analysis Log**: Summary of metrics collected at 1%, 10%, 50%, and 100% traffic steps
- **Deployment Audit Record**: Log entry inserted into deployment audit ledger
