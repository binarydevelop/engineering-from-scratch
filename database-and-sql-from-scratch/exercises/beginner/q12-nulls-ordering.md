# Exercise Q12: Q12 Nulls Ordering

**Tier:** Beginner  
**Target Schema:** `ecommerce`  
**Concept Tags:** `ORDER BY`, `NULLS FIRST/LAST`  

---

## 1. Business Requirement

> Select category id, name, and parent_id. Order by parent_id ASC NULLS FIRST, then id ASC.

---

## 2. Expected Output Shape

- **Result Grain:** 8 rows, 3 columns: id, name, parent_id

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
python3 scripts/grade-query.py exercises/beginner/q12-nulls-ordering.md
```
