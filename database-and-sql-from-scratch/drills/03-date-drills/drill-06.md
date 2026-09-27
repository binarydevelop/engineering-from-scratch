# Drill 06: Time Difference Between Consecutive Events

**Category:** 03-date-drills  
**Target Schema:** `analytics`  
**Concept:** Fluency Drill  

---

## Business Requirement

> For session 'b0000000-0000-0000-0000-000000000001', calculate seconds elapsed between consecutive events. Select event_name, event_timestamp, and seconds_since_prev. Order by event_timestamp ASC.

---

## 14-Question Thinking Anchor
- **What should one output row represent (Grain)?**  
  *One row per event in session.*

---

## Target Verification
When your query is ready, verify it against the test harness:

```bash
python3 scripts/grade-query.py drills/03-date-drills/drill-06.md
```
