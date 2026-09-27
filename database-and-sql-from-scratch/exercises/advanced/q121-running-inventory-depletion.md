# Exercise Q121: Q121 Running Inventory Depletion

**Tier:** Advanced  
**Target Schema:** `ecommerce`  
**Concept Tags:** `Inventory`, `Window Simulation`  

---

## 1. Business Requirement

> Simulate inventory depletion: for product 1, show orders requesting it in order_date order, quantity requested, and remaining simulated stock starting from 45. Order by order_date ASC.

---

## 2. Expected Output Shape

- **Result Grain:** Rows: order_id, order_date, quantity, remaining_stock

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
python3 scripts/grade-query.py exercises/advanced/q121-running-inventory-depletion.md
```
