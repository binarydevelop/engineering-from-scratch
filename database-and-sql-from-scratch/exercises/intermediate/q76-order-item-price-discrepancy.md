# Exercise Q76: Q76 Order Item Price Discrepancy

**Tier:** Intermediate  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Data Integrity`, `JOIN`  

---

## 1. Business Requirement

> Compare historical unit_price recorded on order_items against current product list price in products table. Project order_id, product_name, recorded_price, current_price, difference. Order by order_id ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: order_id, product_name, recorded_price, current_price, difference

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
python3 scripts/grade-query.py exercises/intermediate/q76-order-item-price-discrepancy.md
```
