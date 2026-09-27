# Exercise Q96: Q96 Window Lead Time To Next Order

**Tier:** Advanced  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Window`, `LEAD`, `Repurchase`  

---

## 1. Business Requirement

> For customer 1, calculate days elapsed between current order and the NEXT order using LEAD. Project order_id, order_date, next_order_date, days_to_next. Order by order_date ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: order_id, order_date, next_order_date, days_to_next

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
python3 scripts/grade-query.py exercises/advanced/q96-window-lead-time-to-next-order.md
```
