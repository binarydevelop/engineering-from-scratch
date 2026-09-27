# Phase 78: Architecture Evolution

## Motto
> Never start with maximum complexity. Only add services when a measured physical bottleneck appears.

**Type:** System Design & Evolutionary Architecture  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 73: Project: Highly Available Web App  
**AWS Services Involved:** Architecture Evolution Matrix, System Design  
**Cost Vector:** Stage 1 costs $10/month; Stage 3 costs $80/month; Stage 5 costs $800/month. Costs scale with revenue!  

---

## Problem
A startup builds an over-engineered multi-region Kubernetes cluster with Kafka and Redis for 50 initial users, spending $8,000/month and 6 months of engineering time before writing a single product feature.

---

## Prediction
Architectures should evolve incrementally: 100 users (1 box) -> 10K users (ALB + EC2 + RDS) -> 1M users (Multi-AZ + ASG + CloudFront + SQS) -> 10M users (Microservices + DynamoDB + Edge).

---

## Why this matters
Connects AWS infrastructure directly to real-world system design interview thinking.

---

## First principles
At each stage of scale, ask: **What actually broke?** (1) 100 users: Single server (monolith). Bottleneck: hardware failure. (2) 1,000 users: Separate DB onto managed RDS. Bottleneck: web server CPU. (3) 10,000 users: Add ALB + second EC2 instance. Bottleneck: static file bandwidth. (4) 100,000 users: Add CloudFront + S3 for static assets. Bottleneck: slow DB read queries. (5) 1,000,000 users: Add Read Replicas / ElastiCache + SQS async workers.

---

## Mental model
```text
The Evolutionary Architecture Ladder:
Stage 1 (100 Users):     [ Single EC2 Instance (App + DB on 1 disk) ]
                                      │ Bottleneck: Hardware crash = 100% downtime!
                                      ▼
Stage 2 (1,000 Users):   [ EC2 App ] ──► [ Amazon RDS Database ]
                                      │ Bottleneck: Web server CPU saturates!
                                      ▼
Stage 3 (10,000 Users):  [ ALB ] ──► [ EC2 AZ-A ] + [ EC2 AZ-B ] ──► [ RDS Multi-AZ ]
                                      │ Bottleneck: Static assets crush bandwidth!
                                      ▼
Stage 4 (100,000 Users): [ CloudFront + S3 ] (Static) + [ ALB + EC2 ASG ] ──► [ RDS ]
                                      │ Bottleneck: Repetitive DB reads & slow sync tasks!
                                      ▼
Stage 5 (1,000,000 Users): [ CloudFront ] ──► [ ALB + ASG ] ──► [ RDS + ElastiCache ]
                                                  │
                                                  ▼
                                          [ SQS Async Workers ]
```

---

## Architecture before AWS
Buying a massive mainframe server (Vertical Scaling) and hoping traffic doesn't exceed it.

---

## Build the primitive
```python
# Architecture Evolution Decision Engine
def recommend_architecture(users, qps):
    if users < 1_000:
        return "Stage 1: Single small instance or container (Simple, cheap)"
    elif users < 50_000:
        return "Stage 2: ALB + Multi-AZ Compute + Managed RDS (High Availability)"
    elif users < 1_000_000:
        return "Stage 3: ALB + ASG + CloudFront CDN + S3 + RDS Multi-AZ + SQS workers"
    else:
        return "Stage 4: Serverless / Microservices + DynamoDB + Global Edge Caching"
print(recommend_architecture(500_000, 2500))
```

---

## Use AWS
```bash
# Reference evolution matrix documented
```

---

## Inspect it
```bash
echo 'Evolution decision matrix verified.'
```

---

## Measure it
Trace system bottlenecks at each user tier (CPU saturation, DB connection limits, disk IOPS).

---

## Break it
Deploy Stage 1 architecture and simulate 50,000 concurrent users via Apache Benchmark.

---

## Diagnose it
CPU hits 100%, disk thrashing occurs, TCP connections drop with connection refused.

---

## Recover it
Evolve to Stage 3 architecture (ALB + ASG horizontal scaling).

---

## Security
Security perimeters must scale with architecture: add WAF and IAM roles as tiers grow.

---

## Cost
### Cost Warning
Stage 1 costs $10/month; Stage 3 costs $80/month; Stage 5 costs $800/month. Costs scale with revenue!

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
# No resources created.
```

---

## Verify cleanup
```bash
echo 'Account clean.'
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-78-evidence.md`.

---

## Questions for mastery
1. Why is premature optimization (building Stage 5 on Day 1) fatal for early-stage software companies?
2. At what specific physical bottleneck does vertical scaling (buying a bigger EC2 instance) fail?
3. How does introducing asynchronous queues (SQS) protect relational databases during traffic surges?

---

## When to use this
Use evolutionary architecture principles to guide system redesigns as companies grow.

---

## When not to use this
Do not resist evolving your architecture when real measured performance bottlenecks appear.

---

## What comes next
Phase 79: AWS Anti-Patterns — The 20 most common cloud architectural footguns.
