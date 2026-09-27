# Exercise Q139: Q139 Saas Mrr Cohort Waterfall

**Tier:** Challenge  
**Target Schema:** `saas`  
**Concept Tags:** `SaaS`, `Financial Modeling`  

---

## 1. Business Requirement

> Construct an MRR report showing total active subscriptions, total MRR, average revenue per organization (ARPO), and enterprise tier share percentage. Order by total_mrr DESC.

---

## 2. Expected Output Shape

- **Result Grain:** 1 row: active_subs, total_mrr, arpo, enterprise_share_pct

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
python3 scripts/grade-query.py exercises/challenge/q139-saas-mrr-cohort-waterfall.md
```
