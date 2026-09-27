# Exercise Q94: Q94 Window Partition By Customer Spending

**Tier:** Advanced  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Window`, `PARTITION BY`  

---

## 1. Business Requirement

> For all completed orders, compute total customer spend to date on that order and overall customer average order value side-by-side with order details. Order by customer_id ASC, order_date ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: customer_id, id, order_date, total_amount, running_customer_total, avg_customer_order

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
python3 scripts/grade-query.py exercises/advanced/q94-window-partition-by-customer-spending.md
```
