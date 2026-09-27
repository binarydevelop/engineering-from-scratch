# Drill 05: Filtering on Left-Joined Table (Preserving Left Rows)

**Category:** 01-join-drills  
**Target Schema:** `ecommerce`  
**Concept:** Fluency Drill  

---

## Business Requirement

> Select customer email and completed order count. All customers must appear, even if count is 0. Order by order count descending, customer email ascending.

---

## 14-Question Thinking Anchor
- **What should one output row represent (Grain)?**  
  *One row per customer.*

---

## Target Verification
When your query is ready, verify it against the test harness:

```bash
python3 scripts/grade-query.py drills/01-join-drills/drill-05.md
```
