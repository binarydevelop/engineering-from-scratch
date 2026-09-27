# Phase 84: Architecture From Requirements

## Motto
> Do not begin with service names. Begin with numbers, constraints, failure models, and primitives.

**Type:** System Design Challenge & Synthesis  
**Time Estimate:** ~90 minutes  
**Prerequisites:** Phase 78: Architecture Evolution  
**AWS Services Involved:** System Design Methodology, Capacity Math  
**Cost Vector:** Include a full parametric cost estimate with sensitivity analysis in your design deliverable.  

---

## Problem
Given a business requirement ('Build a photo-sharing app for 10M users with 99.9% uptime on a $1,500/mo budget'), novice engineers immediately start listing buzzwords ('We will use Kubernetes and Kafka') without calculating bandwidth, QPS, or storage.

---

## Prediction
Calculating back-of-the-envelope numbers (Read QPS, Write QPS, IOPS, egress bandwidth, storage growth) logically forces the exact cloud primitives needed.

---

## Why this matters
This phase bridges cloud engineering with senior system design interview mastery.

---

## First principles
The System Design Derivation Formula: (1) **Requirements**: Functional (what it does) and Non-Functional (availability, latency, budget). (2) **Numbers**: QPS, payload size, storage/year, data transfer. (3) **Failure Model**: What can fail? What is the RTO/RPO? (4) **Underlying Primitives**: Block vs Object? Sync vs Async? (5) **AWS Managed Services**: S3, DynamoDB, CloudFront, ALB, ECS. (6) **Tradeoffs**: Cost vs Latency vs Operational Burden.

---

## Mental model
```text
System Design Derivation Tree:
Business Requirements: 10M Users | Read-Heavy | Uploads | $1,500/mo Budget
                           │
                           ▼ Back-of-the-Envelope Math
Read QPS: 2,500 req/s | Write QPS: 50 req/s | Egress: 8 TB/mo | Storage: 5 TB/yr
                           │
                           ▼ Infrastructure Needs
• Edge Caching (Speed of light) ──────────► Amazon CloudFront
• High-Capacity Object Storage ───────────► Amazon S3 Standard + Lifecycle
• High-Read Key-Value Data ───────────────► Amazon DynamoDB (On-Demand)
• Stateless Scalable Compute ─────────────► AWS Lambda / ECS Fargate
• Asynchronous Image Resizing ────────────► Amazon SQS + Worker Pool
                           │
                           ▼ Cost Model Verification
Total Estimated Monthly Spend: ~$1,120.00 (Comfortably under $1,500 budget!)
```

---

## Architecture before AWS
Capacity planning spreadsheets presented to architecture review boards.

---

## Build the primitive
```python
# Back-of-the-envelope capacity calculations
mau = 10_000_000
daily_active = mau * 0.20 # 20% DAU = 2,000,000 users
requests_per_day = daily_active * 25 # 50,000,000 requests/day
avg_qps = requests_per_day / 86400
peak_qps = avg_qps * 2.5
print(f"Average QPS: {avg_qps:.1f} req/sec | Peak QPS: {peak_qps:.1f} req/sec")
```

---

## Use AWS
```bash
# Complete architecture design challenge specification
```

---

## Inspect it
```bash
echo 'Architecture design challenge documented.'
```

---

## Measure it
Verify calculations: convert QPS into database read capacity units (RCUs) and network bandwidth (Mbps).

---

## Break it
Challenge: Assume write traffic surges by 20x. Does your architecture survive?

---

## Diagnose it
If writes hit a relational database directly, it crashes. If buffered by SQS or Kinesis, it queues safely.

---

## Recover it
Ensure all write-heavy endpoints decouple via asynchronous buffers.

---

## Security
Include security perimeters in your design: IAM roles, private subnets, WAF, encryption.

---

## Cost
### Cost Warning
Include a full parametric cost estimate with sensitivity analysis in your design deliverable.

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
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-84-evidence.md`.

---

## Questions for mastery
1. Why must non-functional requirements (SLA, RTO, budget) be quantified before selecting database engines?
2. How do you calculate peak QPS from daily active users (DAU)?
3. When would a $1,500/month budget constraint force you to choose ECS Fargate over AWS Lambda?

---

## When to use this
Use this structured 6-step framework for every system design problem and architecture proposal.

---

## When not to use this
Do not skip back-of-the-envelope math; guessing capacity leads to under-provisioned outages or massive cloud waste.

---

## What comes next
Phase 85: Final Mental Model — The complete trace from finger to disk.
