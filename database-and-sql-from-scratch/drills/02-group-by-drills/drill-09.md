# Drill 09: Grouping on Multiple Attributes

**Category:** 02-group-by-drills  
**Target Schema:** `ecommerce`  
**Concept:** Fluency Drill  

---

## Business Requirement

> Select status, payment_method, count of orders, and sum of total amount from orders joined with payments. Order by status ASC, payment_method ASC.

---

## 14-Question Thinking Anchor
- **What should one output row represent (Grain)?**  
  *One row per status and payment_method combination.*

---

## Target Verification
When your query is ready, verify it against the test harness:

```bash
python3 scripts/grade-query.py drills/02-group-by-drills/drill-09.md
```
