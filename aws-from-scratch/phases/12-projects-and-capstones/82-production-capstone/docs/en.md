# Phase 82: Production-Like AWS Capstone

## Motto
> The complete synthesis: Every component justified. Every byte traced. Every failure accounted for. Every dollar modeled.

**Type:** Capstone 2 & Enterprise Production Synthesis  
**Time Estimate:** ~120 minutes  
**Prerequisites:** Phase 76: Project: Containerized Production Application  
**AWS Services Involved:** CloudFront, ALB, ECS Fargate, RDS PostgreSQL Multi-AZ, SQS, S3, KMS, CloudWatch  
**Cost Vector:** Detailed parametric cost model: ~$0.08/hour for testing (~$2.00 for a 24-hour test lab).  

---

## Problem
Junior engineers know individual services in isolation, but fail when asked to integrate networking, IAM, compute, storage, asynchronous queues, caching, observability, and cost controls into a single cohesive production architecture.

---

## Prediction
Building a full-scale resilient production architecture satisfying all 6 pillars of the Well-Architected Framework proves end-to-end cloud engineering mastery.

---

## Why this matters
This is Capstone 2: the comprehensive capstone project synthesizing the entire curriculum.

---

## First principles
The production architecture integrates: CloudFront (edge caching & TLS) -> ALB (Layer 7 path routing) -> ECS Fargate in private subnets -> RDS PostgreSQL Multi-AZ (synchronous state) + SQS with DLQ (asynchronous work) + S3 with KMS encryption (durable object storage) + CloudWatch structured telemetry.

---

## Mental model
```text
Capstone 2 Complete Architecture:
[ Global Users ] ──► [ CloudFront CDN (TLS 1.3) ]
                             │
            ┌────────────────┴────────────────┐
            ▼ Static Assets                   ▼ Dynamic APIs (/api/*)
    [ Private S3 Bucket ]             [ ALB (Public Multi-AZ) ]
                                              │
                      ┌───────────────────────┴───────────────────────┐
                      ▼                                               ▼
             [ AZ-A Private Subnet ]                         [ AZ-B Private Subnet ]
             [ ECS Fargate Container ]                       [ ECS Fargate Container ]
                      │                                               │
                      └───────────────────────┬───────────────────────┘
                                              │
                    ┌─────────────────────────┼─────────────────────────┐
                    ▼ Relational State        ▼ Async Buffer            ▼ Document Storage
             [ RDS PostgreSQL ]        [ Amazon SQS + DLQ ]      [ Encrypted S3 Bucket ]
             (Multi-AZ Standby)        (Orders Worker Cluster)   (KMS Customer Key)
```

---

## Architecture before AWS
Enterprise multi-tier architecture spanning multiple physical colocation facilities.

---

## Build the primitive
```python
with open('projects/project-08-production-capstone/README.md') as f:
    print("Capstone 2 Specification verified:", "Production-Grade Resilient Architecture" in f.read())
```

---

## Use AWS
```bash
# Implementation and teardown guide in projects/project-08-production-capstone/README.md
```

---

## Inspect it
```bash
cat projects/project-08-production-capstone/README.md
```

---

## Measure it
Audit against the 6 pillars: measure RTO (< 90s), RPO (0s), p99 latency (< 35ms), and running cost (~$0.08/hr).

---

## Break it
Execute the comprehensive chaos testing plan detailed in Capstone 2.

---

## Diagnose it
Inspect CloudWatch distributed traces and alarms to identify root causes.

---

## Recover it
Automated self-healing and failover restores 100% operational capacity.

---

## Security
Zero public compute or database subnets. Least-privilege IAM task roles. KMS Customer Managed Keys.

---

## Cost
### Cost Warning
Detailed parametric cost model: ~$0.08/hour for testing (~$2.00 for a 24-hour test lab).

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
Follow teardown commands in `projects/project-08-production-capstone/README.md`.
```

---

## Verify cleanup
```bash
./scripts/cleanup-check.sh
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-82-evidence.md`.

---

## Questions for mastery
1. How does each tier in Capstone 2 achieve independent failure domain isolation?
2. Where does state live in this architecture, and why can compute nodes be terminated at any time without data loss?
3. How does this architecture satisfy all 6 pillars of the AWS Well-Architected Framework?

---

## When to use this
Use this blueprint as the foundational production pattern for modern enterprise cloud systems.

---

## When not to use this
Do not deploy this full stack for simple single-developer personal websites (use Project 01 or Project 03).

---

## What comes next
Phase 83: Failure Day — Injecting intentional chaos across all infrastructure layers.
