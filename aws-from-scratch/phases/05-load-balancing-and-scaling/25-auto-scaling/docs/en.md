# Phase 25: Auto Scaling

## Motto
> Elasticity means paying for what you need when you need it, and turning it off when you don't.

**Type:** Hands-on Lab & Dynamic Elasticity  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 24: Multi-AZ Application  
**AWS Services Involved:** Auto Scaling Groups (ASG), Launch Templates, Target Tracking Policies  
**Cost Vector:** Auto Scaling Groups are free; you pay only for the underlying EC2 instances and CloudWatch alarms.  

---

## Problem
Traffic fluctuates dramatically throughout the day. Fixed static server fleets either crash during traffic spikes or waste thousands of dollars sitting idle at night.

---

## Prediction
Applying synthetic CPU load to an ASG will trigger a CloudWatch alarm and cause the ASG to launch replacement instances automatically.

---

## Why this matters
Auto Scaling is the essence of cloud elasticity. It handles both demand-driven scaling and automatic self-healing when hardware fails.

---

## First principles
An Auto Scaling Group (ASG) is a control loop supervisor: `DesiredCapacity = f(Metric, Min, Max)`. The ASG periodically reconciles current healthy instances against the desired capacity. If an instance fails its EC2 or ALB health check, the ASG terminates it and provisions a fresh replacement from the Launch Template.

---

## Mental model
```text
Auto Scaling Control Loop:
[ CloudWatch Metric: CPU > 70% ]
                │
                ▼
[ Auto Scaling Group ] ──► Reconciles: Desired (2) ──► Increase to Desired (4)
                                                              │
             ┌────────────────────────────────────────────────┘
             ▼
[ EC2 API: RunInstances ] ──► Boots 2 Fresh Instances ──► Registers with ALB Target Group
```

---

## Architecture before AWS
Capacity planning meetings 6 months in advance; over-provisioning datacenter hardware to survive peak Black Friday traffic.

---

## Build the primitive
```python
# ASG capacity reconciliation logic
current = 2
target_cpu = 75
actual_cpu = 90
if actual_cpu > target_cpu:
    desired = min(current * 2, 10) # Scale out up to max 10
    print(f"Scale-out triggered! Desired capacity updated from {current} to {desired}")
```

---

## Use AWS
```bash
aws autoscaling create-auto-scaling-group --auto-scaling-group-name lab-asg --launch-template LaunchTemplateName=lab-lt --min-size 1 --max-size 4 --desired-capacity 2 --vpc-zone-identifier '$PUB_SUBNET_1,$PUB_SUBNET_2' --tags Key=Project,Value=aws-from-scratch
```

---

## Inspect it
```bash
aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names lab-asg --output json
```

---

## Measure it
Measure scale-out reaction time: CloudWatch alarm evaluation period (1-3 min) + instance boot time (1-2 min).

---

## Break it
Manually terminate an EC2 instance managed by the ASG.

---

## Diagnose it
The ASG detects current capacity (1) < desired capacity (2); immediately calls `ec2:RunInstances` to launch a replacement.

---

## Recover it
The replacement instance boots, passes health checks, and returns fleet capacity to 2.

---

## Security
Enforce strict Launch Template versioning to prevent untracked configuration changes.

---

## Cost
### Cost Warning
Auto Scaling Groups are free; you pay only for the underlying EC2 instances and CloudWatch alarms.

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
aws autoscaling update-auto-scaling-group --auto-scaling-group-name lab-asg --min-size 0 --desired-capacity 0
aws autoscaling delete-auto-scaling-group --auto-scaling-group-name lab-asg --force-delete
```

---

## Verify cleanup
```bash
aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names lab-asg --query 'AutoScalingGroups[]' --output text
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-25-evidence.md`.

---

## Questions for mastery
1. Why does an Auto Scaling scale-out action have a warm-up / cooldown period?
2. What happens if your scaling metric is CPU utilization, but the bottleneck is database lock contention?
3. Why should an ASG balance instances evenly across Availability Zones?

---

## When to use this
Use Auto Scaling Groups for any production stateless server fleet—even with min=1, max=1 for self-healing!

---

## When not to use this
Do not use standard ASGs for stateful relational databases that cannot scale horizontally by adding nodes.

---

## What comes next
Phase 26: RDS From First Principles — Managed relational databases.
