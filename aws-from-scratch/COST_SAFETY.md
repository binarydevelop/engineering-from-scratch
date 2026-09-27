# Cost Safety Guide: The Zero-Surprise Cloud Protocol

> **Rule 0 of Cloud Engineering:** A cloud experiment is NOT finished until all resources are deleted and deletion has been explicitly verified.

Cloud infrastructure differs from a local laptop in one fundamental way: **idle resources accrue continuous financial liability**. If you run a Docker container locally and close your laptop lid, your CPU sleeps and your electricity bill barely twitches. If you launch a multi-AZ RDS database or a NAT Gateway on AWS and forget about it for 30 days, your credit card will be billed continuously.

This document establishes the mandatory Cost Safety Protocol for all labs in `aws-from-scratch`.

---

## 1. The Cost Mental Model

AWS bills based on five fundamental resource consumption dimensions:

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                           AWS BILLING PRIMITIVES                        │
├───────────────────┬─────────────────────────────────────────────────────┤
│ Dimension         │ Examples                                            │
├───────────────────┼─────────────────────────────────────────────────────┤
│ 1. Time (Hourly)  │ EC2 running hours, NAT Gateway hours, RDS hours,    │
│                   │ ALB hourly charges. Bill continuously while active. │
├───────────────────┼─────────────────────────────────────────────────────┤
│ 2. Storage (GB-Mo)│ S3 stored gigabytes, EBS volume provisioned size,   │
│                   │ RDS storage, DynamoDB storage. Accrues even if idle!│
├───────────────────┼─────────────────────────────────────────────────────┤
│ 3. Requests/Calls │ S3 PUT/GET, API Gateway requests, DynamoDB RCUs/WCUs│
│                   │ SQS SendMessage, Lambda invocations.                │
├───────────────────┼─────────────────────────────────────────────────────┤
│ 4. Data Transfer  │ Egress to internet, cross-AZ traffic, cross-region. │
│                   │ Ingress is free; egress costs money.                │
├───────────────────┼─────────────────────────────────────────────────────┤
│ 5. Provisioned    │ DynamoDB provisioned throughput, ElastiCache nodes, │
│    Capacity       │ Kinesis shards, RDS provisioned IOPS.               │
└───────────────────┴─────────────────────────────────────────────────────┘
```

### The "Idle Resource" Trap
The most common source of surprise AWS bills is **not** high traffic—it is **abandoned infrastructure**:
1. **NAT Gateways**: Cost ~$0.045/hour (~$32.40/month per gateway) even with zero packets flowing. If deployed across 2 AZs, that is ~$65/month for an idle lab!
2. **Unattached EBS Volumes**: When you terminate an EC2 instance without deleting the attached EBS volume (or if you detach a volume and leave it), AWS continues billing for the provisioned disk capacity (e.g. $0.08/GB-month for gp3).
3. **Application Load Balancers (ALBs)**: Cost ~$0.0225/hour (~$16.20/month) + LCU hours even if zero requests are served.
4. **Elastic IP Addresses (EIPs)**: Unattached Elastic IPs incur an idle charge (~$0.005/hour) to discourage public IPv4 hoarding. In modern AWS, even in-use public IPv4 addresses incur a small hourly charge (~$0.005/hour).
5. **Multi-AZ Databases**: Running an idle `db.t4g.micro` or `db.m6g.large` in Multi-AZ duplicates compute and synchronous storage costs across two physical availability zones.

---

## 2. Mandatory Pre-Lab Setup: Guardrails

Before executing any phase that communicates with live AWS APIs, you MUST configure these three safety guardrails:

### Step 1: Set Up an AWS Zero-Spend Budget
An AWS Budget sends an automated email alert when your forecasted or actual spending exceeds a dollar threshold (e.g., $1.00 or $5.00).

```bash
# Create a zero-spend / $5 budget alert using AWS CLI
aws budgets create-budget \
    --account-id $(aws sts get-caller-identity --query Account --output text) \
    --budget '{
        "BudgetName": "aws-from-scratch-safety-budget",
        "BudgetLimit": {
            "Amount": "5.0",
            "Unit": "USD"
        },
        "TimeUnit": "MONTHLY",
        "BudgetType": "COST"
    }' \
    --notifications-with-subscribers '[{
        "Notification": {
            "NotificationType": "ACTUAL",
            "ComparisonOperator": "GREATER_THAN",
            "Threshold": 80,
            "ThresholdType": "PERCENTAGE"
        },
        "Subscribers": [{
            "SubscriptionType": "EMAIL",
            "Address": "your-email@example.com"
        }]
    }]'
