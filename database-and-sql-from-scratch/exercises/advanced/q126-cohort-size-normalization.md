# Exercise Q126: Q126 Cohort Size Normalization

**Tier:** Advanced  
**Target Schema:** `analytics`  
**Concept Tags:** `Cohorts`, `Normalization`  

---

## 1. Business Requirement

> Compute signup cohort sizes for each month and return normalized user counts. Order by cohort_month ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: cohort_month, total_users

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
python3 scripts/grade-query.py exercises/advanced/q126-cohort-size-normalization.md
```
