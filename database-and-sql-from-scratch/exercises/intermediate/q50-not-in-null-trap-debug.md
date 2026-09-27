# Exercise Q50: Q50 Not In Null Trap Debug

**Tier:** Intermediate  
**Target Schema:** `ecommerce`  
**Concept Tags:** `NULL Trap`, `NOT IN vs NOT EXISTS`  

---

## 1. Business Requirement

> Demonstrate the safe NOT EXISTS pattern to find customers with no orders, avoiding the famous NOT IN (NULL) trap. Project id, email. Order by id ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Zero-order customers: id, email

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
python3 scripts/grade-query.py exercises/intermediate/q50-not-in-null-trap-debug.md
```
