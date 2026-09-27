# Project 08: Production-Grade Resilient Architecture (Capstone 2)

> **Motto:** The complete synthesis: Every component justified. Every byte traced. Every failure accounted for. Every dollar modeled.

---

## 1. The Production Architecture Diagram

```text
                                [ Global Users ]
                                        │
                                        │ 1. HTTPS / Route 53 Anycast DNS
                                        ▼
                         [ Amazon CloudFront CDN ]
                         (Edge Caching & TLS Termination)
                                        │
               ┌────────────────────────┴────────────────────────┐
               │ Static Web Assets (/static/*)                   │ Dynamic APIs (/api/*)
               ▼                                                 ▼
     [ Private S3 Bucket ]                     [ Application Load Balancer (Public Multi-AZ) ]
     (OAC Authenticated)                                         │
                                       ┌─────────────────────────┴─────────────────────────┐
                                       ▼                                                   ▼
                           [ Availability Zone A ]                             [ Availability Zone B ]
                           ┌─────────────────────────────┐                     ┌─────────────────────────────┐
                           │ Private App Subnet A        │                     │ Private App Subnet B        │
                           │ ┌─────────────────────────┐ │                     │ ┌─────────────────────────┐ │
                           │ │ ECS Fargate Container   │ │                     │ │ ECS Fargate Container   │ │
                           │ └───────────┬─────────────┘ │                     │ └───────────┬─────────────┘ │
                           └─────────────┼───────────────┘                     └─────────────┼───────────────┘
                                         │                                                   │
                                         └─────────────────────────┬─────────────────────────┘
                                                                   │
                                 ┌─────────────────────────────────┼─────────────────────────────────┐
                                 │ Relational State                │ Async Decoupling                │ Object State
                                 ▼                                 ▼                                 ▼
                     [ Amazon RDS PostgreSQL ]          [ Amazon SQS Queue ]             [ Private S3 Bucket ]
                     (Multi-AZ Sync Standby)           (Orders + DLQ Buffer)            (Customer Documents)
                                 │                                 │                                 │
                                 └─────────────────────────────────┼─────────────────────────────────┘
                                                                   ▼
                                             [ Observability & Security Control Plane ]
                                             • CloudWatch Metrics, Alarms & Logs
                                             • AWS Secrets Manager & KMS Customer Master Key
                                             • Least-Privilege IAM Task Roles
```

---

## 2. Complete End-to-End Data Flow

1. **User Request:** User navigates to `https://app.example.com/checkout`.
2. **Edge Inspection:** CloudFront serves static HTML/JS bundles directly from edge memory cache in 15ms.
3. **API Routing:** CloudFront routes `/api/v1/orders` dynamically across the private AWS backbone to the Application Load Balancer.
4. **Load Balancer Layer:** ALB terminates TLS, verifies HTTP headers, checks target health, and forwards HTTP POST to a healthy ECS container task in AZ-A over TCP port 8080.
5. **Compute & Secrets:** The containerized application retrieves encrypted database credentials from AWS Secrets Manager using its IAM Task Role (zero hardcoded passwords).
6. **Transactional Write:** Container connects to PostgreSQL Multi-AZ primary instance, executes ACID order insertion, and the write-ahead log (WAL) synchronously replicates to the AZ-B standby.
7. **Asynchronous Hand-off:** Container publishes an `OrderCreated` notification message to SQS within 5ms and returns HTTP 201 Created to the browser.
8. **Background Processing:** Background worker pulls the SQS message, generates an invoice PDF, encrypts it via KMS envelope encryption, and writes it to an S3 bucket with Object Lock and versioning enabled.
9. **Telemetry:** Structured JSON logs stream to CloudWatch Logs with p95/p99 latency metrics emitted to CloudWatch Metrics.

---

## 3. Failure Mode & Disaster Recovery Matrix

