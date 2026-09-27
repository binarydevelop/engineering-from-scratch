# Exercise Q148: Q148 Keyset Pagination Cursor Query

**Tier:** Challenge  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Pagination`, `Keyset Cursor`  

---

## 1. Business Requirement

> Execute a high-performance keyset cursor pagination step: fetch 3 orders after cursor (order_date = '2026-02-05 13:00:00+00', id = 7). Order by order_date ASC, id ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: id, order_date, total_amount

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
python3 scripts/grade-query.py exercises/challenge/q148-keyset-pagination-cursor-query.md
```
