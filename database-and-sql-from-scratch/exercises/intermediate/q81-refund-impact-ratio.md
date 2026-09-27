# Exercise Q81: Q81 Refund Impact Ratio

**Tier:** Intermediate  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Finance`, `Refunds`  

---

## 1. Business Requirement

> Calculate total revenue lost to refunds compared to gross completed revenue. Return gross_rev, refunded_rev, and refund_loss_pct.

---

## 2. Expected Output Shape

- **Result Grain:** 1 row: gross_rev, refunded_rev, refund_loss_pct

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
python3 scripts/grade-query.py exercises/intermediate/q81-refund-impact-ratio.md
```
