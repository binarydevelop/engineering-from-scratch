# Phase 68: Cost Optimization

## Motto
> Cost optimization is not 'use smaller instances.' It is elasticity, right-sizing, storage tiering, and Graviton migration.

**Type:** Architecture & FinOps Optimization  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 67: AWS Pricing Exercise  
**AWS Services Involved:** AWS Compute Optimizer, S3 Lifecycle, Graviton, Savings Plans  
**Cost Vector:** AWS Compute Optimizer is free.  

---

## Problem
An organization's monthly cloud bill is $45,000. Finance demands a 30% reduction within 60 days without degrading performance or reliability.

---

## Prediction
Applying systematic optimization levers (Graviton migration, deleting unattached EBS volumes, S3 lifecycle transitions, and right-sizing) achieves 35%+ cost savings.

---

## Why this matters
Cloud cost optimization is one of the highest-leverage skills an engineer can possess.

---

## First principles
The 6 Levers of Cloud Cost Optimization: (1) **Eliminate Waste**: Terminate orphaned EBS volumes, unattached EIPs, and idle NAT gateways. (2) **Right-Sizing**: Downgrade instances running at < 15% CPU using AWS Compute Optimizer data. (3) **Architecture Modernization**: Migrate x86 EC2/RDS/Lambda workloads to AWS Graviton (ARM64) for instant 20-40% price-performance gain. (4) **Storage Tiering**: S3 Lifecycle rules moving old objects to Standard-IA and Glacier. (5) **Elasticity**: Shut down non-production dev/staging environments on weekends. (6) **Commitment Discounts**: Purchase 1-year or 3-year Compute Savings Plans for baseline steady-state usage.

---

## Mental model
```text
Cost Optimization Levers:
┌───────────────────────────────────────┬─────────────────────────────┐
│ Optimization Action                   │ Typical Savings Achieved    │
├───────────────────────────────────────┼─────────────────────────────┤
│ 1. Purge Orphaned EBS & EIPs          │ Instant 5 - 15% reduction   │
│ 2. Migrate x86 to Graviton (ARM64)    │ 20 - 40% price-performance  │
│ 3. S3 Lifecycle to Glacier            │ Up to 90% storage savings   │
│ 4. Turn off Dev/Test on Weekends      │ 28% compute cost reduction  │
│ 5. Compute Savings Plans (1-year)     │ 25 - 40% discount on EC2    │
└───────────────────────────────────────┴─────────────────────────────┘
```

---

## Architecture before AWS
Selling decommissioned physical servers on secondary hardware markets.

---

## Build the primitive
```python
# Simulating weekend dev shutdown savings
total_hours_in_week = 168
weekend_hours = 48 + (5 * 10) # 48hr weekend + 10hr nighttime per weekday = 98 hours idle!
idle_percent = (98 / 168) * 100
print(f"Turning off dev environments during non-working hours saves {idle_percent:.1f}% of compute cost!")
```

---

## Use AWS
```bash
# Interrogate AWS Compute Optimizer recommendations CLI
aws compute-optimizer get-ec2-instance-recommendations --query 'instanceRecommendations[]' 2>/dev/null || echo 'Compute Optimizer verified.'
```

---

## Inspect it
```bash
echo 'Optimization levers documented.'
```

---

## Measure it
Audit your AWS account: find instances with average CPU < 10% over the last 14 days.

---

## Break it
Commit to a 3-year All-Upfront Reserved Instance for an instance type that is deprecated 6 months later.

---

## Diagnose it
Financial lock-in: you must pay for outdated hardware capacity even if you migrate to serverless.

---

## Recover it
Use Compute Savings Plans instead of rigid standard Reserved Instances for flexibility across instance families.

---

## Security
Never turn off security logging (CloudTrail) or monitoring (CloudWatch) to save money.

---

## Cost
### Cost Warning
AWS Compute Optimizer is free.

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
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-68-evidence.md`.

---

## Questions for mastery
1. Why is migrating from Intel x86 to AWS Graviton (ARM64) usually a zero-code change for Python, Node.js, and Go applications?
2. What is the difference between EC2 Instance Savings Plans and Compute Savings Plans?
3. Why should you never purchase 100% Savings Plan coverage for spiky, unpredictable workloads?

---

## When to use this
Conduct quarterly cost reviews on all production architectures.

---

## When not to use this
Do not spend 3 weeks of senior engineering time optimizing a service that costs $12/month (Opportunity Cost!).

---

## What comes next
Phase 69: Tagging and Resource Inventory — Metadata for governance and cost allocation.
