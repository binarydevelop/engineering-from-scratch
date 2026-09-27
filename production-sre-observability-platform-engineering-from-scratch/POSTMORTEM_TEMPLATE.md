# Incident Postmortem: [Incident Name]

> **Blameless Culture Note**: Postmortems examine the systemic, environmental, and procedural factors that enabled an incident to occur. Human errors are symptoms of systemic vulnerabilities, never root causes.

---

# Incident
[Brief descriptive title, date, and severity classification, e.g. "SEV-1 Checkout API Degradation Due to Payment Connection Exhaustion - 2026-09-25"]

## Impact
* **Duration**: 21 minutes (14:15Z - 14:36Z)
* **User Impact**: 3,420 checkout attempts failed with HTTP 500 error. Approximately $82,000 in delayed or abandoned shopping cart transactions.
* **SLO Impact**: Consumed 18.2% of the rolling 30-day error budget for `checkout-service`.

## Detection
* **Detection Mechanism**: Prometheus Alertmanager multi-window burn rate alert (`CheckoutSLOHighBurnRate1h`).
* **Time to Detect (TTD)**: 3 minutes from trigger to alert firing.
* **Time to Acknowledge (TTA)**: 3 minutes from page to responder presence in war room.

## Timeline
| Time (UTC) | Event Description / Operational Action |
|:---|:---|
| 14:10 | Automated CI/CD pipeline deployed `payment-service:v1.4.2` to production. |
| 14:15 | Automated health checks passed (readiness probe only checked `/healthz`), but real traffic hit unindexed database lock. |
| 14:18 | Multi-window burn rate alert paged on-call engineer. |
| 14:22 | Responders inspected Grafana RED dashboard; identified 35% error rate on `/checkout`. |
| 14:25 | Responders opened Tempo trace waterfall; isolated 30s latency in child span `payment.verify_token`. |
| 14:30 | Incident Commander verified change correlation: `payment-service` deployed at 14:10. |
| 14:32 | Incident Commander executed rollback command: `make rollback SERVICE=payment-service VERSION=v1.4.1`. |
| 14:36 | Rollback completed across all replicas. Error rate dropped below 0.05%. |
| 14:45 | Incident declared mitigated; monitoring active for 30 minutes. |

## Trigger
A routine deployment of `payment-service:v1.4.2` containing an updated database connection pooling parameter.

## Technical Causes
The default connection pool size in `payment-service` was decreased from 50 to 5 in `config.py` during refactoring. Under concurrent load (120 RPS), worker threads exhausted all 5 database connections within 45 seconds, blocking subsequent requests until the HTTP client read timeout of 30 seconds was reached.

## Contributing Factors
1. **Inadequate Staging Load**: The change was tested in staging under single-user synthetic tests where 5 connections were sufficient.
2. **Shallow Readiness Probe**: The `/ready` probe returned HTTP 200 without validating database pool acquisition latency.
3. **Missing Circuit Breaker**: The upstream `checkout-service` waited the full 30 seconds for `payment-service` instead of tripping a fast-failing circuit breaker after 5 consecutive failures.

## Why Impact Was Possible
The platform lacked an automated canary analysis step in the deployment pipeline that compares error rates between new and old versions prior to 100% traffic shifting.

## Mitigation
Immediate manual rollback to previous immutable container image `payment-service:v1.4.1`.

## Recovery
System returned to normal latency and error baseline immediately upon container replacement. Stale connection slots in PostgreSQL closed automatically upon TCP teardown.

## What Went Well
* Multi-window burn rate alert fired reliably within 3 minutes of customer degradation.
* Distributed traces immediately pointed to the exact downstream service and span causing the bottleneck.
* Rollback was fast and cleanly automated via the platform deployment script.

## What Went Poorly
* Responders initially scaled out `checkout-service` pods, which increased pressure on downstream dependencies without relieving the bottleneck.
* Staging environment testing did not mimic realistic concurrency.

## Corrective Actions
| Action Item | Type (Prevent / Mitigate / Detect) | Priority | Owner | Due Date |
|:---|:---|:---|:---|:---|
| Add connection pool saturation metric and alert to `payment-service` | Detect | P1 | @infra-telemetry | 2026-10-02 |
| Implement client-side circuit breaker in `checkout-service` for payment calls | Mitigate | P1 | @checkout-team | 2026-10-05 |
| Integrate automated canary progressive delivery into platform CLI | Prevent | P2 | @platform-team | 2026-10-15 |
| Deepen readiness probes to verify connection pool health | Prevent | P2 | @payment-team | 2026-10-08 |

## Owners
* Primary Author: 
* SRE Reviewer: 
* Service Team Lead: 

## Follow-Up Date
Review scheduled for Sprint Planning on [Date].

## Lessons
Reliability cannot be verified with zero-traffic health checks. Concurrency-dependent configurations (thread pools, connection pools, queue depths) must be guarded with automated canary analysis and client-side isolation patterns like bulkheads and circuit breakers.
