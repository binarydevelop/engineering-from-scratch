# Service Level Objectives (SLOs) & Error Budget Engineering

> **Motto**: 100% reliability is the wrong target for virtually every system. The error budget is not a permission to be sloppy; it is the currency of engineering velocity.

---

## 1. The Anatomy of an SLO

An SLO is a product and engineering agreement defining expected reliability over time:

```text
Critical User Journey (CUJ)
       │
       ▼
Service Level Indicator (SLI)
   SLI = Good Events / Total Events
       │
       ▼
Service Level Objective (SLO)
   SLO = Target % over Rolling Window (e.g. 99.9% over 30 days)
       │
       ▼
Error Budget
   Error Budget = 100% - SLO Target (e.g. 0.1% allowable failures)
```

---

## 2. Multi-Window Multi-Burn-Rate Alerting

Traditional alerts on simple error rates create false positives (a 30-second error burst triggers a wake-up page) or detect catastrophic outages too late (a 2% error rate takes 24 hours to page).

Google SRE pioneered **Multi-Window Multi-Burn-Rate Alerting**, which measures both a short window (to confirm the condition is still active) and a long window (to ensure significant error budget is consumed):

```text
┌──────────────┬─────────────┬────────────┬────────────────────────┬──────────────────────┐
│ Alert Tier   │ Burn Rate   │ Budget %   │ Short Window           │ Long Window          │
├──────────────┼─────────────┼────────────┼────────────────────────┼──────────────────────┤
│ Page (Urgent)│ 14.4x       │ 2% budget  │ 5 minutes              │ 1 hour               │
│ Page (Medium)│ 6x          │ 5% budget  │ 30 minutes             │ 6 hours              │
│ Ticket (Low) │ 1x          │ 10% budget │ 2 hours                │ 3 days               │
└──────────────┴─────────────┴────────────┴────────────────────────┴──────────────────────┘
```

### The PromQL Implementation:
```promql
# 1-Hour Burn Rate Alert (14.4x burn rate on 99.9% SLO)
(
  sum(rate(http_requests_total{job="checkout-service", status=~"5.."}[1h]))
  /
  sum(rate(http_requests_total{job="checkout-service"}[1h]))
) > (14.4 * (1 - 0.999))
and
(
  sum(rate(http_requests_total{job="checkout-service", status=~"5.."}[5m]))
  /
  sum(rate(http_requests_total{job="checkout-service"}[5m]))
) > (14.4 * (1 - 0.999))
```

---

## 3. The Error Budget Policy

What happens when an error budget is exhausted?
1. **Development Freeze on Risky Features**: New feature releases with non-zero risk are paused.
2. **Shift to Reliability**: Sprints are dedicated to addressing postmortem action items, resilience patterns, and architectural fixes.
3. **Restoration**: Once the 30-day rolling compliance window recovers above the SLO target, standard deployment cadence resumes.
