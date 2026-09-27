# Drill 04: DynamoDB PartiQL SQL-Compatible Queries

* **Target Language:** PartiQL
* **Goal:** Build rapid muscle memory for pattern #04 without hesitation.
* **SLA Requirement:** Formulate and verify query in < 60 seconds.

## Objective
Write a clean, targeted PartiQL query to satisfy the following access pattern:
> Retrieve records for entity `PARTIQL_ID_0004` matching status `ACTIVE` and filtered by range `metric >= 40`, ordered by timestamp DESC with limit 10.

## Expected Query Structure
Identify:
1. Exact key / partition parameter.
2. Filter condition applied before or after retrieval.
3. Index required to prevent scanning.

## Exercise Prompt
Formulate your query below:
```text
-- Write your PartiQL query here
```

## Self-Check Validation
- [ ] Query strictly identifies the target partition
- [ ] No unbounded scans or full-collection filters
- [ ] Output matches required 10-record boundary
