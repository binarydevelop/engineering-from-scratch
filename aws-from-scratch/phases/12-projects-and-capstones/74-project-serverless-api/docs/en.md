# Phase 74: Project: Serverless API

## Motto
> True scale-to-zero: Pay strictly for executed milliseconds and written items. Zero servers to manage.

**Type:** Architecture Project & Serverless System  
**Time Estimate:** ~90 minutes  
**Prerequisites:** Phase 41: API Gateway + Lambda  
**AWS Services Involved:** API Gateway, Lambda, DynamoDB, CloudWatch  
**Cost Vector:** Exactly $0.00/month while idle. 100% covered by AWS Free Tier for low to medium learning traffic.  

---

## Problem
Traditional VM architectures burn $50+/month even with zero users. Building a modern startup API requires true utility pricing and instant elasticity.

---

## Prediction
Deploying API Gateway + Lambda + DynamoDB On-Demand handles 0 to 10,000 requests/sec with zero capacity planning and zero idle monthly cost.

---

## Why this matters
This is Project 03: the definitive serverless transactional API architecture.

---

## First principles
API Gateway receives HTTP POST, verifies rate limits, and invokes Lambda. Lambda verifies idempotency in DynamoDB, executes business logic, writes with conditional expressions, and returns JSON. Every component scales automatically.

---

## Mental model
```text
Project 03 Architecture:
[ Client ] ──► [ API Gateway HTTP API ] ──► [ Lambda (orders-handler) ]
                                                    │
                                                    ├── 1. Idempotency Check
                                                    └── 2. PutItem (Condition: attribute_not_exists)
                                                    ▼
                                            [ DynamoDB (On-Demand) ]
```

---

## Architecture before AWS
Provisioning VPS servers running Flask/Django with SQLite or MySQL.

---

## Build the primitive
```python
with open('projects/project-03-serverless-api/README.md') as f:
    print("Project 03 loaded:", "API Gateway + Lambda + DynamoDB" in f.read())
```

---

## Use AWS
```bash
# Deploy via infrastructure/serverless-api.yaml template
```

---

## Inspect it
```bash
aws cloudformation describe-stacks --stack-name aws-from-scratch-serverless --output table
```

---

## Measure it
Measure latency: p50 warm execution takes ~8ms; cold start takes ~220ms.

---

## Break it
Send duplicate POST requests with the same `Idempotency-Key` header.

---

## Diagnose it
The handler intercepts the duplicate, avoids a duplicate database write, and returns HTTP 409/200 cached.

---

## Recover it
The client receives confirmation without double-billing.

---

## Security
Enforce strict IAM execution role policies: Lambda can only access its specific DynamoDB table.

---

## Cost
### Cost Warning
Exactly $0.00/month while idle. 100% covered by AWS Free Tier for low to medium learning traffic.

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
aws cloudformation delete-stack --stack-name aws-from-scratch-serverless
```

---

## Verify cleanup
```bash
./scripts/cleanup-check.sh
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-74-evidence.md`.

---

## Questions for mastery
1. Why is an idempotency layer mandatory when building serverless POST APIs?
2. What are the tradeoffs of API Gateway + Lambda vs ALB + EC2 in terms of cost at 100M requests/month?
3. How does DynamoDB On-Demand pricing differ from Provisioned Capacity?

---

## When to use this
Use for web APIs, webhooks, mobile backends, and event-driven microservices.

---

## When not to use this
Do not use for long-running batch jobs (> 15 mins) or websocket gaming servers with persistent memory state.

---

## What comes next
Phase 75: Project: Event-Driven System — Decoupled asynchronous messaging.
