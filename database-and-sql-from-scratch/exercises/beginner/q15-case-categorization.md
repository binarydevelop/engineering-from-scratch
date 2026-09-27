# Exercise Q15: Q15 Case Categorization

**Tier:** Beginner  
**Target Schema:** `ecommerce`  
**Concept Tags:** `CASE`, `Conditional Logic`  

---

## 1. Business Requirement

> Classify each customer's status: if 'active' then 'Verified User', if 'suspended' then 'Action Required', else 'Unknown'. Return email, status, and status_label. Order by id ASC.

---

## 2. Expected Output Shape

- **Result Grain:** 15 rows, 3 columns: email, status, status_label

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
python3 scripts/grade-query.py exercises/beginner/q15-case-categorization.md
```
