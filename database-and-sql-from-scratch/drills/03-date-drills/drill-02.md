# Drill 02: Date Extraction (Day of Week)

**Category:** 03-date-drills  
**Target Schema:** `ecommerce`  
**Concept:** Fluency Drill  

---

## Business Requirement

> Extract day of week (0=Sunday to 6=Saturday) from order_date. Count orders per day of week. Order by day_of_week ASC.

---

## 14-Question Thinking Anchor
- **What should one output row represent (Grain)?**  
  *One row per day of week.*

---

## Target Verification
When your query is ready, verify it against the test harness:

```bash
python3 scripts/grade-query.py drills/03-date-drills/drill-02.md
```
