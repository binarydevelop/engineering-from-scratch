# Exercise Q155: Q155 Saas Activity Burn Rate

**Tier:** Challenge  
**Target Schema:** `saas`  
**Concept Tags:** `SaaS`, `Telemetry Velocity`  

---

## 1. Business Requirement

> Calculate daily telemetry event velocity (events per day) per organization. Project organization_id, avg_daily_events. Order by avg_daily_events DESC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: organization_id, avg_daily_events

---

## 3. Query Thinking Framework Checklist

Before writing SQL, answer these questions:
1. What should one row represent in your output?
2. Which tables hold the primary facts and attributes?
3. What is the join cardinality? (1:1, 1:N, N:M)
4. Are any rows eliminated by NULL handling or outer joins?
5. Is an explicit `ORDER BY` necessary for deterministic result verification?

---

## 4. Verification

Execute your query and grade it against the reference solution:

```bash
python3 scripts/grade-query.py exercises/challenge/q155-saas-activity-burn-rate.md
```
