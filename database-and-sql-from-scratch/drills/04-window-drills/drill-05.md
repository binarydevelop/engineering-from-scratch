# Drill 05: LEAD (Next Event Name)

**Category:** 04-window-drills  
**Target Schema:** `analytics`  
**Concept:** Fluency Drill  

---

## Business Requirement

> For session 'b0000000-0000-0000-0000-000000000001', select event_name, event_timestamp, and next event_name. Order by event_timestamp ASC.

---

## 14-Question Thinking Anchor
- **What should one output row represent (Grain)?**  
  *One row per event.*

---

## Target Verification
When your query is ready, verify it against the test harness:

```bash
python3 scripts/grade-query.py drills/04-window-drills/drill-05.md
```
