# Drill 09: Timezone Conversion Display

**Category:** 03-date-drills  
**Target Schema:** `ecommerce`  
**Concept:** Fluency Drill  

---

## Business Requirement

> Convert order_date for order 1 to 'America/New_York' timezone. Display UTC timestamp, NY timestamp, and total_amount.

---

## 14-Question Thinking Anchor
- **What should one output row represent (Grain)?**  
  *One row for order 1.*

---

## Target Verification
When your query is ready, verify it against the test harness:

```bash
python3 scripts/grade-query.py drills/03-date-drills/drill-09.md
```
