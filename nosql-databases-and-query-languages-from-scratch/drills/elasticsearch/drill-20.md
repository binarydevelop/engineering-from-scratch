# Drill 20: Elasticsearch JSON Query DSL & Aggregations

* **Target Language:** Query DSL
* **Goal:** Build rapid muscle memory for pattern #20 without hesitation.
* **SLA Requirement:** Formulate and verify query in < 60 seconds.

## Objective
Write a clean, targeted Query DSL query to satisfy the following access pattern:
> Retrieve records for entity `ELASTICSEARCH_ID_0020` matching status `ACTIVE` and filtered by range `metric >= 200`, ordered by timestamp DESC with limit 10.

## Expected Query Structure
Identify:
1. Exact key / partition parameter.
2. Filter condition applied before or after retrieval.
3. Index required to prevent scanning.

## Exercise Prompt
Formulate your query below:
```text
-- Write your Query DSL query here
```

## Self-Check Validation
- [ ] Query strictly identifies the target partition
- [ ] No unbounded scans or full-collection filters
- [ ] Output matches required 10-record boundary
