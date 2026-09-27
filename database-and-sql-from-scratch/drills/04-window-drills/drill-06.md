# Drill 06: Moving Average (3-Order Moving Window)

**Category:** 04-window-drills  
**Target Schema:** `ecommerce`  
**Concept:** Fluency Drill  

---

## Business Requirement

> Calculate 3-order moving average of completed order totals (current row and preceding 2 rows). Project order_id, order_date, total_amount, moving_avg. Order by order_date ASC.

---

## 14-Question Thinking Anchor
- **What should one output row represent (Grain)?**  
  *One row per completed order.*

---

## Target Verification
When your query is ready, verify it against the test harness:

```bash
python3 scripts/grade-query.py drills/04-window-drills/drill-06.md
```
