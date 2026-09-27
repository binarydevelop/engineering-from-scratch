# Exercise Q27: Q27 Numeric Rounding

**Tier:** Beginner  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Numeric`, `ROUND/CEIL/FLOOR`  

---

## 1. Business Requirement

> Calculate unit_price divided by 3 for order items in order 1. Show raw_val, rounded to 2 decimals, ceil_val, and floor_val. Order by id ASC.

---

## 2. Expected Output Shape

- **Result Grain:** 2 rows, 5 columns: id, raw_val, rounded_val, ceil_val, floor_val

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
python3 scripts/grade-query.py exercises/beginner/q27-numeric-rounding.md
```
