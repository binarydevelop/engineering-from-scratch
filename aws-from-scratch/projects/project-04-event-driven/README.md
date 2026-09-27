# Project 04: Resilient Event-Driven Fan-Out (SNS + SQS + DLQ)

> **Motto:** Decouple producers from consumers. Never let a slow billing service or shipping outage block customer order placement.

---

## 1. Architectural Diagram

```text
                           [ Order Placement API ]
                                     │
                                     │ 1. Publish Event: OrderPlaced
                                     ▼
                      [ Amazon SNS Topic: order-events ]
                                     │
             ┌───────────────────────┴───────────────────────┐
             │ (Fan-out Subscription)                        │ (Fan-out Subscription)
             ▼                                               ▼
 [ SQS: billing-service-queue ]                 [ SQS: shipping-service-queue ]
 (VisibilityTimeout: 30s)                       (VisibilityTimeout: 30s)
             │                                               │
             ├── Redrive on 3rd failure                      ├── Redrive on 3rd failure
             ▼                                               ▼
 [ SQS DLQ: billing-dlq ]                       [ SQS DLQ: shipping-dlq ]
             │                                               │
             ▼                                               ▼
 [ Billing Worker Cluster ]                     [ Shipping Worker Cluster ]
 (Pulls messages at its own pace)               (Pulls messages at its own pace)
```

---

## 2. Why Fan-Out Solves the Synchronous Antipattern

If the Order API synchronously invokes the Billing API and Shipping API via direct HTTP:
1. **Cascading Failure:** If Shipping is experiencing downtime, the entire customer checkout fails.
2. **Latency Accumulation:** Total response time = Latency(Billing) + Latency(Shipping) + Network round-trips.
3. **No Retries or Backpressure:** If traffic spikes by 10x, downstream databases crash from connection exhaustion.

**With SNS + SQS Fan-Out:**
- The Order API publishes **one event** to SNS in ~10 milliseconds and returns HTTP 201 Created to the user immediately.
- SNS immediately duplicates the message into the independent SQS queues.
- Billing workers and Shipping workers consume messages at their own sustainable rate. If Shipping is down for 3 hours of maintenance, messages accumulate safely in the queue and are processed when Shipping comes back online.

---

## 3. Systems Failure Mechanics & Dead-Letter Queues

```text
Message Ingestion ──► Worker Receives ──► Worker Panics (Uncaught Exception)
                                                 │
                                                 ▼
      Message Reappears in Queue ◄── Visibility Timeout Expires
                                                 │
                   (Repeat maxReceiveCount times: e.g. 3)
                                                 │
                                                 ▼
               Evicted to Dead-Letter Queue (DLQ)
                                                 │
                                                 ▼
            CloudWatch Alarm Alerts On-Call Engineer:
            "DLQ Depth > 0 (Poison Message Detected)"
```

---

## 4. Well-Architected Review

### Reliability
- **At-Least-Once Delivery Handling:** Consumers must implement an idempotency cache to prevent double-charging credit cards if a message reappears after a worker timeout.
- **DLQ Redrive:** SQS supports DLQ redrive directly via the AWS CLI or Console to replay resolved poison pill messages back into the primary queue once the application bug is patched.

### Cost Optimization
- SQS Standard: First 1,000,000 requests/month are free; $0.40 per million requests thereafter.
- SQS Long Polling: Setting `ReceiveMessageWaitTimeSeconds = 20` reduces empty receives by up to 90%, dramatically decreasing API request costs.
- Zero idle costs: When no orders are placed, the messaging infrastructure costs **$0.00**.

---

## 5. Teardown & Cleanup

```bash
# Delete SQS Queues
aws sqs delete-queue --queue-url "$BILLING_QUEUE_URL"
aws sqs delete-queue --queue-url "$BILLING_DLQ_URL"
aws sqs delete-queue --queue-url "$SHIPPING_QUEUE_URL"
aws sqs delete-queue --queue-url "$SHIPPING_DLQ_URL"

# Delete SNS Topic
aws sns delete-topic --topic-arn "$SNS_TOPIC_ARN"
```

### Verify Cleanup
```bash
./scripts/cleanup-check.sh
```
