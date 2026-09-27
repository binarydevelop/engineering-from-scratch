# Drill 07: Percent of Total Contribution

**Category:** 04-window-drills  
**Target Schema:** `ecommerce`  
**Concept:** Fluency Drill  

---

## Business Requirement

> For completed orders, calculate each order's percentage contribution to total completed revenue. Project order_id, total_amount, pct_of_total. Order by total_amount DESC.

---

## 14-Question Thinking Anchor
- **What should one output row represent (Grain)?**  
  *One row per completed order.*

---

## Target Verification
When your query is ready, verify it against the test harness:

```bash
python3 scripts/grade-query.py drills/04-window-drills/drill-07.md
```
