# Drill 09: DynamoDB Native Query & KeyCondition Expressions

* **Target Language:** DynamoDB Native
* **Goal:** Build rapid muscle memory for pattern #09 without hesitation.
* **SLA Requirement:** Formulate and verify query in < 60 seconds.

## Objective
Write a clean, targeted DynamoDB Native query to satisfy the following access pattern:
> Retrieve records for entity `DYNAMODB_ID_0009` matching status `ACTIVE` and filtered by range `metric >= 90`, ordered by timestamp DESC with limit 10.

## Expected Query Structure
Identify:
1. Exact key / partition parameter.
2. Filter condition applied before or after retrieval.
3. Index required to prevent scanning.

## Exercise Prompt
Formulate your query below:
```text
-- Write your DynamoDB Native query here
```

## Self-Check Validation
- [ ] Query strictly identifies the target partition
- [ ] No unbounded scans or full-collection filters
- [ ] Output matches required 10-record boundary
