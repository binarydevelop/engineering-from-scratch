# Project 04: SaaS Multi-Tenant Metrics Engine

> **Repository Motto:** Understand it. Model it. Query it. Inspect it. Measure it. Break it. Fix it. Optimize it. Ship it.

---

## 1. Project Overview

This project models B2B multi-tenant SaaS application mechanics, tracking enterprise organizations, role-based memberships, seat subscriptions, JSONB telemetry events, and financial KPIs.

---

## 2. Key Queries Implemented

- Monthly Recurring Revenue (MRR) by plan tier (`starter`, `pro`, `enterprise`)
- Seat utilization rates: comparing used seats to purchased subscription seats
- Organization feature adoption through JSONB payload analysis
- Churn candidate identification (active subscriptions with zero recent activity)
- Telemetry event velocity per tenant

---

## 3. Running the SaaS Lab

```bash
make seed-saas
docker exec -i database-sql-scratch-db psql -U postgres -d sqllab < projects/04-saas-metrics-engine/saas_queries.sql
```
