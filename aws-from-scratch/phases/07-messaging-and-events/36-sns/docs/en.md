# Phase 36: SNS

## Motto
> SQS is point-to-point (one consumer processes each message). SNS is pub/sub (every subscriber gets a copy).

**Type:** Hands-on Lab & Publish/Subscribe  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 34: SQS  
**AWS Services Involved:** Amazon Simple Notification Service (SNS)  
**Cost Vector:** First 1,000,000 Amazon SNS requests/month are free; $0.50 per million thereafter.  

---

## Problem
When an order is placed, 4 different systems need the event (Billing, Shipping, Analytics, Fraud). Writing code that calls each system sequentially creates tight coupling and fragility.

---

## Prediction
Publishing an event to an SNS topic will push an identical copy of the message to all registered subscribers simultaneously.

---

## Why this matters
SNS is the primary publish/subscribe primitive in AWS for 1-to-many fan-out architecture.

---

## First principles
Publish/Subscribe (Pub/Sub) decouples the publisher from subscribers. The publisher pushes a message to a Topic without knowing who is subscribed. SNS immediately fans out the message to heterogeneous subscriber protocols (SQS, Lambda, HTTP webhooks, SMS, Email).

---

## Mental model
```text
SNS Publish/Subscribe Fan-Out:
                  [ Order Placement API ]
                             │
                             ▼ Publish("OrderPlaced")
                  [ Amazon SNS Topic: orders ]
                             │
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
[ SQS: Billing ]     [ SQS: Shipping ]    [ Lambda: Analytics ]
```

---

## Architecture before AWS
Enterprise Service Buses (ESB) like TIBCO, ActiveMQ Virtual Topics, or Kafka broadcast topics.

---

## Build the primitive
```python
# Simulating Pub/Sub Topic
subscribers = []
def subscribe(fn): subscribers.append(fn)
def publish(event):
    for sub in subscribers: sub(event)
subscribe(lambda e: print("Billing received:", e))
subscribe(lambda e: print("Shipping received:", e))
publish({"order_id": "ORD-123"})
```

---

## Use AWS
```bash
aws sns create-topic --name lab-order-events --tags Key=Project,Value=aws-from-scratch
```

---

## Inspect it
```bash
aws sns list-topics --output table
```

---

## Measure it
Measure fan-out latency: SNS dispatches to 100 subscribers in parallel within 50ms.

---

## Break it
Publish a message to an SNS topic that has an unreachable HTTP webhook subscriber.

---

## Diagnose it
SNS delivery retries fail; unbuffered messages are dropped unless an SNS delivery DLQ is configured.

---

## Recover it
Always subscribe SQS queues to SNS topics instead of raw HTTP endpoints to ensure durable buffering.

---

## Security
Use SNS topic policies to restrict which AWS accounts or IAM principals can publish to the topic.

---

## Cost
### Cost Warning
First 1,000,000 Amazon SNS requests/month are free; $0.50 per million thereafter.

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
aws sns delete-topic --topic-arn $TOPIC_ARN
```

---

## Verify cleanup
```bash
echo 'SNS topic deleted.'
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-36-evidence.md`.

---

## Questions for mastery
1. Why does SNS push messages immediately rather than buffering them like SQS?
2. What happens if an SNS subscriber is offline when a message is published?
3. How does SNS Message Filtering prevent subscribers from receiving events they don't care about?

---

## When to use this
Use SNS for 1-to-many broadcast events where multiple independent microservices must react to the same trigger.

---

## When not to use this
Do not use SNS standalone if subscribers need message persistence, queue buffering, or rate-limited consumption.

---

## What comes next
Phase 37: SNS + SQS Fan-Out — Combining pub/sub broadcast with durable queue buffering.
