# Phase 24: Multi-AZ Application

## Motto
> Redundancy without geographic separation is an illusion. Multi-AZ is the baseline of cloud reliability.

**Type:** Architecture Project & Failure Injection  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 23: ALB  
**AWS Services Involved:** ALB, Multi-AZ EC2, Cross-Zone Load Balancing  
**Cost Vector:** Cross-AZ traffic between ALB and target instances in different AZs is covered by standard cross-AZ data transfer fees ($0.01/GB).  

---

## Problem
Running two EC2 instances in the same Availability Zone protects against software crashes, but a datacenter power outage destroys both simultaneously.

---

## Prediction
Deploying Instance A in AZ-1 and Instance B in AZ-2 behind a Multi-AZ ALB allows one entire AZ to be destroyed with zero downtime for clients.

---

## Why this matters
This is Project 02 in the curriculum and the standard reference architecture for highly available web systems.

---

## First principles
Availability Zones are independent physical failure domains with isolated power feeds, backup generators, and physical facilities. Deploying stateless compute across two or more AZs ensures that any localized catastrophe has a blast radius bounded to a fraction of your fleet.

---

## Mental model
```text
Multi-AZ Architecture:
                    [ Public Internet ]
                             │
                             ▼
            [ Application Load Balancer (Multi-AZ) ]
                             │
            ┌────────────────┴────────────────┐
            ▼                                 ▼
   [ us-east-1a (DC 1) ]             [ us-east-1b (DC 2) ]
   ┌──────────────────────┐          ┌──────────────────────┐
   │ EC2 Instance A       │          │ EC2 Instance B       │
   │ (Private IP: 10.0.1) │          │ (Private IP: 10.0.2) │
   └──────────────────────┘          └──────────────────────┘
```

---

## Architecture before AWS
Active-passive hot standby datacenters with automated DNS failover.

---

## Build the primitive
```python
# Verification of multi-AZ target distribution
targets = [{"id": "i-001a", "az": "us-east-1a"}, {"id": "i-002b", "az": "us-east-1b"}]
distinct_azs = len(set(t['az'] for t in targets))
print(f"Distinct AZs spanned: {distinct_azs} (Multi-AZ compliant: {distinct_azs >= 2})")
```

---

## Use AWS
```bash
aws ec2 describe-instances --filters 'Name=tag:Project,Values=aws-from-scratch' --query 'Reservations[].Instances[].[InstanceId,Placement.AvailabilityZone]' --output table
```

---

## Inspect it
```bash
aws elbv2 describe-target-health --target-group-arn $TG_ARN --output table
```

---

## Measure it
Simulate client traffic while terminating the instance in AZ-A; measure 5xx error rate (should be 0.00%).

---

## Break it
Terminate the instance in us-east-1a via `aws ec2 terminate-instances`.

---

## Diagnose it
ALB detects AZ-A target unhealthy; all incoming traffic seamlessly served by AZ-B target.

---

## Recover it
Launch a replacement instance in us-east-1a.

---

## Security
Enforce least-privilege Security Groups: EC2 instances only accept traffic from the ALB's Security Group ID.

---

## Cost
### Cost Warning
Cross-AZ traffic between ALB and target instances in different AZs is covered by standard cross-AZ data transfer fees ($0.01/GB).

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
aws elbv2 delete-load-balancer --load-balancer-arn $ALB_ARN && aws ec2 terminate-instances --instance-ids $INST_A $INST_B
```

---

## Verify cleanup
```bash
./scripts/cleanup-check.sh
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-24-evidence.md`.

---

## Questions for mastery
1. What happens if Cross-Zone Load Balancing is disabled on an ALB that has 8 instances in AZ-A and 2 instances in AZ-B?
2. Why must the application instances be stateless for Multi-AZ load balancing to work correctly?
3. What failure modes does Multi-AZ protect against, and which failure modes does it NOT protect against?

---

## When to use this
Use Multi-AZ for all production workloads requiring 99.9%+ availability.

---

## When not to use this
Do not deploy Multi-AZ for short-lived non-critical batch jobs where failure simply means retrying.

---

## What comes next
Phase 25: Auto Scaling — Dynamic fleet sizing based on real-time load signals.
