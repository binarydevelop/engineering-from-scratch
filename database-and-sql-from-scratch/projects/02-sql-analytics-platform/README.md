# Project 02: SQL Analytics & Business Intelligence Engine

> **Repository Motto:** Understand it. Model it. Query it. Inspect it. Measure it. Break it. Fix it. Optimize it. Ship it.

---

## 1. Project Overview

This project compiles a complete suite of executive business intelligence queries against our relational dataset. You will construct:
- Daily and monthly revenue runs
- Average Order Value (AOV) dynamics
- Top products and categories by margin and volume
- Repeat customer behavior
- Customer Lifetime Revenue (LTV) distributions
- Full 5-stage conversion funnels
- Monthly cohort retention matrices
- Rolling 7-day smoothed revenue windows
- Month-over-Month (MoM) growth calculations

---

## 2. Running the Analytics Suite

```bash
docker exec -i database-sql-scratch-db psql -U postgres -d sqllab < projects/02-sql-analytics-platform/analytics_suite.sql
```
