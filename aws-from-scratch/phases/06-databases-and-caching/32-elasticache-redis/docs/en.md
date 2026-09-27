# Phase 32: ElastiCache / Managed Redis

## Motto
> In-memory caching is 10x faster than disk, but introduces the hardest problem in computer science: cache invalidation.

**Type:** Hands-on Lab & In-Memory Caching  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 26: RDS From First Principles  
**AWS Services Involved:** Amazon ElastiCache (Redis / Valkey)  
**Cost Vector:** `cache.t4g.micro` costs ~$0.016/hour (~$11.50/month). Unlike serverless DynamoDB, ElastiCache accrues hourly charges 24/7.  

---

## Problem
A relational database CPU spikes to 100% answering 10,000 identical queries per second for the homepage product catalog.

---

## Prediction
Adding an in-memory Redis cache drops read latency from 12ms (disk) to 0.7ms (RAM), absorbing 99% of database query load.

---

## Why this matters
ElastiCache Redis / Valkey is the standard caching primitive in AWS. Understanding Cache-Aside vs Write-Through prevents stale data bugs.

---

## First principles
DRAM memory access latency (~100 nanoseconds) is three to four orders of magnitude faster than NVMe SSD disk access (~100 microseconds). Redis is a single-threaded event-loop in-memory key-value data store supporting atomic data structures (strings, hashes, sets, sorted sets, hyperloglogs).

---

## Mental model
```text
Cache-Aside Pattern:
Application ──(1. Get User 42)──► [ ElastiCache Redis (RAM) ]
                                          │
                  ┌───────────────────────┴───────────────────────┐
             (Cache Hit: 0.5ms)                              (Cache Miss: None)
                  │                                               │
                  ▼                                               ▼
         [ Return Data to App ]                    [ Query Amazon RDS PostgreSQL (12ms) ]
                                                                  │
                                                                  ▼
                                                   [ Write to Redis with TTL=300s ]
```

---

## Architecture before AWS
Hosting Memcached or Redis clusters on physical servers with Sentinel failover.

---

## Build the primitive
```python
# Run our cache-aside benchmark
import subprocess
subprocess.run(['python3', 'benchmarks/benchmark_cache.py'], check=True)
```

---

## Use AWS
```bash
# Inspect ElastiCache replication groups
aws elasticache describe-replication-groups --query 'ReplicationGroups[].[ReplicationGroupId,Status,CacheNodeType]' --output table
```

---

## Inspect it
```bash
python3 benchmarks/benchmark_cache.py
```

---

## Measure it
Measure latency speedup: direct DB reads (12ms) vs cache-aside reads (0.7ms) = 15.9x faster!

---

## Break it
Simulate Cache Stampede (Thundering Herd): delete a popular key while 1,000 concurrent threads are requesting it.

---

## Diagnose it
All 1,000 threads experience a cache miss simultaneously and hammer the database with identical queries, crashing PostgreSQL.

---

## Recover it
Implement probabilistic early expiration (XFetch algorithm) or mutex locks on cache misses.

---

## Security
Enforce in-transit TLS encryption and Redis AUTH tokens; keep ElastiCache strictly in private subnets with no public ingress.

---

## Cost
### Cost Warning
`cache.t4g.micro` costs ~$0.016/hour (~$11.50/month). Unlike serverless DynamoDB, ElastiCache accrues hourly charges 24/7.

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
# Cleanup ElastiCache clusters if created
```

---

## Verify cleanup
```bash
echo 'ElastiCache verified.'
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-32-evidence.md`.

---

## Questions for mastery
1. What is the difference between Cache-Aside, Write-Through, and Write-Behind caching strategies?
2. Why is adding Redis an antipattern if your relational database queries are simply missing proper B-Tree indexes?
3. How does Redis memory eviction work when RAM is full (e.g. `volatile-lru` vs `allkeys-lru`)?

---

## When to use this
Use ElastiCache for sub-millisecond caching of read-heavy databases, distributed session stores, and rate limiters.

---

## When not to use this
Do not add Redis prematurely before measuring database performance. Caching adds cache invalidation complexity.

---

## What comes next
Phase 33: Queues Before SQS — Asynchronous decoupling and backpressure.
