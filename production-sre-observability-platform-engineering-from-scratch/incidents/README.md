# Production Incident Response Simulations Suite (30+ Scenarios)

> **Motto**: When production is burning, follow the diagnostic evidence tree, not your ungrounded intuition. Mitigate first; satisfy intellectual curiosity later.

---

## 1. How Incident Simulations Work

Each incident simulation immerses you in a realistic on-call scenario:
1. An automated failure or traffic surge is triggered.
2. A Prometheus multi-window burn rate or symptom alert pages the incident channel.
3. You receive incomplete, ambiguous evidence across metrics, logs, and traces.
4. You must declare incident severity, assume the Incident Commander role, triage, execute a safe mitigation, restore service health, and author a blameless postmortem.

```text
Alert Fires (PagerDuty / Alertmanager)
   │
   ▼
Triage (User Impact? Since When? What Changed?)
   │
   ▼
Mitigate (Rollback / Circuit Breaker / Load Shedding)
   │
   ▼
Verify Recovery (SLO compliance & Error Rate < 0.05%)
   │
   ▼
Blameless Postmortem (swiss cheese causal model)
```

---

## 2. Directory of Incident Simulations

| Sim ID | Incident Scenario | Primary Symptom | Mitigation Action |
|:---|:---|:---|:---|
| **01** | `simulation-01-deployment-error-spike` | 35% error rate immediately after deployment | Image rollback to previous version |
| **02** | `simulation-02-db-lock-contention` | p99 latency climbs to 4,500ms on checkout | Terminate blocking idle transaction |
| **03** | `simulation-03-dependency-dns-failure` | 504 Gateway Timeouts across payment calls | Switch to static IP / backup DNS resolver |
| **04** | `simulation-04-cache-stampede-overload` | Cache flush causes 100% DB CPU saturation | Enable mutex lock / warm cache |
| **05** | `simulation-05-silent-queue-backlog` | Notifications delayed 45 minutes; 0 errors | Restart stalled consumer thread |
| **06** | `simulation-06-cascading-retry-storm` | Traffic doubles; dependency in crash loop | Enable exponential backoff & jitter |
| **07** | `simulation-07-memory-leak-slow-burn` | OOMKilled every 4 hours across API pods | Restart pods & patch cache key TTL |
| **08** | `simulation-08-cpu-quota-throttling` | 800ms latency spikes with 25% CPU usage | Relax CFS quota or increase CPU limits |
| **09** | `simulation-09-connection-pool-exhaustion`| In-flight requests queue up; timeouts | Tune pool size & close idle connections |
| **10** | `simulation-10-third-party-payment-timeout`| Stripe API hangs for 30s | Trip client circuit breaker |
| **11 – 30**| Comprehensive Scenarios Suite | Varied distributed failures | See `simulation-11-to-30-catalog.md` |
