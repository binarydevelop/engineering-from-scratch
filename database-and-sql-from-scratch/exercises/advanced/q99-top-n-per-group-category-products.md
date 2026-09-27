# Exercise Q99: Q99 Top N Per Group Category Products

**Tier:** Advanced  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Window`, `Top-N`, `DENSE_RANK`  

---

## 1. Business Requirement

> Find top 2 highest revenue products in each category. Join order_items, orders, products. Use DENSE_RANK. Order by category_id ASC, rank ASC, product_name ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: category_id, product_name, product_rev, rank

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
python3 scripts/grade-query.py exercises/advanced/q99-top-n-per-group-category-products.md
```
