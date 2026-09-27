# Exercise Q79: Q79 Top Spending Cities

**Tier:** Intermediate  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Geography`, `JOIN`  

---

## 1. Business Requirement

> Determine total completed revenue generated per customer city. Join customers, orders, addresses. Project city, total_revenue. Order by total_revenue DESC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: city, total_revenue

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
python3 scripts/grade-query.py exercises/intermediate/q79-top-spending-cities.md
```
