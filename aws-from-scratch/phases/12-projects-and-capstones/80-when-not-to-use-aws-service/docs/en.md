# Phase 80: When NOT to Use an AWS Service

## Motto
> Managed service != automatically correct design. Requirements dictate the architecture.

**Type:** Architecture Decision Framework  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 79: AWS Anti-Patterns  
**AWS Services Involved:** Architecture Selection Tradeoffs  
**Cost Vector:** Avoid idle service baseline costs ($73/mo for EKS, $16/mo for ALB, $32/mo for NAT) when simpler designs suffice.  

---

## Problem
Engineers assume that because AWS offers a managed service (EKS, DynamoDB, Step Functions, CloudFront), it is automatically the right choice for every single project.

---

## Prediction
Evaluating concrete technical constraints reveals scenarios where simpler alternatives (EC2 over EKS, RDS over DynamoDB, direct code over Step Functions) are vastly superior.

---

## Why this matters
True cloud mastery is knowing when to say NO to an AWS service.

---

## First principles
Every managed service introduces a trade-off: abstractions hide complexity, but impose constraints, pricing cliffs, and vendor coupling. The right architecture is the simplest design that satisfies all measured requirements.

---

## Mental model
```text
When NOT to Use AWS Services Decision Matrix:
┌─────────────────┬─────────────────────────────────┬─────────────────────────────────┐
│ Service         │ When to USE                     │ When NOT to Use (Better Choice) │
├─────────────────┼─────────────────────────────────┼─────────────────────────────────┤
│ Amazon EKS      │ Multi-cloud K8s, complex CRDs   │ Standard web apps (Use ECS)     │
│ Amazon DynamoDB │ Single-digit ms key-value scale │ Complex JOINs/OLAP (Use RDS)    │
│ AWS Lambda      │ Event-driven, spiky APIs        │ 24/7 steady compute (Use ECS)   │
│ Amazon SQS      │ Point-to-point task buffering   │ Multi-subscriber pub/sub (SNS)  │
│ CloudFront      │ Global public web traffic       │ Internal private VPN apps (None)│
│ ElastiCache     │ Measured sub-ms DB read cache   │ Fast indexed database (Tune DB!)│
└─────────────────┴─────────────────────────────────┴─────────────────────────────────┘
```

---

## Architecture before AWS
Vendor sales representatives selling proprietary enterprise hardware appliances.

---

## Build the primitive
```python
# Service Selection Guardrail
def evaluate_service_need(service, requirement):
    if service == "DynamoDB" and "complex_joins" in requirement:
        return "REJECT DynamoDB: Relational JOINs required -> Choose Amazon RDS"
    if service == "EKS" and "small_team_simple_api" in requirement:
        return "REJECT EKS: High operational complexity -> Choose ECS Fargate"
    return "Service choice justified."
print(evaluate_service_need("DynamoDB", ["complex_joins"]))
print(evaluate_service_need("EKS", ["small_team_simple_api"]))
```

---

## Use AWS
```bash
# Service map matrix in docs/service-map.md
```

---

## Inspect it
```bash
cat docs/service-map.md
```

---

## Measure it
Compare operational overhead: maintaining 1 ECS service (2 hours/month) vs 1 EKS cluster (20 hours/month).

---

## Break it
Attempt to run an ad-hoc financial analytical SQL report across 15 DynamoDB tables.

---

## Diagnose it
Impossible without writing custom ETL pipelines to dump tables to S3 Athena; massive development delay.

---

## Recover it
Migrate relational data to Amazon RDS PostgreSQL.

---

## Security
Fewer services mean smaller attack surfaces: don't deploy services you don't need.

---

## Cost
### Cost Warning
Avoid idle service baseline costs ($73/mo for EKS, $16/mo for ALB, $32/mo for NAT) when simpler designs suffice.

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
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-80-evidence.md`.

---

## Questions for mastery
1. Why is Amazon RDS often a better choice than DynamoDB for early-stage startups with evolving queries?
2. Under what sustained request volume does an EC2/ECS cluster become significantly cheaper than AWS Lambda?
3. Why is adding a message queue (SQS) an over-engineering mistake if the client needs an immediate synchronous response?

---

## When to use this
Consult this decision framework during every design phase.

---

## When not to use this
Do not dismiss a managed service simply because you haven't learned it yet.

---

## What comes next
Phase 81: Build a Tiny Cloud Simulator — Capstone 1: Coding cloud primitives in Python.
