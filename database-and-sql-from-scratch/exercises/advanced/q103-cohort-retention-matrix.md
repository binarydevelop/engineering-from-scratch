# Exercise Q103: Q103 Cohort Retention Matrix

**Tier:** Advanced  
**Target Schema:** `analytics`  
**Concept Tags:** `Cohort Analysis`, `Retention`  

---

## 1. Business Requirement

> Calculate Month 0 and Month 1 retention counts for user cohorts: count users active in their cohort month vs active 1 month later. Order by cohort_month ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: cohort_month, cohort_size, m1_active, m1_retention_pct

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
python3 scripts/grade-query.py exercises/advanced/q103-cohort-retention-matrix.md
```
