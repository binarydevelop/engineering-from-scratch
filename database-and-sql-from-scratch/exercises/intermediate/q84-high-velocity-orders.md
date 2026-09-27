# Exercise Q84: Q84 High Velocity Orders

**Tier:** Intermediate  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Timing`, `Orders`  

---

## 1. Business Requirement

> Find customers who placed two different orders within 7 days of each other. Project customer_id, order_a_id, order_b_id, days_between. Order by customer_id ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: customer_id, order_a_id, order_b_id, days_between

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
python3 scripts/grade-query.py exercises/intermediate/q84-high-velocity-orders.md
```