```

### Step 2: Set Up a CloudWatch Billing Alarm
Billing metrics are published to CloudWatch in the `us-east-1` region (regardless of where your resources run).

```bash
# Create a CloudWatch Alarm for estimated charges > $3.00
aws cloudwatch put-metric-alarm \
    --region us-east-1 \
    --alarm-name "aws-from-scratch-spend-alert" \
    --alarm-description "Triggered when estimated monthly AWS charges exceed $3" \
    --metric-name "EstimatedCharges" \
    --namespace "AWS/Billing" \
    --statistic "Maximum" \
    --period 21600 \
    --threshold 3.0 \
    --comparison-operator "GreaterThanThreshold" \
    --evaluation-periods 1
```

### Step 3: Mandatory Lab Resource Tagging
All resources created in this curriculum must carry three standard tags:

```text
Key: Project      Value: aws-from-scratch
Key: Lesson       Value: <lesson-slug> (e.g., 06-vpc-from-scratch)
Key: Environment  Value: learning
```

This ensures our automated inventory scanner (`scripts/list-lab-resources.sh`) can discover and list every resource created by your labs.

---

## 3. Data Transfer Charges: The Hidden Vector

Data transfer in cloud computing follows an asymmetric cost model:

```text
           Internet
              │
              │ INCOMING DATA: FREE ($0.00 / GB)
              ▼
       ┌──────────────┐
       │     VPC      │
       │  Subnet A    │
       └──────┬───────┘
              │
              ├── CROSS-AZ TRANSFER: ~$0.01 / GB each direction
              │   (Data crossing between AZ-A and AZ-B)
              ▼
       ┌──────────────┐
       │     VPC      │
       │  Subnet B    │
       └──────┬───────┘
              │
              │ OUTGOING DATA TO INTERNET: ~$0.09 / GB (after first 100GB/mo)
              ▼
           Internet
```

**Golden Rules of Data Transfer:**
1. **Never benchmark bandwidth with large multi-gigabyte transfers over the public internet** during learning labs.
2. **Keep communication within the same Availability Zone** during single-node performance experiments.
3. **Use S3 Gateway Endpoints** inside your VPC: S3 Gateway Endpoints route S3 traffic over the internal AWS network at **$0.00/hour and $0.00/GB**, avoiding NAT Gateway data transfer processing charges!

---

## 4. Regional Price Disparities

AWS pricing is not uniform across the globe:
- `us-east-1` (N. Virginia) and `us-west-2` (Oregon) are typically among the lowest-cost regions.
- `eu-central-1` (Frankfurt), `ap-southeast-1` (Singapore), or `sa-east-1` (São Paulo) can be 15% to 40% higher due to local real estate, power, and regulatory costs.
- Always check the official [AWS Pricing Calculator](https://calculator.aws/#/) before provisioning non-trivial workloads.

---

## 5. The Verification & Teardown Protocol

Every single lesson in this repository includes:
1. `## Cost Warning`: Explicit disclosure of billing vectors.
2. `## Resources Created`: Exact list of every AWS resource provisioned.
3. `## How to Verify Them`: The AWS CLI command to list active resources.
4. `## Cleanup`: The precise teardown commands.
5. `## How to Verify Cleanup`: The command confirming the resource list is empty.

To check your account across all services for lingering lab resources, run:

```bash
./scripts/list-lab-resources.sh
```

And to verify zero leftover lab footprint:

```bash
./scripts/cleanup-check.sh
```

---

## 6. Official Pricing Reference Checklist

*Prices change over time and vary by region. Always consult official AWS pricing pages:*
- EC2 On-Demand Pricing: `https://aws.amazon.com/ec2/pricing/on-demand/`
- S3 Storage Pricing: `https://aws.amazon.com/s3/pricing/`
- RDS Relational Database Pricing: `https://aws.amazon.com/rds/pricing/`
- DynamoDB Pricing: `https://aws.amazon.com/dynamodb/pricing/`
- Lambda Serverless Pricing: `https://aws.amazon.com/lambda/pricing/`
- VPC NAT Gateway Pricing: `https://aws.amazon.com/vpc/pricing/`
- AWS Free Tier Details: `https://aws.amazon.com/free/`
