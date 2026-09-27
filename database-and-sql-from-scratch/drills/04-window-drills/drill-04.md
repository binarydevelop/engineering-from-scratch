# Drill 04: LAG (Previous Order Amount)

**Category:** 04-window-drills  
**Target Schema:** `ecommerce`  
**Concept:** Fluency Drill  

---

## Business Requirement

> For customer 1, show order id, order_date, total_amount, and previous order amount. Order by order_date ASC.

---

## 14-Question Thinking Anchor
- **What should one output row represent (Grain)?**  
  *One row per order for customer 1.*

---

## Target Verification
When your query is ready, verify it against the test harness:

```bash
python3 scripts/grade-query.py drills/04-window-drills/drill-04.md
```
