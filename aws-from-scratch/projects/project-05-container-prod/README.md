# Project 05: Containerized Production Application (ECS Fargate + ALB + RDS)

> **Motto:** Containers package application dependencies; ECS Fargate eliminates server management; VPC networking secures the perimeter.

---

## 1. Architectural Diagram

```text
                           [ Route 53 Public DNS ]
                                     │
                                     ▼
                [ Application Load Balancer (Public Subnets) ]
                                     │
                ┌────────────────────┴────────────────────┐
                ▼                                         ▼
    [ Availability Zone A ]                   [ Availability Zone B ]
    ┌─────────────────────────────┐           ┌─────────────────────────────┐
    │ Private App Subnet A        │           │ Private App Subnet B        │
    │ ┌─────────────────────────┐ │           │ ┌─────────────────────────┐ │
    │ │ ECS Fargate Task        │ │           │ │ ECS Fargate Task        │ │
    │ │ (awsvpc network mode)   │ │           │ │ (awsvpc network mode)   │ │
    │ │ • Container App         │ │           │ │ • Container App         │ │
    │ │ • Secrets via SSM/KMS   │ │           │ │ • Secrets via SSM/KMS   │ │
    │ └───────────┬─────────────┘ │           │ └───────────┬─────────────┘ │
    └─────────────┼───────────────┘           └─────────────┼───────────────┘
                  │                                         │
                  └────────────────────┬────────────────────┘
                                       │ (TCP 5432)
                                       ▼
    ┌───────────────────────────────────────────────────────────────────────┐
    │ Private Database Subnets                                              │
    │ ┌─────────────────────────┐             ┌───────────────────────────┐ │
    │ │ Amazon RDS PostgreSQL   │══(Sync Rep)═│ Standby Multi-AZ Instance │ │
    │ └─────────────────────────┘             └───────────────────────────┘ │
    └───────────────────────────────────────────────────────────────────────┘
```

---

## 2. Crucial Architectural Justification: When to Add Redis (and When NOT To)

> **Architectural Guardrail:** Do NOT add ElastiCache Redis simply because it is fashionable in architecture diagrams!

### When Redis IS Justified:
1. **Measured Database Read Saturation:** Profiling shows 85%+ CPU utilization on PostgreSQL primarily answering identical, read-heavy query patterns (e.g. top 10 products, product catalog).
2. **Sub-Millisecond SLA:** The business requires p99 response times < 2ms, which physical disk-backed relational databases cannot achieve.
3. **Distributed Session State / Rate Limiting:** High-frequency atomic counter operations (e.g. API rate limiting 10,000 req/sec) that would thrash database row locks.

### When Redis is an Anti-Pattern:
- Your database is operating at 15% CPU.
- Your data changes constantly and cache invalidation adds high complexity and stale-data bugs.
- You are adding Redis before creating proper PostgreSQL B-tree indexes! (An index often drops query time from 2,000ms to 2ms without adding a $30/month Redis node).

---

## 3. ECS Fargate Deep-Dive: Networking & IAM Separation

In modern ECS Fargate, each task runs in `awsvpc` network mode, which means **every task gets its own dedicated Elastic Network Interface (ENI) and private IP address** inside your private subnet.

### Two Separate IAM Roles:
1. **Task Execution Role (`executionRoleArn`):**
   - Used by the AWS ECS Agent to pull the Docker image from ECR and fetch encrypted secrets from AWS Secrets Manager or SSM Parameter Store before the container boots.
2. **Task Role (`taskRoleArn`):**
   - Used by your application code running inside the container to make AWS API calls (e.g., reading an S3 bucket or putting a message on SQS).

---

## 4. Well-Architected Review

### Security
- **No Inbound Public Access:** Fargate tasks run in private subnets with zero public IP addresses. Inbound traffic can ONLY arrive from the ALB's security group.
- **Zero Hardcoded Passwords:** Database credentials stored in AWS Secrets Manager and injected dynamically into container environment variables at task launch.

### Reliability
- **Automated Task Health Checking & Replacement:** If a container task exits (PID 1 crashes) or fails the ALB HTTP health check, ECS automatically terminates the task and launches a new one.

### Cost
- Fargate charges per vCPU-hour and GB-RAM-hour consumed.
- Minimum size: 0.25 vCPU, 0.5 GB RAM (~$0.012 / hour per running task).
- Baseline monthly estimate: ~$25 - $40 / month (ALB + 2 Fargate tasks + RDS).

---

## 5. Teardown & Cleanup

```bash
# Scale ECS service to 0 and delete service
aws ecs update-service --cluster aws-from-scratch-cluster --service app-service --desired-count 0
aws ecs delete-service --cluster aws-from-scratch-cluster --service app-service

# Delete ALB, RDS, and ECR repository
aws elbv2 delete-load-balancer --load-balancer-arn "$ALB_ARN"
aws rds delete-db-instance --db-instance-identifier aws-from-scratch-db --skip-final-snapshot
aws ecr delete-repository --repository-name aws-from-scratch-app --force
```

### Verify Cleanup
```bash
./scripts/cleanup-check.sh
```
