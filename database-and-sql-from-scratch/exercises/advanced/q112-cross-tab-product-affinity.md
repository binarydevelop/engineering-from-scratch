# Exercise Q112: Q112 Cross Tab Product Affinity

**Tier:** Advanced  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Market Basket`, `Self Join`  

---

## 1. Business Requirement

> Market Basket Analysis: find pairs of products frequently bought together in the same order. Project prod_a_id, prod_b_id, co_purchase_count where prod_a_id < prod_b_id. Order by co_purchase_count DESC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: prod_a_id, prod_b_id, co_purchase_count

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
python3 scripts/grade-query.py exercises/advanced/q112-cross-tab-product-affinity.md
```
