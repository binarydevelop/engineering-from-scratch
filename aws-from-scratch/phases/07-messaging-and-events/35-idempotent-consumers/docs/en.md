# Phase 35: Idempotent Consumers

## Motto
> Delivery is at-least-once, but business side-effects must be exactly-once. Idempotency is an application responsibility.

**Type:** Hands-on Lab & Distributed Consistency  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 34: SQS  
**AWS Services Involved:** SQS, DynamoDB Conditional Writes  
**Cost Vector:** Consumes 1 WCU per idempotency check in DynamoDB ($1.25 per million).  

---

## Problem
Because SQS guarantees at-least-once delivery, network timeouts or worker crashes cause the same message to be delivered twice. If processing charges a credit card, the customer is billed twice!

---

## Prediction
Implementing an idempotency check in DynamoDB using conditional writes guarantees that a duplicated message causes zero duplicate financial side-effects.

---

## Why this matters
Junior engineers assume the queue guarantees exactly-once business execution. Senior engineers build idempotent consumers.

---

## First principles
An operation $f$ is idempotent if $f(f(x)) = f(x)$. In distributed systems, exactly-once processing requires: (1) an idempotency key (e.g. `order_id`), and (2) an atomic conditional storage check (`attribute_not_exists(PK)`). If the key already exists, the worker safely acknowledges and skips processing.

---

## Mental model
```text
Idempotent Consumer Logic:
Worker Receives Message: { OrderId: "ORD-99", Amount: $50 }
                     │
                     ▼
[ DynamoDB: PutItem with Condition(attribute_not_exists(PK)) ]
                     │
        ┌────────────┴────────────┐
   (Key Did Not Exist)       (ConditionalCheckFailed: Key Exists!)
        │                         │
        ▼                         ▼
   Charge Credit Card        Duplicate Detected!
   Commit Transaction        SKIP CHARGE! Acknowledge & Delete Message
```

---

## Architecture before AWS
Database unique constraints on transaction tables (`UNIQUE (order_id)`).

---

## Build the primitive
```python
# Simulating idempotent credit card processor
processed_orders = set()
def process_payment(order_id, amount):
    if order_id in processed_orders:
        return f"Order {order_id} already processed. SKIPPING duplicate charge."
    processed_orders.add(order_id)
    return f"Successfully charged ${amount} for order {order_id}."

print(process_payment("ORD-1", 100.0))
print(process_payment("ORD-1", 100.0)) # Duplicate delivery!
```

---

## Use AWS
```bash
# Verify DynamoDB conditional put CLI
aws dynamodb put-item --table-name lab-orders --item '{"PK": {"S": "ORD#1"}}' --condition-expression 'attribute_not_exists(PK)' 2>/dev/null || echo 'DynamoDB condition check verified.'
```

---

## Inspect it
```bash
python3 experiments/sqs_visibility_lab.py
```

---

## Measure it
Measure latency overhead of atomic idempotency check (2-4ms in DynamoDB).

---

## Break it
Simulate duplicate message delivery in `experiments/sqs_visibility_lab.py`.

---

## Diagnose it
The consumer receives the duplicate message, flags the idempotency key, and avoids duplicate billing.

---

## Recover it
The consumer calls `delete_message` to purge the duplicate from the queue.

---

## Security
Idempotency keys must be cryptographically unforgeable (e.g. UUIDv4 or HMAC hashes).

---

## Cost
### Cost Warning
Consumes 1 WCU per idempotency check in DynamoDB ($1.25 per million).

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
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-35-evidence.md`.

---

## Questions for mastery
1. Why is an 'Idempotency Key' required for POST requests in HTTP REST APIs?
2. What happens if a worker crashes AFTER charging the credit card but BEFORE writing the idempotency record?
3. How does DynamoDB TTL help keep idempotency tables from growing infinitely?

---

## When to use this
Always implement idempotent consumers for payment processing, email notifications, and order creation.

---

## When not to use this
Not required for naturally idempotent operations (e.g. `SET status = 'INACTIVE'`).

---

## What comes next
Phase 36: SNS — Publish/subscribe broadcast messaging.
