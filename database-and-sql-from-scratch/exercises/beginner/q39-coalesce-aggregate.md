# Exercise Q39: Q39 Coalesce Aggregate

**Tier:** Beginner  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Aggregate`, `COALESCE`  

---

## 1. Business Requirement

> Sum total refunded amount from refunds table. If no refunds match or table is empty, return 0.00. Aliased as total_refunded.

---

## 2. Expected Output Shape

- **Result Grain:** 1 row, 1 column: total_refunded

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
python3 scripts/grade-query.py exercises/beginner/q39-coalesce-aggregate.md
```
