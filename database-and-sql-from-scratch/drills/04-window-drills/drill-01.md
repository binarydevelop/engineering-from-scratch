# Drill 01: ROW_NUMBER (Latest Order per Customer)

**Category:** 04-window-drills  
**Target Schema:** `ecommerce`  
**Concept:** Fluency Drill  

---

## Business Requirement

> Find each customer's most recent order. Select customer_id, order_id, and order_date. Order by customer_id ASC.

---

## 14-Question Thinking Anchor
- **What should one output row represent (Grain)?**  
  *One row per customer.*

---

## Target Verification
When your query is ready, verify it against the test harness:

```bash
python3 scripts/grade-query.py drills/04-window-drills/drill-01.md
```
