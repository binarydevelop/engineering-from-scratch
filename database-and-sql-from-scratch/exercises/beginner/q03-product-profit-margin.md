# Exercise Q03: Q03 Product Profit Margin

**Tier:** Beginner  
**Target Schema:** `ecommerce`  
**Concept Tags:** `SELECT`, `Arithmetic`  

---

## 1. Business Requirement

> Calculate the absolute profit (price - cost) and markup percentage (ROUND(((price - cost) / cost) * 100, 2)) for each product. Return sku, name, profit, markup_pct. Order by profit DESC.

---

## 2. Expected Output Shape

- **Result Grain:** 12 rows, 4 columns: sku, name, profit, markup_pct

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
python3 scripts/grade-query.py exercises/beginner/q03-product-profit-margin.md
```
