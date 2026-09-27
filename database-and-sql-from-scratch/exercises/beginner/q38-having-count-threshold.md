# Exercise Q38: Q38 Having Count Threshold

**Tier:** Beginner  
**Target Schema:** `ecommerce`  
**Concept Tags:** `HAVING`, `Threshold`  

---

## 1. Business Requirement

> Group products by category_id and filter for categories having strictly more than 1 product. Project category_id and product_count. Order by category_id ASC.

---

## 2. Expected Output Shape

- **Result Grain:** 4 rows, 2 columns: category_id, product_count

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
python3 scripts/grade-query.py exercises/beginner/q38-having-count-threshold.md
```
