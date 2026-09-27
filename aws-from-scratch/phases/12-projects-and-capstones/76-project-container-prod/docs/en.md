# Phase 76: Project: Containerized Production Application

## Motto
> Containers package dependencies; Fargate eliminates server management; VPC networking secures the perimeter.

**Type:** Architecture Project & Container Production  
**Time Estimate:** ~90 minutes  
**Prerequisites:** Phase 47: ECS + ALB  
**AWS Services Involved:** ECS Fargate, ALB, RDS PostgreSQL, Secrets Manager, ECR  
**Cost Vector:** Running cost is ~$25-40/month if left running. Terminate immediately after completing the lab!  

---

## Problem
Monolithic applications require complex system libraries and dependencies that don't fit into Lambda's execution limits.

---

## Prediction
Deploying an ECS Fargate service in private subnets behind an ALB with RDS PostgreSQL and dynamic secrets creates a secure, auto-recovering container cluster.

---

## Why this matters
This is Project 05: the enterprise container standard for running microservices in AWS.

---

## First principles
Fargate tasks run in `awsvpc` mode with dedicated private IPs. The ALB routes public traffic to healthy tasks. Tasks fetch database passwords dynamically from Secrets Manager via IAM Task Execution Roles. ElastiCache is evaluated and only added if measured read bottlenecks justify it.

---

## Mental model
```text
Project 05 Architecture:
[ Internet ] ──► [ Route 53 ] ──► [ ALB (Public Multi-AZ) ]
                                         │
        ┌────────────────────────────────┴────────────────────────────────┐
        ▼ (Private App Subnet A)                                          ▼ (Private App Subnet B)
[ ECS Fargate Task 1 ]                                            [ ECS Fargate Task 2 ]
• awsvpc Network Mode                                             • awsvpc Network Mode
• Secrets via IAM                                                 • Secrets via IAM
        │                                                                 │
        └────────────────────────────────┬────────────────────────────────┘
                                         │ TCP 5432
                                         ▼
                            [ Amazon RDS PostgreSQL ]
                            (Multi-AZ Isolated Database)
```

---

## Architecture before AWS
Managing Docker Swarm or Nomad clusters on physical server hardware.

---

## Build the primitive
```python
with open('projects/project-05-container-prod/README.md') as f:
    print("Project 05 loaded:", "ECS Fargate + ALB + RDS" in f.read())
```

---

## Use AWS
```bash
# Implementation commands in projects/project-05-container-prod/README.md
```

---

## Inspect it
```bash
aws ecs list-tasks --cluster aws-from-scratch-cluster --output table
```

---

## Measure it
Measure zero-downtime rolling update duration: ECS rolls out new container image with 0% 5xx errors.

---

## Break it
Kill container PID 1 inside the running Fargate task.

---

## Diagnose it
The task exits; ECS supervisor detects task stopped; immediately provisions a new Fargate task.

---

## Recover it
The replacement task registers with the ALB target group automatically.

---

## Security
Zero public IP addresses on container tasks or database instances. No SSH ports open.

---

## Cost
### Cost Warning
Running cost is ~$25-40/month if left running. Terminate immediately after completing the lab!

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
Follow teardown commands in `projects/project-05-container-prod/README.md`.
```

---

## Verify cleanup
```bash
./scripts/cleanup-check.sh
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-76-evidence.md`.

---

## Questions for mastery
1. Why is adding Redis an antipattern if database CPU is at 15% and queries are fast?
2. What is the difference between ECS Task Execution Role and ECS Task Role?
3. How does Fargate eliminate host operating system patching?

---

## When to use this
Use ECS Fargate for long-running microservices, web apps, and containerized background daemons.

---

## When not to use this
Do not use Fargate if you need direct GPU acceleration or custom kernel network drivers.

---

## What comes next
Phase 77: Project: Data Ingestion Architecture — High-throughput streaming data lakes.
