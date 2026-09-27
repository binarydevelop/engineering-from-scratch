# Exercise Q20: Q20 Date Extraction

**Tier:** Beginner  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Dates`, `EXTRACT`  

---

## 1. Business Requirement

> For all orders, extract order year and order month as integers. Return id, order_year, order_month. Order by id ASC.

---

## 2. Expected Output Shape

- **Result Grain:** 17 rows, 3 columns: id, order_year, order_month

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
python3 scripts/grade-query.py exercises/beginner/q20-date-extraction.md
```
