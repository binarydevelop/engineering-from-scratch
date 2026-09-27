# Exercise Q132: Q132 Customer Second Purchase Within 30 Days

**Tier:** Challenge  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Window`, `Repurchase Lag`  

---

## 1. Business Requirement

> Find customers whose second order occurred within 30 days of their first order. Project customer_id, first_order_date, second_order_date, days_between. Order by customer_id ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: customer_id, first_order_date, second_order_date, days_between

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
python3 scripts/grade-query.py exercises/challenge/q132-customer-second-purchase-within-30-days.md
```
