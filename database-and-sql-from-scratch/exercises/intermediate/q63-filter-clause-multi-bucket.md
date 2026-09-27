# Exercise Q63: Q63 Filter Clause Multi Bucket

**Tier:** Intermediate  
**Target Schema:** `ecommerce`  
**Concept Tags:** `FILTER Clause`, `Aggregates`  

---

## 1. Business Requirement

> Calculate count of orders, count of credit_card payments, and count of paypal payments by customer_id. Order by customer_id ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: customer_id, total_orders, cc_payments, paypal_payments

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
python3 scripts/grade-query.py exercises/intermediate/q63-filter-clause-multi-bucket.md
```
