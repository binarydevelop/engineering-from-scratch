# Exercise Q75: Q75 Duplicate Email Detection

**Tier:** Intermediate  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Data Hygiene`, `HAVING`  

---

## 1. Business Requirement

> Write a data hygiene query checking if any email address appears more than once in customers table. Project email, occurrence_count. (Should return 0 rows).

---

## 2. Expected Output Shape

- **Result Grain:** 0 rows expected: email, occurrence_count

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
python3 scripts/grade-query.py exercises/intermediate/q75-duplicate-email-detection.md
```
