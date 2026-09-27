# Exercise Q135: Q135 Monthly Retention Cohort Analysis

**Tier:** Challenge  
**Target Schema:** `analytics`  
**Concept Tags:** `Cohorts`, `Retention Table`  

---

## 1. Business Requirement

> Generate a cohort retention report: for each signup cohort month, display cohort size, count active in Month 0, count active in Month 1, and retention percentage. Order by cohort_month ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: cohort_month, cohort_size, m0_users, m1_users, m1_retention_rate

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
python3 scripts/grade-query.py exercises/challenge/q135-monthly-retention-cohort-analysis.md
```
