# Drill 06: SaaS Seat Usage by Organization

**Category:** 02-group-by-drills  
**Target Schema:** `saas`  
**Concept:** Fluency Drill  

---

## Business Requirement

> For each organization, calculate total active memberships and compare against seats purchased. Project org name, used_seats, purchased_seats. Order by org name ASC.

---

## 14-Question Thinking Anchor
- **What should one output row represent (Grain)?**  
  *One row per organization.*

---

## Target Verification
When your query is ready, verify it against the test harness:

```bash
python3 scripts/grade-query.py drills/02-group-by-drills/drill-06.md
```
