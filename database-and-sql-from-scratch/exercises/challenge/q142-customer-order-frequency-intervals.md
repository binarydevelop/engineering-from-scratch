# Exercise Q142: Q142 Customer Order Frequency Intervals

**Tier:** Challenge  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Window`, `Intervals`  

---

## 1. Business Requirement

> For customers with at least 3 orders, calculate the average interval in days between their successive orders. Project customer_id, order_count, avg_days_between_orders. Order by avg_days_between_orders ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: customer_id, order_count, avg_days_between_orders

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
python3 scripts/grade-query.py exercises/challenge/q142-customer-order-frequency-intervals.md
```
