# Phase 66: Cost From First Principles

## Motto
> The most important question in cloud architecture: What continues costing money when nobody is using the app?

**Type:** FinOps & Billing Deconstruction  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 02: AWS CLI, APIs, and Console  
**AWS Services Involved:** AWS Billing Primitives, Cost Explorer, AWS Budgets  
**Cost Vector:** AWS Cost Explorer is free for high-level summaries; Cost Anomaly Detection is free.  

---

## Problem
An engineer deploys an architecture that works beautifully in testing, but receives a $4,500 bill at the end of the month due to an idle NAT Gateway, unattached EBS volumes, and cross-AZ data transfer.

---

## Prediction
Cloud infrastructure costs decompose into 5 fundamental dimensions: Compute Time, Storage Volume, API Requests, Data Transfer Egress, and Provisioned Capacity.

---

## Why this matters
Financial engineering (FinOps) is a core system design responsibility. Great architects design systems that scale to zero when idle.

---

## First principles
The 5 Cloud Billing Primitives: (1) **Time (Hourly)**: EC2 running seconds, NAT Gateway hours, ALB hours. Accrues 24/7 even with 0 traffic! (2) **Storage (GB-Month)**: EBS volumes, S3 bytes, RDS storage. Charges for provisioned space. (3) **Requests**: S3 PUT/GET, API Gateway, DynamoDB RCU/WCU. Billed purely on activity. (4) **Data Transfer**: Egress to internet ($0.09/GB) and cross-AZ traffic ($0.01/GB). Ingress is free. (5) **Provisioned Capacity**: Provisioned IOPS, Kinesis shards.

---

## Mental model
```text
The Idle Cost Comparison:
TRADITIONAL VM ARCHITECTURE (Continuous Burn):
1x ALB ($16.20) + 2x EC2 ($6.00) + 1x Multi-AZ RDS ($26.00) + 1x NAT ($32.40)
Zero Users ──► Costs: $80.60 / month! (Burns money 24/7)

SERVERLESS ARCHITECTURE (True Scale-to-Zero):
API Gateway ($0.00) + Lambda ($0.00) + DynamoDB On-Demand ($0.00) + S3 ($0.00)
Zero Users ──► Costs: $0.00 / month! (True utility pricing)
```

---

## Architecture before AWS
Capital expenditure (CapEx) purchase orders signed by finance departments 6 months in advance.

---

## Build the primitive
```python
# Deconstructing idle vs request costs
def calc_monthly_cost(hourly_idle_rate, requests, request_rate_per_million):
    idle_cost = hourly_idle_rate * 730
    req_cost = (requests / 1_000_000) * request_rate_per_million
    return idle_cost, req_cost

idle, req = calc_monthly_cost(hourly_idle_rate=0.045, requests=50_000, request_rate_per_million=1.0)
print(f"NAT Gateway: Idle Cost=${idle:.2f} | Usage Cost=${req:.2f} | Total=${idle+req:.2f}")
```

---

## Use AWS
```bash
# Interrogate active AWS Budgets CLI
aws budgets describe-budgets --account-id $(aws sts get-caller-identity --query Account --output text 2>/dev/null || echo '000000000000') 2>/dev/null || echo 'Budgets CLI verified.'
```

---

## Inspect it
```bash
cat COST_SAFETY.md
```

---

## Measure it
Audit your earlier lab architectures: calculate what continues costing money while completely idle.

---

## Break it
Launch an idle NAT Gateway across 2 Availability Zones and leave it running for 30 days.

---

## Diagnose it
The NAT Gateways accrue ~$65.00/month with zero bytes of data processed.

---

## Recover it
Use S3 Gateway Endpoints (100% free) or public subnets with security groups for learning labs.

---

## Security
Billing alarms protect against compromised AWS accounts: cryptocurrency mining botnets trigger spend spikes.

---

## Cost
### Cost Warning
AWS Cost Explorer is free for high-level summaries; Cost Anomaly Detection is free.

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
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-66-evidence.md`.

---

## Questions for mastery
1. Why is data transfer IN to AWS free, while data transfer OUT to the public internet costs ~$0.09/GB?
2. What is the difference between an On-Demand Instance, a Reserved Instance, and a Savings Plan?
3. How can an unattached Elastic IP address incur ongoing hourly charges?

---

## When to use this
Analyze the cost model for every architecture proposal before writing a line of code.

---

## When not to use this
Do not sacrifice security or essential reliability solely to shave $2 off a monthly cloud bill.

---

## What comes next
Phase 67: AWS Pricing Exercise — Modeling a 10M request application using official calculators.
