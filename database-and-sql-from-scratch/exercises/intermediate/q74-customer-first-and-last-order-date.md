# Exercise Q74: Q74 Customer First And Last Order Date

**Tier:** Intermediate  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Aggregate`, `MIN/MAX Dates`  

---

## 1. Business Requirement

> For each customer with orders, determine their first order date and most recent order date. Project customer_id, first_order, latest_order. Order by customer_id ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: customer_id, first_order, latest_order

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
python3 scripts/grade-query.py exercises/intermediate/q74-customer-first-and-last-order-date.md
```
