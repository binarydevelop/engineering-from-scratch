# Phase 45: ECS

## Motto
> Task Definition is the blueprint. Task is the running container. Service is the supervisor maintaining desired count.

**Type:** Hands-on Lab & Container Orchestration  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 44: ECR  
**AWS Services Involved:** Amazon Elastic Container Service (ECS)  
**Cost Vector:** The ECS control plane is 100% free. You pay only for the compute capacity (EC2 or Fargate) executing the tasks.  

---

## Problem
Running `docker run` on an EC2 instance works until the container crashes or the host runs out of memory. Who restarts failed containers and manages rolling updates?

---

## Prediction
An ECS Service monitors container health: if a task dies, ECS automatically schedules a replacement to maintain the desired count.

---

## Why this matters
ECS is AWS's battle-tested, native container orchestration system. It is significantly simpler and faster than Kubernetes.

---

## First principles
ECS data model consists of four primitives: (1) **Cluster**: Logical grouping of capacity. (2) **Task Definition**: Declarative JSON blueprint (container image, CPU/RAM, ports, env vars). (3) **Task**: A running instance of a Task Definition. (4) **Service**: Long-running supervisor maintaining desired count.

---

## Mental model
```text
ECS Data Model Hierarchy:
[ ECS Cluster: production-cluster ]
  └── [ ECS Service: web-service ] (Desired Count: 2)
        ├── Supervises ──► [ Task 1 (Running on Fargate / EC2) ]
        └── Supervises ──► [ Task 2 (Running on Fargate / EC2) ]
                              ▲
                              │ Instantiated From
        [ Task Definition: web-app:v1 (JSON Blueprint) ]
              └── Image: 123.dkr.ecr.us-east-1.../app:latest
              └── CPU: 256 | RAM: 512 | Ports: 8080
```

---

## Architecture before AWS
Docker Swarm, Mesos Marathon, or custom shell scripts running in systemd loops.

---

## Build the primitive
```python
# ECS Task Definition Structure
task_def = {
    "family": "web-app",
    "networkMode": "awsvpc",
    "containerDefinitions": [{
        "name": "web",
        "image": "nginx:alpine",
        "cpu": 256,
        "memory": 512,
        "essential": True,
        "portMappings": [{"containerPort": 80}]
    }]
}
print("ECS Task Definition validated:", task_def['family'])
```

---

## Use AWS
```bash
aws ecs create-cluster --cluster-name lab-cluster --tags Key=Project,Value=aws-from-scratch
```

---

## Inspect it
```bash
aws ecs describe-clusters --clusters lab-cluster --output table
```

---

## Measure it
Measure task replacement speed: kill task -> ECS registers death -> new task running (typically 10-20 seconds).

---

## Break it
Stop a running ECS task via `aws ecs stop-task`.

---

## Diagnose it
The task transitions to `STOPPED`; the ECS Service immediately launches a replacement task to restore desired count.

---

## Recover it
ECS handles recovery automatically without human intervention.

---

## Security
Assign separate `executionRoleArn` (for pulling images/secrets) and `taskRoleArn` (for app permissions).

---

## Cost
### Cost Warning
The ECS control plane is 100% free. You pay only for the compute capacity (EC2 or Fargate) executing the tasks.

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
aws ecs delete-cluster --cluster lab-cluster
```

---

## Verify cleanup
```bash
echo 'ECS cluster deleted.'
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-45-evidence.md`.

---

## Questions for mastery
1. What is the critical difference between an ECS Task and an ECS Service?
2. What happens if a non-essential container inside an ECS task crashes vs an essential container?
3. Why does ECS require two different IAM roles: Task Execution Role vs Task Role?

---

## When to use this
Use ECS for production container workloads where you want deep AWS integration without Kubernetes complexity.

---

## When not to use this
Do not use ECS if you require standard upstream Kubernetes APIs for multi-cloud portability (use EKS).

---

## What comes next
Phase 46: Fargate — Serverless container capacity.
