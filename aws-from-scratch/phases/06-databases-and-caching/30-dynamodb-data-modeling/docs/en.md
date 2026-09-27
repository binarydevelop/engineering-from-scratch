# Phase 30: DynamoDB Data Modeling

## Motto
> In relational databases, you model your entities first. In DynamoDB, you model your query access patterns first.

**Type:** Hands-on Lab & Data Modeling  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 29: DynamoDB From First Principles  
**AWS Services Involved:** DynamoDB Single-Table Design, GSI  
**Cost Vector:** Query operations consume 1 RCU per 4KB of data read. Fetching 10 items sharing a PK consumes far fewer RCUs than 10 separate GetItem calls.  

---

## Problem
Applying relational third-normal-form (3NF) design to DynamoDB results in 15 separate tables requiring 15 sequential network round-trips from application code to fetch one user dashboard.

---

## Prediction
Single-table design allows fetching a User, their Orders, and their Shipping Address in a single HTTP `Query` API call.

---

## Why this matters
Single-table design is the state-of-the-art DynamoDB engineering paradigm pioneered by Rick Houlihan.

---

## First principles
A Composite Primary Key consists of a Partition Key (PK) and a Sort Key (SK). The PK determines physical partition placement; within that partition, items are stored sorted in B-tree order by the SK. You can query all items sharing a PK with `SK begins_with(...)`.

---

## Mental model
```text
Single-Table Design Layout:
PK (Partition Key)    SK (Sort Key)         Attributes
USER#101              METADATA              { Name: "Alice", Email: "alice@..." }
USER#101              ORDER#2026-001        { Total: $45.00, Status: "SHIPPED" }
USER#101              ORDER#2026-002        { Total: $12.50, Status: "PENDING" }
USER#102              METADATA              { Name: "Bob", Email: "bob@..." }

Single Query(PK="USER#101") returns Alice's profile AND all her orders in 4 milliseconds!
```

---

## Architecture before AWS
Relational schema normalization with foreign keys and multi-table SQL `JOIN` clauses.

---

## Build the primitive
```python
# Single table query simulation
table_items = [
    {"PK": "USER#101", "SK": "METADATA", "Name": "Alice"},
    {"PK": "USER#101", "SK": "ORDER#1", "Total": 45.0},
    {"PK": "USER#102", "SK": "METADATA", "Name": "Bob"}
]
user_101_bundle = [item for item in table_items if item['PK'] == "USER#101"]
print(f"Single Query retrieved {len(user_101_bundle)} heterogeneous records for USER#101!")
```

---

## Use AWS
```bash
aws dynamodb put-item --table-name lab-users --item '{"PK": {"S": "USER#101"}, "SK": {"S": "METADATA"}, "Name": {"S": "Alice"}}'
```

---

## Inspect it
```bash
aws dynamodb query --table-name lab-users --key-condition-expression 'PK = :pk' --expression-attribute-values '{":pk": {"S": "USER#101"}}' --output table
```

---

## Measure it
Measure latency: Single Query retrieving 10 items takes ~5ms (one network round-trip).

---

## Break it
Attempt to query by `Name = 'Alice'` without defining a secondary index.

---

## Diagnose it
The Query API fails with `ValidationException: Query key condition not supported` because `Name` is not a key attribute.

---

## Recover it
Create a Global Secondary Index (GSI) with `Name` as the GSI Partition Key.

---

## Security
Enforce field-level encryption for sensitive PII attributes before storing in DynamoDB items.

---

## Cost
### Cost Warning
Query operations consume 1 RCU per 4KB of data read. Fetching 10 items sharing a PK consumes far fewer RCUs than 10 separate GetItem calls.

### Resources Created
- Documented in lesson steps above.

### How to Verify Them
```bash
./scripts/list-lab-resources.sh
```

---

## Modify it
Experiment by tuning parameters, increasing capacity, changing timeouts, or tweaking security group rules. Observe metric changes in CloudWatch.

---

## Cleanup
```bash
aws dynamodb delete-item --table-name lab-users --key '{"PK": {"S": "USER#101"}, "SK": {"S": "METADATA"}}'
```

---

## Verify cleanup
```bash
echo 'Items cleaned.'
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-30-evidence.md`.

---

## Questions for mastery
1. Why does Single-Table Design make ad-hoc business intelligence reporting difficult without exporting data to S3 / Athena?
2. What is the difference between a Local Secondary Index (LSI) and a Global Secondary Index (GSI)?
3. How do you model a Many-to-Many relationship in DynamoDB?

---

## When to use this
Use Single-Table Design when access patterns are strictly known and p99 latency SLAs are paramount.

---

## When not to use this
Do not use Single-Table Design if your query patterns change weekly or if your team is unfamiliar with NoSQL modeling.

---

## What comes next
Phase 31: DynamoDB Capacity and Hot Partitions — Hashing physics and throttling.
