# Drill 10: Correlated NOT EXISTS with Date Filter

**Category:** 05-subquery-drills  
**Target Schema:** `saas`  
**Concept:** Fluency Drill  

---

## Business Requirement

> Find organizations that have NOT generated any telemetry events in March 2026. Project org id and org name. Order by org id ASC.

---

## 14-Question Thinking Anchor
- **What should one output row represent (Grain)?**  
  *One row per organization inactive in March 2026.*

---

## Target Verification
When your query is ready, verify it against the test harness:

```bash
python3 scripts/grade-query.py drills/05-subquery-drills/drill-10.md
```