| Component | Failure Injected | Blast Radius | Recovery Mechanism | Measured RTO / RPO |
|:---|:---|:---|:---|:---|
| **AZ-A Data Center** | Total power failure / fiber cut | 50% of compute instances die; primary DB goes offline | ALB removes AZ-A targets; RDS triggers automatic DNS failover to AZ-B standby; ASG scales up AZ-B tasks | RTO: 60-90s<br>RPO: 0 (Zero data loss) |
| **ECS Task Process** | Application out-of-memory (OOM) | 1 container instance crashes | ALB health check evicts task; ECS task supervisor launches replacement | RTO: 15s<br>RPO: N/A (Stateless) |
| **Database Network** | Transient network blip to RDS | In-flight DB queries fail with connection reset | Application retries with exponential backoff and jitter | RTO: 2s<br>RPO: 0 |
| **Worker Failure** | Worker crashes while processing invoice | Message unacknowledged in SQS | SQS Visibility Timeout expires; message reappears; secondary worker completes task | RTO: 30s<br>RPO: 0 |
| **Poison Message** | Corrupted payload crashes all workers | Worker crash loop | SQS maxReceiveCount triggers eviction to Dead-Letter Queue (DLQ) | RTO: Instant eviction<br>Alerts on-call engineer |

---

## 4. Comprehensive Well-Architected Review

### 1. Operational Excellence
- Infrastructure completely defined as code via CloudFormation / Terraform.
- Deployment via blue/green rolling deployments with automated rollback on CloudWatch error metric alarms.
- Centralized structured JSON logging with distributed request correlation IDs (`x-correlation-id`).

### 2. Security
- Zero public database or application subnets; only the ALB is exposed to the internet.
- Strict least-privilege IAM Task Roles; no permanent credentials stored on instances or containers.
- Encryption in transit (TLS 1.3 enforced) and encryption at rest (KMS Customer Managed Keys with automatic rotation).

### 3. Reliability
- Fully redundant across 2 Availability Zones at every tier (ALB, ECS, RDS, S3, SQS).
- Automated health check eviction and dynamic capacity autoscaling.
- Automated daily RDS backups with 35-day Point-in-Time Recovery (PITR).

### 4. Performance Efficiency
- Static assets offloaded to CloudFront edge (95%+ cache hit ratio reduces origin load).
- ECS Fargate tasks right-sized based on measured CPU/memory percentiles.
- SQS buffers traffic surges, preventing database saturation during peak events.

### 5. Cost Optimization
- Pay-as-you-go serverless primitives utilized wherever applicable.
- S3 lifecycle policies transition cold documents from Standard to Standard-IA after 30 days, then to Glacier Flexible Retrieval after 90 days.
- NAT Gateways replaced by Gateway VPC Endpoints for S3, eliminating data processing charges.

### 6. Sustainability
- ARM64 Graviton instances utilized for RDS and ECS compute, delivering up to 40% better price-performance and 60% lower carbon footprint than comparable x86 instances.
- Automatic scaling scales down idle tasks during off-peak hours.

---

## 5. Cost Model & Teardown Protocol

### Estimated Running Cost Breakdown:
- CloudFront: Free Tier eligible (< 1TB)
- ALB: ~$0.0225/hr (~$16.20/mo)
- ECS Fargate (2 tasks @ 0.25 vCPU, 0.5 GB RAM): ~$0.024/hr (~$17.50/mo)
- Amazon RDS PostgreSQL (`db.t4g.micro` Multi-AZ): ~$0.036/hr (~$26.00/mo)
- S3 & SQS: Pay-per-use (< $1.00/mo)
- **Total Estimated Cost for Running Lab:** ~$0.08 / hour (~$2.00 for a 24-hour test lab).

### Teardown Commands
```bash
# 1. Delete ECS Service and Cluster
aws ecs update-service --cluster capstone-cluster --service web-service --desired-count 0
aws ecs delete-service --cluster capstone-cluster --service web-service
aws ecs delete-cluster --cluster capstone-cluster

# 2. Delete ALB & Target Group
aws elbv2 delete-load-balancer --load-balancer-arn "$ALB_ARN"
aws elbv2 delete-target-group --target-group-arn "$TG_ARN"

# 3. Delete RDS Multi-AZ Database
aws rds delete-db-instance --db-instance-identifier capstone-db --skip-final-snapshot

# 4. Delete SQS Queues & S3 Buckets
aws sqs delete-queue --queue-url "$CAPSTONE_QUEUE_URL"
aws s3 rm "s3://$CAPSTONE_BUCKET" --recursive
aws s3api delete-bucket --bucket "$CAPSTONE_BUCKET"
```

### Verify Teardown
```bash
./scripts/cleanup-check.sh
```
