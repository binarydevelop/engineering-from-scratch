# Project 03: Production Serverless API (API Gateway + Lambda + DynamoDB)

> **Motto:** Pay strictly for executed milliseconds and written items. Scale from 0 to 10,000 requests/sec with zero idle servers.

---

## 1. Architectural Diagram

```text
[ Client / Browser ]
        │
        │ 1. HTTPS POST /orders (Payload: JSON with Idempotency-Key)
        ▼
[ Amazon API Gateway (HTTP API v2) ]
        │ 2. Request validation, throttling, and direct Lambda proxy integration
        ▼
[ AWS Lambda (orders-handler) ]
  (Memory: 256MB | Runtime: Python 3.12 | IAM Execution Role)
        │
        ├── 3. Idempotency Check (Check DynamoDB table for existing key)
        ├── 4. Business Logic & Input Validation
        └── 5. PutItem with Conditional Expression
        ▼
[ Amazon DynamoDB (orders-table) ]
  (BillingMode: PAY_PER_REQUEST | PartitionKey: PK | SortKey: SK)
        │
        └── CloudWatch Logs (Structured JSON logs with correlation IDs)
```

---

## 2. Serverless vs Traditional VM/Container Architecture

| Dimension | Serverless (API Gateway + Lambda + DynamoDB) | Traditional (ALB + ECS Fargate + RDS) |
|:---|:---|:---|
| **Idle Cost** | **$0.00 / month** (True zero when idle) | ~$45 - $60 / month baseline running cost |
| **Scaling Mechanism** | Instant horizontal concurrency (0 to 1,000 workers in seconds) | Provisioning new container tasks (30s - 2min) |
| **Operational Burden** | Zero OS or container runtime patching; zero connection pool tuning | Manage VPC subnets, task definitions, DB connection pooling |
| **Latency Profile** | Variable (cold starts 100-500ms; warm calls 5-15ms) | Consistent (sub-5ms predictable p99) |
| **Connection Limits** | Ephemeral functions can overwhelm traditional databases | Long-lived connection pools match DB limits |
| **Execution Duration** | Hard ceiling: Max 15 minutes per invocation | Unlimited execution duration |

---

## 3. The Idempotency Layer

Because network timeouts can occur **after** a write succeeds, clients retry POST requests. Without an idempotency layer, a retried request causes duplicate charges or duplicate order fulfillment.

```python
# Serverless Idempotent Handler Pattern
def handle_create_order(event):
    idempotency_key = event['headers'].get('idempotency-key')
    order_data = json.loads(event['body'])
    
    # Conditional Put: Only succeeds if PK does not already exist
    try:
        table.put_item(
            Item={
                'PK': f"IDEMPOTENCY#{idempotency_key}",
                'SK': 'LOCK',
                'Status': 'PROCESSING',
                'TTL': int(time.time()) + 86400  # Expires in 24 hours
            },
            ConditionExpression='attribute_not_exists(PK)'
        )
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            # Request is a duplicate! Return cached or idempotent response
            return {'statusCode': 409, 'body': json.dumps({'error': 'Duplicate request in flight'})}
        raise
```

---

## 4. Well-Architected Review

### Performance Efficiency
- **Memory Allocation Tuning:** Lambda CPU scales proportionally with allocated memory. Increasing memory from 128MB to 512MB often reduces execution time by 4x, resulting in lower total cost and faster response times.
- **Warm Invocation Optimization:** Initialize database connections, AWS SDK clients, and configuration outside the handler function to reuse across warm invocations.

### Cost Optimization
- **API Gateway HTTP APIs (v2):** Costs $1.00 per million requests (over 70% cheaper than legacy REST APIs at $3.50/million).
- **Lambda:** First 1,000,000 invocations and 3,200,000 seconds of compute time per month are free.
- **DynamoDB On-Demand:** $1.25 per million write request units; $0.25 per million read request units.

---

## 5. Cleanup & Verification

```bash
# Delete CloudFormation stack
aws cloudformation delete-stack --stack-name aws-from-scratch-serverless-api

# Wait for deletion
aws cloudformation wait stack-delete-complete --stack-name aws-from-scratch-serverless-api
```

### Verify Cleanup
```bash
./scripts/cleanup-check.sh
```
