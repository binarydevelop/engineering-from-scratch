# Phase 38: EventBridge

## Motto
> EventBridge is an intelligent event bus. It inspects JSON payloads and routes events based on declarative rule patterns.

**Type:** Hands-on Lab & Event Bus Routing  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 37: SNS + SQS Fan-Out  
**AWS Services Involved:** Amazon EventBridge (Event Bus, Rules, Targets)  
**Cost Vector:** Custom event bus ingestion: $1.00 per million events. Events delivered by native AWS services are free.  

---

## Problem
SNS topics route messages blindly based on topic subscriptions. If a service only wants orders where `total > $1,000` or `country == 'CA'`, writing custom routing microservices adds code maintenance.

---

## Prediction
EventBridge rules inspect the JSON body of an event and route it to specific targets (Lambda, SQS, Step Functions) only if declarative pattern conditions match.

---

## Why this matters
EventBridge is the modern enterprise event spine for AWS, integrating third-party SaaS (Stripe, GitHub, Datadog) with AWS services.

---

## First principles
Amazon EventBridge is a serverless content-based event bus. Publishers send CloudEvents-formatted JSON events. EventBridge evaluates JSON pattern matching rules (`prefix`, `numeric range`, `anything-but`) and routes matching events to up to 5 targets per rule with automatic payload transformation.

---

## Mental model
```text
EventBridge Content-Based Routing:
[ Order Service ] ──► PutEvents({ "detail": { "total": 1250, "country": "US" } })
                                │
                                ▼
                   [ EventBridge Custom Bus ]
                                │
        ┌───────────────────────┴───────────────────────┐
        │ Rule: detail.total > 1000                     │ Rule: detail.country == "CA"
        ▼                                               ▼
[ SQS: VIP-Orders-Queue ]                       [ SQS: Canada-Orders-Queue ]
```

---

## Architecture before AWS
Enterprise Service Bus (ESB) routing engines running XML / XPath queries or Apache Camel.

---

## Build the primitive
```python
# Simulating EventBridge JSON rule matching
event = {"source": "ecommerce.orders", "detail": {"total": 1500, "status": "CONFIRMED"}}
rule = {"source": ["ecommerce.orders"], "detail.total": lambda x: x > 1000}
is_match = (event["source"] in rule["source"]) and rule["detail.total"](event["detail"]["total"])
print("Event matched VIP rule:", is_match)
```

---

## Use AWS
```bash
aws events create-event-bus --name lab-event-bus --tags Key=Project,Value=aws-from-scratch
```

---

## Inspect it
```bash
aws events list-event-buses --output table
```

---

## Measure it
Measure routing latency: EventBridge evaluates rules and invokes targets typically in 20-40ms.

---

## Break it
Send an event with a malformed JSON envelope missing `Source` or `DetailType`.

---

## Diagnose it
EventBridge rejects the API call with `InvalidEventPatternException`.

---

## Recover it
Ensure events follow the standard AWS EventBridge event envelope format.

---

## Security
Use EventBridge schema discovery to prevent payload schema drift between microservice teams.

---

## Cost
### Cost Warning
Custom event bus ingestion: $1.00 per million events. Events delivered by native AWS services are free.

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
aws events delete-event-bus --name lab-event-bus
```

---

## Verify cleanup
```bash
echo 'Event bus deleted.'
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-38-evidence.md`.

---

## Questions for mastery
1. What is the architectural difference between Amazon SNS and Amazon EventBridge?
2. Why is EventBridge preferred over SNS for complex microservice domain events?
3. How does EventBridge Archive and Replay help recover from production consumer bugs?

---

## When to use this
Use EventBridge for enterprise event-driven architectures, SaaS integrations, and content-based routing.

---

## When not to use this
Do not use EventBridge for high-throughput streaming (millions of records/sec; use Amazon Kinesis instead).

---

## What comes next
Phase 39: Lambda From First Principles — Event-driven serverless compute.
