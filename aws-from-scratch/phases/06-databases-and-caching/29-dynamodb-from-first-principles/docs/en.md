# Phase 29: DynamoDB From First Principles

## Motto
> DynamoDB trades relational JOINs for predictable single-digit millisecond latency at any scale.

**Type:** Hands-on Lab & Distributed Storage  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 26: RDS From First Principles  
**AWS Services Involved:** Amazon DynamoDB  
**Cost Vector:** On-Demand (Pay-Per-Request): $1.25 per million write units, $0.25 per million read units. Zero idle costs when no requests occur!  

---

## Problem
Relational databases cannot scale writes beyond a single primary server without manual sharding complexity. Traffic spikes to 100,000 writes/sec crash relational write-ahead logs.

---

## Prediction
DynamoDB partitions data horizontally across independent storage servers using the hash of the Partition Key, delivering identical 4ms latency whether storing 10 items or 10 billion items.

---

## Why this matters
DynamoDB powers Amazon's shopping cart and high-scale Tier-1 cloud services. Understanding its partition physics is mandatory for systems design.

---

## First principles
DynamoDB is a distributed B-tree/LSM-tree key-value store. It hashes the Partition Key (PK) using MD5/SHA to map items to 10GB physical storage partitions. Each partition handles up to 1,000 WCUs and 3,000 RCUs. Reads and writes bypass query planners, addressing raw storage partitions directly.

---

## Mental model
```text
DynamoDB Consistent Hashing Architecture:
Item: { PK: "USER#8821", Name: "Alice" }
         │
         ▼ Hash(PK) = 0x7a3f...
┌────────────────────────────────────────────────────────┐
│ DynamoDB Request Router Fleet                          │
└───────────────┬────────────────────────────────────────┘
                │ Routes directly to target partition
┌───────────────▼────────────────────────────────────────┐
│ Storage Partition 3 (Handles hash range 0x7000-0x7FFF) │
│ ┌─────────────────────────┐   ┌──────────────────────┐ │
│ │ Storage Node 1 (Leader) │═══│ Storage Node 2, 3    │ │
│ └─────────────────────────┘   └──────────────────────┘ │
└────────────────────────────────────────────────────────┘
```

---

## Architecture before AWS
Self-managed Apache Cassandra, HBase, or sharded MySQL clusters with manual Vitess partitioning.

---

## Build the primitive
```python
import hashlib
def get_partition(pk, num_partitions=4):
    h = int(hashlib.md5(pk.encode()).hexdigest(), 16)
    return h % num_partitions
print("User 1 lands on partition:", get_partition("USER#1001"))
print("User 2 lands on partition:", get_partition("USER#1002"))
```

---

## Use AWS
```bash
aws dynamodb create-table --table-name lab-users --attribute-definitions AttributeName=PK,AttributeType=S AttributeName=SK,AttributeType=S --key-schema AttributeName=PK,KeyType=HASH AttributeName=SK,KeyType=RANGE --billing-mode PAY_PER_REQUEST --tags Key=Project,Value=aws-from-scratch
```

---

## Inspect it
```bash
aws dynamodb describe-table --table-name lab-users --query 'Table.[TableName,TableStatus,ItemCount,BillingModeSummary]' --output table
```

---

## Measure it
Measure latency: GetItem p50 latency is typically 2-6 milliseconds regardless of table size.

---

## Break it
Attempt to run a relational query (`SELECT * FROM table WHERE email = 'x' AND age > 25`) without an index.

---

## Diagnose it
DynamoDB requires a Table Scan (reading every partition in the entire database!), which is extremely slow and burns massive RCU read capacity.

---

## Recover it
Model data by access pattern using Global Secondary Indexes (GSIs).

---

## Security
Use IAM fine-grained condition keys (`dynamodb:LeadingKeys`) to allow mobile users to access only their own user ID partition.

---

## Cost
### Cost Warning
On-Demand (Pay-Per-Request): $1.25 per million write units, $0.25 per million read units. Zero idle costs when no requests occur!

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
aws dynamodb delete-table --table-name lab-users
```

---

## Verify cleanup
```bash
echo 'DynamoDB table cleaned.'
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-29-evidence.md`.

---

## Questions for mastery
1. Why does DynamoDB not support multi-table JOIN operations?
2. What is the difference between an RCU (Read Capacity Unit) for Strongly Consistent Reads vs Eventually Consistent Reads?
3. Why is On-Demand billing almost always preferred for learning labs and spiky workloads over Provisioned Capacity?

---

## When to use this
Use DynamoDB for high-scale key-value access, user sessions, shopping carts, and serverless applications.

---

## When not to use this
Do not use DynamoDB for ad-hoc analytical OLAP queries, multi-table joins, or unknown query access patterns.

---

## What comes next
Phase 30: DynamoDB Data Modeling — Access-pattern-first single-table design.
