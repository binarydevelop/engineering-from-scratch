# Exercise Q10: Q10 Nullif Division Safeguard

**Tier:** Beginner  
**Target Schema:** `ecommerce`  
**Concept Tags:** `NULL`, `NULLIF`  

---

## 1. Business Requirement

> Calculate ratio of reorder_level to stock_quantity for inventory items. Use NULLIF to prevent division by zero when stock_quantity = 0. Project product_id, stock_quantity, reorder_level, ratio. Order by product_id ASC.

---

## 2. Expected Output Shape

- **Result Grain:** 12 rows, 4 columns: product_id, stock_quantity, reorder_level, ratio

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
python3 scripts/grade-query.py exercises/beginner/q10-nullif-division-safeguard.md
```
