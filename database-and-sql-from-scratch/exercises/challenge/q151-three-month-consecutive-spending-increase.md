# Exercise Q151: Q151 Three Month Consecutive Spending Increase

**Tier:** Challenge  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Window`, `Triple Lag`  

---

## 1. Business Requirement

> Find customers whose spending increased for 2 consecutive calendar months (Jan -> Feb -> Mar 2026). Project customer_id, jan_spend, feb_spend, mar_spend. Order by customer_id ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: customer_id, jan_spend, feb_spend, mar_spend

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
python3 scripts/grade-query.py exercises/challenge/q151-three-month-consecutive-spending-increase.md
```
