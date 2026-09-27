# Phase 73: Project: Highly Available Web App

## Motto
> Multi-AZ redundancy at every tier: ALB, stateless Auto Scaling instances, and synchronous Multi-AZ RDS.

**Type:** Architecture Project & Production Deployment  
**Time Estimate:** ~90 minutes  
**Prerequisites:** Phase 24: Multi-AZ Application  
**AWS Services Involved:** ALB, EC2 Auto Scaling, RDS PostgreSQL Multi-AZ, VPC  
**Cost Vector:** Baseline running cost is ~$45-55/month. Run for 1 hour to test, then terminate immediately!  

---

## Problem
Single-server applications fail completely when host hardware dies, when traffic spikes 5x, or when a datacenter facility loses power.

---

## Prediction
Deploying an ALB in front of a multi-AZ stateless Auto Scaling Group with a multi-AZ RDS database eliminates all single points of failure.

---

## Why this matters
This is Project 02: the classic 3-tier enterprise high-availability web architecture.

---

## First principles
Every tier is redundant across independent availability zones. State is completely externalized to the database. Compute nodes are disposable cattle managed by the Auto Scaling Group.

---

## Mental model
```text
Project 02 Architecture:
            [ Internet ] ──► [ Route 53 ] ──► [ ALB (Public Multi-AZ) ]
                                                     │
                    ┌────────────────────────────────┴────────────────────────────────┐
                    ▼                                                                 ▼
           [ AZ-A Private Subnet ]                                           [ AZ-B Private Subnet ]
           ┌──────────────────────┐                                          ┌──────────────────────┐
           │ EC2 App (AutoScaling)│                                          │ EC2 App (AutoScaling)│
           └──────────┬───────────┘                                          └──────────┬───────────┘
                      │                                                                 │
                      └───────────────────────────────┬─────────────────────────────────┘
                                                      │ TCP 5432
                                                      ▼
                                          [ Amazon RDS Multi-AZ ]
                                          Primary (AZ-A) ══(Sync Rep)══► Standby (AZ-B)
```

---

## Architecture before AWS
Active-passive physical server pairs with shared SAN storage and heartbeat failover.

---

## Build the primitive
```python
with open('projects/project-02-ha-webapp/README.md') as f:
    print("Project 02 loaded:", "ALB + ASG + Multi-AZ RDS" in f.read())
```

---

## Use AWS
```bash
# Reference implementation in projects/project-02-ha-webapp/README.md
```

---

## Inspect it
```bash
aws elbv2 describe-target-health --target-group-arn $TG_ARN --output table
```

---

## Measure it
Measure failover availability: kill AZ-A instance; verify 0.00% client request drop.

---

## Break it
Trigger RDS forced failover during high read/write traffic.

---

## Diagnose it
Primary flips to AZ-B standby; application reconnects within 60 seconds.

---

## Recover it
The application pool re-establishes connections automatically.

---

## Security
Chain security groups: ALB -> App SG -> RDS SG. No public access to app or DB tiers.

---

## Cost
### Cost Warning
Baseline running cost is ~$45-55/month. Run for 1 hour to test, then terminate immediately!

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
Follow teardown commands in `projects/project-02-ha-webapp/README.md`.
```

---

## Verify cleanup
```bash
./scripts/cleanup-check.sh
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-73-evidence.md`.

---

## Questions for mastery
1. Why must the compute instances be strictly stateless for Auto Scaling to work without data loss?
2. What happens if an entire AWS datacenter facility is destroyed by a flood in this architecture?
3. How does Security Group chaining isolate the database tier from direct internet traffic?

---

## When to use this
Use for relational, transactional web applications with predictable baseline traffic.

---

## When not to use this
Do not use for microservices with huge idle periods where 24/7 running costs waste money.

---

## What comes next
Phase 74: Project: Serverless API — Building a scale-to-zero serverless API.
