# Exercise Q109: Q109 First Value Last Value Frame Trap

**Tier:** Advanced  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Window`, `Window Frame Trap`  

---

## 1. Business Requirement

> Demonstrate the default RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW trap with LAST_VALUE, and fix it using explicit UNBOUNDED FOLLOWING. Return order_id, total_amount, highest_order_amount.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: id, total_amount, highest_order_amount

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
python3 scripts/grade-query.py exercises/advanced/q109-first-value-last-value-frame-trap.md
```
