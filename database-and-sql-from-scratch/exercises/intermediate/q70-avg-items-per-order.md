# Exercise Q70: Q70 Avg Items Per Order

**Tier:** Intermediate  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Derived Table`, `Aggregates`  

---

## 1. Business Requirement

> Calculate the average number of unique items and average total quantity per completed order. Return avg_unique_items and avg_quantity rounded to 2 decimals.

---

## 2. Expected Output Shape

- **Result Grain:** 1 row: avg_unique_items, avg_quantity

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
python3 scripts/grade-query.py exercises/intermediate/q70-avg-items-per-order.md
```
