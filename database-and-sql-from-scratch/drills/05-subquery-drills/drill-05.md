# Drill 05: Subquery in FROM (Derived Table)

**Category:** 05-subquery-drills  
**Target Schema:** `ecommerce`  
**Concept:** Fluency Drill  

---

## Business Requirement

> From a derived table calculating customer completed order totals, calculate overall average customer spend. Return avg_spend rounded to 2 decimal places.

---

## 14-Question Thinking Anchor
- **What should one output row represent (Grain)?**  
  *Single scalar summary row.*

---

## Target Verification
When your query is ready, verify it against the test harness:

```bash
python3 scripts/grade-query.py drills/05-subquery-drills/drill-05.md
```
