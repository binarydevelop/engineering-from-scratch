# Drill 10: Days Since Last Order per Customer

**Category:** 03-date-drills  
**Target Schema:** `ecommerce`  
**Concept:** Fluency Drill  

---

## Business Requirement

> Calculate days between customer's most recent order and '2026-03-20'::DATE. Project customer_id, latest_order_date, and days_since_last_order. Order by days_since_last_order ASC.

---

## 14-Question Thinking Anchor
- **What should one output row represent (Grain)?**  
  *One row per customer with orders.*

---

## Target Verification
When your query is ready, verify it against the test harness:

```bash
python3 scripts/grade-query.py drills/03-date-drills/drill-10.md
```
