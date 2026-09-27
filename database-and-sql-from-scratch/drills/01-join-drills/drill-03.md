# Drill 03: Multi-Table Join (Order -> Items -> Products)

**Category:** 01-join-drills  
**Target Schema:** `ecommerce`  
**Concept:** Fluency Drill  

---

## Business Requirement

> Select order_id, product name, quantity, and unit_price for order 1. Order by product name ascending.

---

## 14-Question Thinking Anchor
- **What should one output row represent (Grain)?**  
  *One row per line item in order 1.*

---

## Target Verification
When your query is ready, verify it against the test harness:

```bash
python3 scripts/grade-query.py drills/01-join-drills/drill-03.md
```
