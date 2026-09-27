# Exercise Q44: Q44 Conditional Aggregation Pivot

**Tier:** Intermediate  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Aggregate`, `CASE`, `Pivoting`  

---

## 1. Business Requirement

> Produce a single-row status breakdown showing completed_count, cancelled_count, refunded_count, and pending_count across all orders.

---

## 2. Expected Output Shape

- **Result Grain:** 1 row, 4 columns: completed_count, cancelled_count, refunded_count, pending_count

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
python3 scripts/grade-query.py exercises/intermediate/q44-conditional-aggregation-pivot.md
```
