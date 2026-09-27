# Production Deployment Strategies: Comparative Architecture & Trade-Offs

> "There is no single 'best' deployment strategy. Every strategy is an explicit engineering trade-off between infrastructure cost, rollback speed, state compatibility, traffic granularity, and blast radius."

---

## 1. Deep Dive into the Four Core Strategies

### Strategy 1: Recreate Deployment
- **Mechanism**: All existing version 1 (v1) instances are terminated simultaneously. Once v1 is completely shut down, version 2 (v2) instances are started.
- **Downtime Window**: **Guaranteed Downtime**. During the transition interval (between v1 termination and v2 readiness), zero instances exist to handle traffic.
- **State Compatibility**: Excellent. Because v1 and v2 never execute concurrently, you will never have two versions reading and writing to the database at the same instant.
- **When to Use**: Internal batch workers, development environments, or applications with non-backward-compatible breaking data transformations where downtime is contractually accepted.

### Strategy 2: Rolling Update
- **Mechanism**: Instances are incrementally replaced in batches. For example, in a 10-replica cluster with `maxSurge: 2` and `maxUnavailable: 0`, 2 new v2 pods are launched. Once they pass readiness checks, 2 old v1 pods are terminated. This repeats until all replicas run v2.
- **Downtime Window**: **Zero Downtime** (if readiness probes are properly calibrated).
- **State Compatibility Challenge**: **Dual-Version Coexistence**. During the rollout window (which can last 5 to 30 minutes), v1 and v2 pods are both handling live customer traffic and reading/writing to the same database simultaneously.
- **When to Use**: The standard default for microservices running in Kubernetes that have backward-compatible schemas.

### Strategy 3: Blue / Green Deployment
- **Mechanism**: Two complete, identical production environments exist. Blue is currently live (100% traffic). Green is completely idle. The new v2 release is deployed to Green. Staging smoke tests, security scans, and database pre-flights execute against Green without user disruption. Once verified, the load balancer router shifts 100% of live traffic from Blue to Green.
- **Downtime Window**: **Zero Downtime**. The cutover occurs at the load balancer / ingress router level.
- **Rollback Speed**: **Instantaneous (< 1 second)**. If a critical bug is discovered, the router simply swings traffic back to Blue.
- **Capacity Cost**: **High (+100% Infrastructure Cost)**. Requires running double the infrastructure capacity during releases.
- **When to Use**: Mission-critical banking, payment, or telecom systems where rollback must be instantaneous and capacity cost is secondary.

### Strategy 4: Progressive Canary Deployment
- **Mechanism**: A tiny subset of instances (or a weighted router rule) receives a fraction of real user traffic (e.g. 1%). Automated health analysis monitors telemetry (error rate, p95 latency, crash rate). If metrics remain healthy, traffic progresses: 1% -> 10% -> 50% -> 100%. If metrics regress, traffic is cut immediately to 0%.
- **Blast Radius**: **Minimal**. A defect affects only the 1% of users who hit the canary during the test window.
- **Observability Prerequisite**: Requires high-volume, reliable metrics (Prometheus, Datadog) to establish statistical confidence before promoting.
- **When to Use**: High-traffic customer-facing web services, e-commerce, and mobile backend APIs.

---

## 2. Strategy Comparison Matrix

| Evaluation Criteria | Recreate | Rolling Update | Blue / Green | Progressive Canary |
|:---|:---|:---|:---|:---|
| **Downtime** | Guaranteed Downtime | Zero Downtime | Zero Downtime | Zero Downtime |
| **Additional Infrastructure Cost** | 0% (Minimal) | Low (Surge: +10-25%) | Very High (+100%) | Moderate (+10-20%) |
| **Rollback Speed** | Slow (Must Re-deploy) | Moderate (Reverse Rolling) | Instant (< 1s switch) | Fast (Route cut: < 5s) |
| **Simultaneous Version Coexistence**| None (v1 then v2) | Yes (v1 + v2 concurrent)| Minimal (Post-cutover) | Yes (v1 + v2 concurrent)|
| **Traffic Control Granularity** | All or Nothing | Replica-ratio bound | All or Nothing | Arbitrary % (1%, 5%, 50%)|
| **Observability Sophistication** | Basic process check | Readiness probes | Smoke test suite | Automated SLO analysis |
| **Blast Radius on Fatal Bug** | 100% of users affected| Gradual user impact | 100% until reverted | Confined to canary % |

---

## 3. Canary Automated Abort Logic

In progressive delivery, humans should not be staring at dashboards to decide whether to abort a deployment. The deployment controller must enforce hard abort thresholds:

```python
def evaluate_canary_health(canary_metrics, baseline_metrics):
    # Rule 1: HTTP 5xx Error Rate Guardrail
    if canary_metrics.error_rate > 0.005:  # > 0.5% errors
        return ABORT_DEPLOYMENT("5xx error rate exceeded threshold")

    # Rule 2: Latency Degradation Guardrail
    if canary_metrics.p99_latency_ms > (baseline_metrics.p99_latency_ms * 1.5):
        return ABORT_DEPLOYMENT("p99 latency degraded by > 50%")

    # Rule 3: Pod Restart Guardrail
    if canary_metrics.restart_count > 0:
        return ABORT_DEPLOYMENT("Canary process crashed unexpectedly")

    return PROMOTE_TO_NEXT_STEP()
```
