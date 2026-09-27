# Drill 03: Date Interval Arithmetic (Rolling 60 Days)

**Category:** 03-date-drills  
**Target Schema:** `ecommerce`  
**Concept:** Fluency Drill  

---

## Business Requirement

> Select all orders placed between '2026-01-01' and '2026-01-01'::date + INTERVAL '45 days'. Project order id, customer_id, order_date. Order by order_date ASC.

---

## 14-Question Thinking Anchor
- **What should one output row represent (Grain)?**  
  *One row per qualifying order.*

---

## Target Verification
When your query is ready, verify it against the test harness:

```bash
python3 scripts/grade-query.py drills/03-date-drills/drill-03.md
```
