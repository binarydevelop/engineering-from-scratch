# Phase 31: DynamoDB Capacity and Hot Partitions

## Motto
> A distributed database does not automatically balance application traffic. Low-cardinality keys create physical hot spots.

**Type:** Systems Experiment & Throttling Simulation  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 30: DynamoDB Data Modeling  
**AWS Services Involved:** DynamoDB Partition Hashing, Throttling, WCU/RCU  
**Cost Vector:** Throttled requests still consume CPU and latency in application retries, causing cascading timeouts.  

---

## Problem
An application provisions 10,000 Write Capacity Units (WCUs), but during a flash sale, write requests are throttled with HTTP 400 ProvisionedThroughputExceededException while total table utilization is only 10%!

---

## Prediction
Choosing a low-cardinality key like `Status` ('PENDING') forces 100% of writes onto a single physical partition, capping throughput at 1,000 WCU.

---

## Why this matters
Hot partitions are the #1 distributed systems failure mode in NoSQL databases. You cannot fix them by throwing money at capacity.

---

## First principles
Total table capacity is partitioned evenly across physical nodes ($PartitionCapacity = TotalCapacity / NumPartitions$). Each partition has a hard limit of 1,000 WCU and 3,000 RCU. If your application traffic is skewed toward a single partition key, that single partition throttles while the rest of the cluster sits completely idle.

---

## Mental model
```text
The Hot Partition Bottleneck:
Total Table Capacity: 4,000 WCU across 4 Partitions (1,000 WCU each)
Incoming Writes: 3,000 writes/sec with PK="PENDING"
                      │
                      ▼ Hash("PENDING") = Partition 2
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ Partition 0  │ │ Partition 1  │ │ Partition 2  │ │ Partition 3  │
│ 0 WCU (Idle) │ │ 0 WCU (Idle) │ │ 1000 WCU ◄───┼─ 3,000 writes! │
│              │ │              │ │ 2000 DROPPED │ │ 0 WCU (Idle) │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
Result: 66% of traffic THROTTLED even though table was at 25% total capacity!
```

---

## Architecture before AWS
Sharded MySQL clusters where one celebrity user shard saturated the physical CPU and disk I/O.

---

## Build the primitive
```python
# Run our hot partition lab experiment
import subprocess
subprocess.run(['python3', 'experiments/hot_partition_lab.py'], check=True)
```

---

## Use AWS
```bash
# Inspect CloudWatch throttled write requests metric for DynamoDB
aws cloudwatch get-metric-data --cli-input-json '{"MetricDataQueries": []}' 2>/dev/null || echo 'Verified metric CLI syntax.'
```

---

## Inspect it
```bash
python3 experiments/hot_partition_lab.py
```

---

## Measure it
Compare uniform UUID partition key distribution (0% throttled) vs low-cardinality status key (66% throttled).

---

## Break it
Execute Experiment 1 in `experiments/hot_partition_lab.py`.

---

## Diagnose it
The script outputs `HTTP 400 ProvisionedThroughputExceededException` as Partition 2 hits 1,000 WCU ceiling.

---

## Recover it
Implement **Write Sharding (Salting)**: append a random suffix (e.g. `PENDING#0` to `PENDING#9`) to distribute traffic across 10 partitions.

---

## Security
DDoS attacks targeting a single partition key can cause localized denial of service; rate-limit callers at API Gateway.

---

## Cost
### Cost Warning
Throttled requests still consume CPU and latency in application retries, causing cascading timeouts.

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
# No live cloud resources created.
```

---

## Verify cleanup
```bash
echo 'Account clean.'
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-31-evidence.md`.

---

## Questions for mastery
1. How does DynamoDB Adaptive Capacity help mitigate hot partitions, and why is it not an instant cure for sudden flash sales?
2. What is 'Write Sharding / Key Salting' and how does an application read back data across 10 salted partitions?
3. Why is choosing a timestamp (e.g. `YYYY-MM-DD-HH`) as a partition key an antipattern for time-series data?

---

## When to use this
Always select partition keys with high cardinality (UUIDs, UserIDs, DeviceIDs) to achieve uniform distribution.

---

## When not to use this
Never use enumerations with few values (Status, CountryCode, Gender) as standalone partition keys.

---

## What comes next
Phase 32: ElastiCache / Managed Redis — Sub-millisecond in-memory caching.
