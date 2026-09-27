# Phase 34: SQS

## Motto
> Delivery is at-least-once. If a consumer crashes before DeleteMessage, the visibility timeout brings it back.

**Type:** Hands-on Lab & Queue Mechanics  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 33: Queues Before SQS  
**AWS Services Involved:** Amazon SQS, Dead-Letter Queues (DLQ)  
**Cost Vector:** First 1,000,000 SQS requests/month are free; $0.40 per million thereafter. Long polling cuts empty receive costs by 90%.  

---

## Problem
Messages sent to a single server queue are lost if that server crashes. Distributed queues must guarantee durability and survivability.

---

## Prediction
When a worker receives a message, SQS hides it for the Visibility Timeout duration. If the worker crashes before calling `DeleteMessage`, the message becomes visible again.

---

## Why this matters
This visibility timeout mechanism is the cornerstone of at-least-once distributed processing.

---

## First principles
Amazon SQS is a distributed pull-based queue. Ingested messages are replicated across multiple availability zones. When a consumer issues `ReceiveMessage`, SQS marks the message invisible to other consumers for the `VisibilityTimeout`. If `DeleteMessage` is called, it is purged; if the timer expires, it reappears.

---

## Mental model
```text
SQS Visibility Timeout Lifecycle:
[ Producer ] ──► SendMessage("ORD-1") ──► [ SQS Durable Queue ]
                                                  │
                                                  ▼ Consumer Calls ReceiveMessage()
┌────────────────────────────────────────────────────────┐
│ Message Hidden for 30s (Visibility Timeout Ticking)   │
└──────────────────────────┬─────────────────────────────┘
                           │
             ┌─────────────┴─────────────┐
             ▼ (Worker Succeeds)         ▼ (Worker Crashes!)
     [ DeleteMessage() ]        [ 30s Timer Expires! ]
     Message Permanently         Message Reappears in Queue!
     Purged from Queue           Available for Worker 2
```

---

## Architecture before AWS
ActiveMQ / RabbitMQ clusters with disk-backed persistence and manual broker clustering.

---

## Build the primitive
```python
# Run our complete SQS visibility and DLQ lab
import subprocess
subprocess.run(['python3', 'experiments/sqs_visibility_lab.py'], check=True)
```

---

## Use AWS
```bash
aws sqs create-queue --queue-name lab-orders-queue --attributes VisibilityTimeout=30 --tags Project=aws-from-scratch
```

---

## Inspect it
```bash
aws sqs get-queue-attributes --queue-url $QUEUE_URL --attribute-names All --output json
```

---

## Measure it
Measure SQS Long Polling (`WaitTimeSeconds=20`) vs Short Polling API cost reduction.

---

## Break it
Send a poison pill message that crashes the consumer JSON parser on every receipt.

---

## Diagnose it
The message oscillates in visibility forever, driving CPU to 100% and blocking queue throughput.

---

## Recover it
Configure a Dead-Letter Queue (DLQ) with `maxReceiveCount=3` to isolate poison messages.

---

## Security
Use SQS SSE-KMS encryption to encrypt sensitive message bodies at rest.

---

## Cost
### Cost Warning
First 1,000,000 SQS requests/month are free; $0.40 per million thereafter. Long polling cuts empty receive costs by 90%.

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
aws sqs delete-queue --queue-url $QUEUE_URL
```

---

## Verify cleanup
```bash
echo 'SQS queue deleted.'
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-34-evidence.md`.

---

## Questions for mastery
1. Why does standard SQS guarantee at-least-once delivery rather than exactly-once delivery?
2. What is the difference between SQS Standard and SQS FIFO queues?
3. What happens if a worker takes 35 seconds to process a job, but the Visibility Timeout is set to 30 seconds?

---

## When to use this
Use SQS for decoupled point-to-point task queues and background worker buffering.

---

## When not to use this
Do not use SQS if you need pub/sub broadcast to multiple independent subscribers (use SNS).

---

## What comes next
Phase 35: Idempotent Consumers — Solving duplicate delivery in distributed systems.
