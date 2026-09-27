# Exercise Q62: Q62 Cartesian Product Risk Mitigation

**Tier:** Intermediate  
**Target Schema:** `ecommerce`  
**Concept Tags:** `JOIN`, `Safety`  

---

## 1. Business Requirement

> Generate all pairs of distinct products in category 2 where product A price < product B price. Project prod_a_name, prod_b_name, price_diff. Order by price_diff DESC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: prod_a_name, prod_b_name, price_diff

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
python3 scripts/grade-query.py exercises/intermediate/q62-cartesian-product-risk-mitigation.md
```
