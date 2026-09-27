# Phase 46: Fargate

## Motto
> Containers without EC2 servers. Every task gets its own dedicated micro-VM and dedicated ENI.

**Type:** Hands-on Lab & Serverless Containers  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 45: ECS  
**AWS Services Involved:** AWS Fargate, awsvpc Network Mode  
**Cost Vector:** Billed strictly per second for vCPU and RAM allocated. Fargate Spot offers up to 70% discount for fault-tolerant tasks.  

---

## Problem
Running ECS on EC2 requires managing EC2 Auto Scaling groups, patching host operating systems, and dealing with bin-packing container placement.

---

## Prediction
AWS Fargate provisions serverless container compute on demand. Each task receives its own Elastic Network Interface with a private IP directly in your VPC subnet.

---

## Why this matters
Fargate eliminates EC2 cluster capacity management, turning containers into true serverless compute units.

---

## First principles
Fargate is a managed capacity provider. When a task launches, AWS provisions a single-tenant micro-VM running on Firecracker/Nitro, attaches a dedicated ENI directly into your VPC subnet, runs the container, and tears it down when done. There are no shared host OS layers between tasks.

---

## Mental model
```text
EC2-Backed vs Fargate Capacity:
EC2-BACKED ECS (You Manage Hosts):
┌────────────────────────────────────────────────────────┐
│ EC2 Instance Host (You manage AMI, OS patches, Docker) │
│ ├── Container A (Port 8080)                            │
│ └── Container B (Port 8081) ──► Port Conflicts & Pack! │
└────────────────────────────────────────────────────────┘

FARGATE SERVERLESS (Zero Host Management):
┌─────────────────────────────┐ ┌─────────────────────────────┐
│ Fargate Task 1              │ │ Fargate Task 2              │
│ • Private IP: 10.0.1.42     │ │ • Private IP: 10.0.2.88     │
│ • Dedicated ENI & Sec Group │ │ • Dedicated ENI & Sec Group │
│ • Dedicated Micro-VM        │ │ • Dedicated Micro-VM        │
└─────────────────────────────┘ └─────────────────────────────┘
```

---

## Architecture before AWS
Managing bare-metal Mesos or Kubernetes worker node pools with manual OS upgrades.

---

## Build the primitive
```python
# Fargate Pricing Model Calculation
vcpu_price_per_hr = 0.04048
gb_price_per_hr = 0.004445
task_cost = (0.25 * vcpu_price_per_hr) + (0.5 * gb_price_per_hr)
print(f"Fargate minimal task hourly cost: ${task_cost:.5f}/hr (~${task_cost * 730:.2f}/month)")
```

---

## Use AWS
```bash
aws ecs run-task --cluster lab-cluster --task-definition web-app --launch-type FARGATE --network-configuration 'awsvpcConfiguration={subnets=[$PRIV_SUBNET_1],securityGroups=[$SG_ID],assignPublicIp=DISABLED}'
```

---

## Inspect it
```bash
aws ecs list-tasks --cluster lab-cluster --output table
```

---

## Measure it
Measure task provisioning time: Fargate tasks typically launch and register ENIs in 20-35 seconds.

---

## Break it
Attempt to SSH into a running Fargate container directly using traditional SSH.

---

## Diagnose it
There is no host OS and port 22 is closed. Direct SSH is impossible.

---

## Recover it
Use **ECS Exec** (via SSM Session Manager) to open an interactive debugging shell inside the container.

---

## Security
Fargate provides hypervisor-level isolation between tasks: containers never share host OS kernels.

---

## Cost
### Cost Warning
Billed strictly per second for vCPU and RAM allocated. Fargate Spot offers up to 70% discount for fault-tolerant tasks.

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
aws ecs stop-task --cluster lab-cluster --task $TASK_ID
```

---

## Verify cleanup
```bash
echo 'Fargate task stopped.'
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-46-evidence.md`.

---

## Questions for mastery
1. Why does every Fargate task require the `awsvpc` network mode?
2. What are the trade-offs between ECS on EC2 vs ECS on Fargate in terms of cost at 100% sustained utilization?
3. How does Fargate Spot handle task interruption notices?

---

## When to use this
Use Fargate for almost all containerized web applications, microservices, and background batch jobs.

---

## When not to use this
Do not use Fargate if you require GPU acceleration, custom kernel parameters (`sysctl`), or root host filesystem access.

---

## What comes next
Phase 47: ECS + ALB — Routing internet traffic to dynamic container tasks.
