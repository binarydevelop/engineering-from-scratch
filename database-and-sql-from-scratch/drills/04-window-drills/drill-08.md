# Drill 08: FIRST_VALUE and LAST_VALUE in Partition

**Category:** 04-window-drills  
**Target Schema:** `banking`  
**Concept:** Fluency Drill  

---

## Business Requirement

> For account 1 ledger entries, display id, amount, entry_type, first entry amount, and last entry amount. Order by created_at ASC.

---

## 14-Question Thinking Anchor
- **What should one output row represent (Grain)?**  
  *One row per ledger entry for account 1.*

---

## Target Verification
When your query is ready, verify it against the test harness:

```bash
python3 scripts/grade-query.py drills/04-window-drills/drill-08.md
```
