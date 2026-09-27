# Exercise Q55: Q55 Saas Mrr By Tier

**Tier:** Intermediate  
**Target Schema:** `saas`  
**Concept Tags:** `SaaS`, `Financial Modeling`  

---

## 1. Business Requirement

> Calculate Monthly Recurring Revenue (MRR) and active organization count grouped by plan_tier for active subscriptions. Order by total_mrr DESC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: plan_tier, total_mrr, active_orgs

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
python3 scripts/grade-query.py exercises/intermediate/q55-saas-mrr-by-tier.md
```
