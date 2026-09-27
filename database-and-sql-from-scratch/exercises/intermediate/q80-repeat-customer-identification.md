# Exercise Q80: Q80 Repeat Customer Identification

**Tier:** Intermediate  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Cohort`, `HAVING`  

---

## 1. Business Requirement

> Identify repeat customers (customers with 2 or more completed orders). Project customer email and completed_order_count. Order by completed_order_count DESC, email ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: email, completed_order_count

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
python3 scripts/grade-query.py exercises/intermediate/q80-repeat-customer-identification.md
```
