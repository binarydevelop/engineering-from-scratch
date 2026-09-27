# Exercise Q45: Q45 Having Multi Metric

**Tier:** Intermediate  
**Target Schema:** `ecommerce`  
**Concept Tags:** `GROUP BY`, `HAVING`  

---

## 1. Business Requirement

> Find customers who have spent a total of over $1,000 across completed orders and have placed at least 2 orders. Project customer_id, total_spent, order_count. Order by total_spent DESC.

---

## 2. Expected Output Shape

- **Result Grain:** Qualifying customers: customer_id, total_spent, order_count

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
python3 scripts/grade-query.py exercises/intermediate/q45-having-multi-metric.md
```
