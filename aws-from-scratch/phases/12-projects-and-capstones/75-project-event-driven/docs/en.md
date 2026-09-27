# Phase 75: Project: Event-Driven System

## Motto
> Decouple services through publish/subscribe fan-out. Protect workers with dead-letter queues and idempotency.

**Type:** Architecture Project & Asynchronous Cluster  
**Time Estimate:** ~90 minutes  
**Prerequisites:** Phase 37: SNS + SQS Fan-Out  
**AWS Services Involved:** SNS, SQS, Dead-Letter Queues, CloudWatch Alarms  
**Cost Vector:** Zero idle cost ($0.00). SQS and SNS charge only fractions of a cent per million requests.  

---

## Problem
Direct synchronous HTTP calls between microservices lead to cascading failures: if the Billing service has an outage, customers cannot checkout.

---

## Prediction
An SNS + SQS fan-out architecture allows the checkout API to acknowledge orders in 10ms, while Billing and Shipping consume messages independently.

---

## Why this matters
This is Project 04: the reference asynchronous decoupling architecture for distributed systems.

---

## First principles
SNS broadcasts events to independent SQS queues. Each queue buffers messages for its worker fleet. If a worker panics on a poison pill message, SQS redrives it to a Dead-Letter Queue after 3 failed attempts, alerting on-call engineers.

---

## Mental model
```text
Project 04 Architecture:
[ Checkout API ] ──► [ SNS Topic: order-created ]
                               │
            ┌──────────────────┴──────────────────┐
            ▼                                     ▼
    [ SQS: billing-queue ]                [ SQS: shipping-queue ]
    ├── DLQ: billing-dlq                  ├── DLQ: shipping-dlq
    ▼                                     ▼
[ Billing Workers ]                   [ Shipping Workers ]
```

---

## Architecture before AWS
RabbitMQ clusters with shovel plugins or custom Celery Redis workers.

---

## Build the primitive
```python
with open('projects/project-04-event-driven/README.md') as f:
    print("Project 04 loaded:", "SNS + SQS + DLQ" in f.read())
```

---

## Use AWS
```bash
# Implementation commands in projects/project-04-event-driven/README.md
```

---

## Inspect it
```bash
aws sqs get-queue-attributes --queue-url $BILLING_Q --attribute-names ApproximateNumberOfMessages --output table
```

---

## Measure it
Measure producer latency: publishing to SNS takes ~12ms regardless of how slow downstream consumers are.

---

## Break it
Send a corrupted poison pill message into the queue.

---

## Diagnose it
The worker crashes 3 times; SQS detects `maxReceiveCount=3` and evicts the message to the DLQ.

---

## Recover it
The CloudWatch DLQ alarm alerts the engineer; the bug is fixed and the message redriven.

---

## Security
SQS queue policies restrict send permissions strictly to the authorized SNS topic ARN.

---

## Cost
### Cost Warning
Zero idle cost ($0.00). SQS and SNS charge only fractions of a cent per million requests.

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
Follow cleanup commands in `projects/project-04-event-driven/README.md`.
```

---

## Verify cleanup
```bash
./scripts/cleanup-check.sh
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-75-evidence.md`.

---

## Questions for mastery
1. Why is an SQS Dead-Letter Queue essential for preventing head-of-line blocking in queue workers?
2. What happens if a worker crashes before calling `DeleteMessage` in SQS?
3. How does SNS + SQS fan-out prevent the Shipping service outage from affecting Billing?

---

## When to use this
Use for all asynchronous business events (OrderPlaced, UserRegistered, InvoiceGenerated).

---

## When not to use this
Do not use if the caller requires an immediate synchronous response (e.g. credit card CVV check).

---

## What comes next
Phase 76: Project: Containerized Production Application — ECS Fargate and managed databases.
