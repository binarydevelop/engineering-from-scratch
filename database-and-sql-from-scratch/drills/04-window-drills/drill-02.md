# Drill 02: Running Total (Cumulative Revenue)

**Category:** 04-window-drills  
**Target Schema:** `ecommerce`  
**Concept:** Fluency Drill  

---

## Business Requirement

> Calculate running total revenue over completed orders ordered by order_date ASC. Project order_id, order_date, total_amount, running_revenue. Order by order_date ASC.

---

## 14-Question Thinking Anchor
- **What should one output row represent (Grain)?**  
  *One row per completed order.*

---

## Target Verification
When your query is ready, verify it against the test harness:

```bash
python3 scripts/grade-query.py drills/04-window-drills/drill-02.md
```
