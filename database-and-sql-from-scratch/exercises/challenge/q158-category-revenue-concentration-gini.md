# Exercise Q158: Q158 Category Revenue Concentration Gini

**Tier:** Challenge  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Economics`, `Gini / Concentration`  

---

## 1. Business Requirement

> Calculate revenue concentration: proportion of total category revenue coming from the single highest-selling product in that category. Project category_name, max_product_revenue, category_revenue, concentration_pct. Order by concentration_pct DESC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: category_name, max_product_rev, category_rev, concentration_pct

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
python3 scripts/grade-query.py exercises/challenge/q158-category-revenue-concentration-gini.md
```
