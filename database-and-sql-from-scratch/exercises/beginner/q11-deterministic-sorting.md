# Exercise Q11: Q11 Deterministic Sorting

**Tier:** Beginner  
**Target Schema:** `ecommerce`  
**Concept Tags:** `ORDER BY`, `Tie-Breaking`  

---

## 1. Business Requirement

> Select all orders sorted by status ascending, then by total_amount descending, and finally by id ascending as a deterministic tie-breaker.

---

## 2. Expected Output Shape

- **Result Grain:** 17 rows, 4 columns: id, customer_id, status, total_amount

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
python3 scripts/grade-query.py exercises/beginner/q11-deterministic-sorting.md
```
