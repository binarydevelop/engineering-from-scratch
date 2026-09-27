# Exercise Q131: Q131 Top Three Products By Category Revenue

**Tier:** Challenge  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Window`, `Top-N`, `Business Core`  

---

## 1. Business Requirement

> Find the top 3 products by revenue for each category over completed orders, excluding refunds. Project category_name, product_name, revenue, rank. Order by category_name ASC, rank ASC, revenue DESC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: category_name, product_name, revenue, rank

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
python3 scripts/grade-query.py exercises/challenge/q131-top-three-products-by-category-revenue.md
```
