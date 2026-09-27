# Phase 37: SNS + SQS Fan-Out

## Motto
> Combine SNS broadcast with SQS buffering. Each subscriber gets its own independent queue.

**Type:** Architecture Project & Messaging Cluster  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 36: SNS  
**AWS Services Involved:** SNS Topics, SQS Subscriptions, Fan-Out Pattern  
**Cost Vector:** SNS publish ($0.50/M) + SQS delivery ($0.40/M) = less than $1.00 per million fan-out operations.  

---

## Problem
Subscribing HTTP endpoints directly to SNS causes message loss if an endpoint is temporarily down. Subscribing a single SQS queue causes competing consumers to steal messages from each other.

---

## Prediction
Subscribing two independent SQS queues to one SNS topic ensures BOTH Billing and Shipping receive every single message and process them at their own pace.

---

## Why this matters
This is Project 04 in the curriculum and one of the most powerful architectural patterns in cloud computing.

---

## First principles
The Fan-Out pattern combines the 1-to-many broadcast capability of SNS with the durable persistence and rate-controlled buffering of SQS. SNS acts as the router; SQS queues act as independent storage mailboxes for each service.

---

## Mental model
```text
SNS + SQS Fan-Out Architecture:
[ Publisher API ] ──► [ SNS Topic: order-created ]
                               │
            ┌──────────────────┴──────────────────┐
            ▼ (Topic Subscription)                ▼ (Topic Subscription)
    [ SQS: billing-queue ]                [ SQS: shipping-queue ]
            │                                     │
            ▼                                     ▼
    [ Billing Workers ]                   [ Shipping Workers ]
    (Processes in 10ms)                   (Processes in 500ms)
```

---

## Architecture before AWS
Configuring RabbitMQ exchange-to-queue bindings (Fanout Exchange).

---

## Build the primitive
```python
# Simulating SNS-to-SQS fan-out
billing_q = []
shipping_q = []
def sns_fanout(event):
    billing_q.append(event)
    shipping_q.append(event)
sns_fanout({"order": "ORD-55", "total": 120})
print("Billing Queue items:", len(billing_q))
print("Shipping Queue items:", len(shipping_q))
```

---

## Use AWS
```bash
aws sns subscribe --topic-arn $TOPIC_ARN --protocol sqs --notification-endpoint $QUEUE_ARN
```

---

## Inspect it
```bash
aws sns list-subscriptions-by-topic --topic-arn $TOPIC_ARN --output table
```

---

## Measure it
Verify independent processing: simulate a 1-hour Shipping outage; verify Billing processes 100% of orders with zero delay.

---

## Break it
Forget to add the SQS Queue Policy granting `sns.amazonaws.com` permission to call `sqs:SendMessage`.

---

## Diagnose it
SNS publish succeeds, but SQS queue depth remains 0! SNS silently fails to deliver to SQS.

---

## Recover it
Attach a resource policy to the SQS queue allowing `sqs:SendMessage` from the SNS topic ARN.

---

## Security
Enforce principle of least privilege in SQS resource policies: allow only the specific SNS topic ARN.

---

## Cost
### Cost Warning
SNS publish ($0.50/M) + SQS delivery ($0.40/M) = less than $1.00 per million fan-out operations.

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
aws sns delete-topic --topic-arn $TOPIC_ARN && aws sqs delete-queue --queue-url $Q1 && aws sqs delete-queue --queue-url $Q2
```

---

## Verify cleanup
```bash
./scripts/cleanup-check.sh
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-37-evidence.md`.

---

## Questions for mastery
1. Why is an SQS Queue Policy required when subscribing an SQS queue to an SNS topic?
2. What happens if one of the subscriber queues fills up with 100,000 messages while the other queue is empty?
3. How does SNS Dead-Letter Queue (DLQ) differ from an SQS Dead-Letter Queue?

---

## When to use this
Use SNS + SQS Fan-Out for all asynchronous microservice event distribution.

---

## When not to use this
Do not use fan-out if only a single worker service consumes the messages (use direct SQS instead).

---

## What comes next
Phase 38: EventBridge — Declarative content-based event routing.
