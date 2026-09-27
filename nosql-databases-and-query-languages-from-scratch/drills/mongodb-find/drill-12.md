# Drill 12: MongoDB Find & Filter Expressions

* **Target Language:** MQL
* **Goal:** Build rapid muscle memory for pattern #12 without hesitation.
* **SLA Requirement:** Formulate and verify query in < 60 seconds.

## Objective
Write a clean, targeted MQL query to satisfy the following access pattern:
> Retrieve records for entity `MONGODB-FIND_ID_0012` matching status `ACTIVE` and filtered by range `metric >= 120`, ordered by timestamp DESC with limit 10.

## Expected Query Structure
Identify:
1. Exact key / partition parameter.
2. Filter condition applied before or after retrieval.
3. Index required to prevent scanning.

## Exercise Prompt
Formulate your query below:
```text
-- Write your MQL query here
```

## Self-Check Validation
- [ ] Query strictly identifies the target partition
- [ ] No unbounded scans or full-collection filters
- [ ] Output matches required 10-record boundary
