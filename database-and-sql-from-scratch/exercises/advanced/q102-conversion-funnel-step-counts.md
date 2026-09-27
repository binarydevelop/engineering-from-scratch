# Exercise Q102: Q102 Conversion Funnel Step Counts

**Tier:** Advanced  
**Target Schema:** `analytics`  
**Concept Tags:** `Funnel`, `Conversion`  

---

## 1. Business Requirement

> Compute complete e-commerce conversion funnel counts: step 1 (page_view), step 2 (sign_up), step 3 (view_product), step 4 (add_to_cart), step 5 (purchase). Return unique user count at each stage.

---

## 2. Expected Output Shape

- **Result Grain:** 1 row, 5 columns: step1_view, step2_signup, step3_prod, step4_cart, step5_purchase

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
python3 scripts/grade-query.py exercises/advanced/q102-conversion-funnel-step-counts.md
```
