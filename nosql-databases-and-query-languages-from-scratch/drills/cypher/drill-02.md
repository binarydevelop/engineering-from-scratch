# Drill 02: Neo4j Cypher Graph Pattern Matching

* **Target Language:** Cypher 5
* **Goal:** Build rapid muscle memory for pattern #02 without hesitation.
* **SLA Requirement:** Formulate and verify query in < 60 seconds.

## Objective
Write a clean, targeted Cypher 5 query to satisfy the following access pattern:
> Retrieve records for entity `CYPHER_ID_0002` matching status `ACTIVE` and filtered by range `metric >= 20`, ordered by timestamp DESC with limit 10.

## Expected Query Structure
Identify:
1. Exact key / partition parameter.
2. Filter condition applied before or after retrieval.
3. Index required to prevent scanning.

## Exercise Prompt
Formulate your query below:
```text
-- Write your Cypher 5 query here
```

## Self-Check Validation
- [ ] Query strictly identifies the target partition
- [ ] No unbounded scans or full-collection filters
- [ ] Output matches required 10-record boundary
