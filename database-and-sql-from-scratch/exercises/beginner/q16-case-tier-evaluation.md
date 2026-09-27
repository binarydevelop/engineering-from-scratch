# Exercise Q16: Q16 Case Tier Evaluation

**Tier:** Beginner  
**Target Schema:** `ecommerce`  
**Concept Tags:** `CASE`, `Numeric Tiers`  

---

## 1. Business Requirement

> Categorize order totals into size tiers: >= 1000 is 'Enterprise', >= 250 is 'Mid-Market', else 'Standard'. Return id, total_amount, tier. Order by total_amount DESC, id ASC.

---

## 2. Expected Output Shape

- **Result Grain:** 17 rows, 3 columns: id, total_amount, tier

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
python3 scripts/grade-query.py exercises/beginner/q16-case-tier-evaluation.md
```
