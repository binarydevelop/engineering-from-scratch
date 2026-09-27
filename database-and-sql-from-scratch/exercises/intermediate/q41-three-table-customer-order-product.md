# Exercise Q41: Q41 Three Table Customer Order Product

**Tier:** Intermediate  
**Target Schema:** `ecommerce`  
**Concept Tags:** `JOIN`, `Multi-Table`  

---

## 1. Business Requirement

> Join customers, orders, order_items, and products. Return customer email, order id, product name, and quantity for completed orders. Order by customer email ASC, order id ASC, product name ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Multiple rows: email, order_id, product_name, quantity

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
python3 scripts/grade-query.py exercises/intermediate/q41-three-table-customer-order-product.md
```
