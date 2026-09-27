# Project 02: Highly Available Web Application (ALB + ASG + Multi-AZ RDS)

> **Motto:** High availability is not a magic configuration toggle: it is physical redundancy across independent power, cooling, and failure domains.

---

## 1. Architectural Diagram

```text
                           [ Public Internet ]
                                    │
                                    ▼
                 [ Application Load Balancer (Public Subnets) ]
                          (Port 80 / 443 | Multi-AZ)
                                    │
                ┌───────────────────┴───────────────────┐
                ▼                                       ▼
    [ Availability Zone A ]                 [ Availability Zone B ]
    ┌───────────────────────────┐           ┌───────────────────────────┐
    │ Private Subnet A          │           │ Private Subnet B          │
    │ ┌───────────────────────┐ │           │ ┌───────────────────────┐ │
    │ │ EC2 Instance (App-A)  │ │           │ │ EC2 Instance (App-B)  │ │
    │ │ Auto Scaling Group    │ │           │ │ Auto Scaling Group    │ │
    │ └───────────┬───────────┘ │           │ └───────────┬───────────┘ │
    └─────────────┼─────────────┘           └─────────────┼─────────────┘
                  │                                       │
                  └───────────────────┬───────────────────┘
                                      │ (TCP 5432)
                                      ▼
    ┌───────────────────────────────────────────────────────────────────┐
    │ Database Subnet Group (Isolated Private Subnets)                 │
    │ ┌───────────────────────┐             ┌─────────────────────────┐ │
    │ │ Amazon RDS PostgreSQL │══(Sync Rep)═│ Standby Replica (AZ-B)  │ │
    │ │ Primary (AZ-A)        │             │ (Automatic Failover)    │ │
    │ └───────────────────────┘             └─────────────────────────┘ │
    └───────────────────────────────────────────────────────────────────┘
```

---

## 2. Evolution Path: From Snowflake to Highly Available

```text
Step 1: Single EC2 Snowflake
        - Single point of failure.
        - Database and app on same disk.
        - Patching or hardware death = complete outage.

Step 2: Externalize Database to Amazon RDS
        - Compute separated from relational state.
        - Automated daily EBS snapshots and point-in-time recovery (PITR).

Step 3: Multi-AZ RDS Deployment
        - Synchronous block-level replication to standby AZ.
        - Automatic DNS failover in 60-120 seconds if primary AZ suffers power failure.

Step 4: Horizontal Scaling with Application Load Balancer & ASG
        - Application compute made stateless.
        - Traffic distributed evenly across AZ-A and AZ-B.
        - Auto Scaling launches replacements automatically if a node dies.
```

---

## 3. Network & Security Group Isolation Boundaries

Security groups must form an unbroken chain of least privilege:

```text
1. ALB Security Group (sg-alb):
   - Inbound:  TCP 80 / 443 from 0.0.0.0/0
   - Outbound: TCP 8080 to sg-app

2. Application Security Group (sg-app):
   - Inbound:  TCP 8080 ONLY from sg-alb (NOT from 0.0.0.0/0!)
   - Outbound: TCP 5432 to sg-rds, TCP 443 to VPC Endpoints / SSM

3. RDS Database Security Group (sg-rds):
   - Inbound:  TCP 5432 ONLY from sg-app
   - Outbound: None required
```

---

## 4. Well-Architected Review

### Reliability
- **Multi-AZ Blast Radius:** If AZ-A experiences a total power outage, the ALB automatically drops the unhealthy targets in AZ-A; the ASG provisions new instances in AZ-B; and RDS flips the CNAME to the Standby replica in AZ-B.
- **RTO / RPO:** RTO is ~60-120 seconds for database failover. RPO is 0 seconds (synchronous replication guarantees zero committed transaction data loss).

### Security
- Database instances have `PubliclyAccessible: false` and reside in private subnets with zero route to the Internet Gateway.
- Application servers use IAM Instance Profiles to communicate with AWS Systems Manager (SSM Session Manager). No SSH port 22 is open to the internet.

### Cost Optimization
- Baseline idle costs:
  - 1x ALB: ~$16.20/month
  - 2x `t4g.micro` EC2 instances: ~$6.00/month
  - 1x `db.t4g.micro` Multi-AZ RDS instance: ~$24.00/month
- **Total estimated running baseline:** ~$46 - $55 / month.
- **Lab Rule:** Always terminate and delete resources immediately after completing the lab!

---

## 5. Cost Warning & Cleanup Verification

### Cost Warning
This lab creates billable resources (ALB, 2x EC2 instances, Multi-AZ RDS). Do not leave them running overnight.

### Teardown Commands
```bash
# 1. Terminate Auto Scaling Group (scales EC2 instances to 0)
aws autoscaling update-auto-scaling-group --auto-scaling-group-name aws-from-scratch-asg --min-size 0 --desired-capacity 0
aws autoscaling delete-auto-scaling-group --auto-scaling-group-name aws-from-scratch-asg --force-delete

# 2. Delete ALB and Target Group
aws elbv2 delete-load-balancer --load-balancer-arn "$ALB_ARN"
aws elbv2 delete-target-group --target-group-arn "$TG_ARN"

# 3. Delete RDS Database (skip final snapshot for learning labs)
aws rds delete-db-instance --db-instance-identifier aws-from-scratch-db --skip-final-snapshot
```

### Verify Cleanup
```bash
./scripts/cleanup-check.sh
```
