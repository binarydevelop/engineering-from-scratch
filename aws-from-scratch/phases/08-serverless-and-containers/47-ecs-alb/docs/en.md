# Phase 47: ECS + ALB

## Motto
> Containers have dynamic IP addresses. The ALB Target Group dynamically tracks container lifecycles.

**Type:** Architecture Project & Target Registration  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 46: Fargate  
**AWS Services Involved:** ECS Service, Application Load Balancer Target Group  
**Cost Vector:** Running 2 Fargate tasks + ALB costs ~$1.20 per day. Tear down immediately after testing!  

---

## Problem
When Fargate tasks scale from 2 to 10 instances, they receive 8 new private IP addresses. How does the Load Balancer discover and route traffic to them without manual reconfiguration?

---

## Prediction
Connecting an ECS Service to an ALB Target Group instructs the ECS control plane to automatically register new task private IPs with the target group upon boot and deregister them before shutdown.

---

## Why this matters
This is Project 05 in the curriculum and the architecture powering modern containerized microservices in AWS.

---

## First principles
In `awsvpc` mode, each container has its own private IP. The ECS Service acts as the glue: when a task transitions to `RUNNING`, ECS calls `elbv2:RegisterTargets`. The ALB probes `/health`; once healthy, traffic begins flowing. During deployments, the ALB drains connections (`deregistration_delay`) before ECS terminates the old task.

---

## Mental model
```text
ECS + ALB Dynamic Target Sync:
[ Internet ] ──► [ Application Load Balancer ]
                         │
                         ▼ Target Group (Dynamic IP Tracking)
        ┌────────────────┴────────────────┐
        ▼ (Auto-Registered)               ▼ (Auto-Registered)
[ Fargate Task: 10.0.1.42 ]       [ Fargate Task: 10.0.2.88 ]
(Health: 200 OK -> Serving)       (Health: 200 OK -> Serving)
```

---

## Architecture before AWS
Consul / Etcd service discovery with Consul-Template rewriting Nginx upstream blocks and issuing reload signals.

---

## Build the primitive
```python
# Simulating dynamic target registration
target_pool = set()
def on_task_launch(ip): target_pool.add(ip)
def on_task_terminate(ip): target_pool.remove(ip)
on_task_launch("10.0.1.42")
on_task_launch("10.0.2.88")
print("ALB Target Pool actively serving:", target_pool)
```

---

## Use AWS
```bash
aws ecs create-service --cluster lab-cluster --service-name web-svc --task-definition web-app --desired-count 2 --launch-type FARGATE --load-balancers targetGroupArn=$TG_ARN,containerName=web,containerPort=80 --network-configuration 'awsvpcConfiguration={subnets=[$PRIV_SUB_1,$PRIV_SUB_2],securityGroups=[$APP_SG]}'
```

---

## Inspect it
```bash
aws elbv2 describe-target-health --target-group-arn $TG_ARN --output table
```

---

## Measure it
Measure zero-downtime rolling update duration: ECS launches new v2 task -> waits for ALB health pass -> drains v1 task -> terminates v1.

---

## Break it
Deploy an updated task definition where the container crashes on startup (bad config).

---

## Diagnose it
The new task fails ALB health checks; ECS refuses to drain the old healthy v1 tasks. Rolling update halts safely!

---

## Recover it
Rollback the service to the prior task definition version.

---

## Security
Containers in private subnets accept traffic ONLY from the ALB's security group ID. Direct internet access is impossible.

---

## Cost
### Cost Warning
Running 2 Fargate tasks + ALB costs ~$1.20 per day. Tear down immediately after testing!

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
aws ecs update-service --cluster lab-cluster --service-name web-svc --desired-count 0 && aws ecs delete-service --cluster lab-cluster --service-name web-svc
```

---

## Verify cleanup
```bash
./scripts/cleanup-check.sh
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-47-evidence.md`.

---

## Questions for mastery
1. What is ALB Connection Draining (Deregistration Delay) and why is it crucial for zero-downtime deployments?
2. What happens if your ECS service has `minimumHealthyPercent=100` and `maximumPercent=200` during a rolling update?
3. How does an ECS health check differ from an ALB health check?

---

## When to use this
Use ECS + ALB for production containerized APIs, web frontends, and internal microservices.

---

## When not to use this
Do not attach an ALB to background asynchronous worker tasks that only pull messages from SQS.

---

## What comes next
Phase 48: Kubernetes / EKS Overview — When is Kubernetes complexity justified over ECS?
