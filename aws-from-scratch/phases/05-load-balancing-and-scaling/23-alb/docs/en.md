# Phase 23: ALB

## Motto
> Listeners accept connections. Target Groups health check backends. Routing rules dispatch requests.

**Type:** Hands-on Lab & Managed Load Balancing  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 22: Load Balancing From Scratch  
**AWS Services Involved:** AWS Application Load Balancer (ALB)  
**Cost Vector:** ALB charges ~$0.0225/hour + $0.008 per LCU-hour. Delete immediately after testing!  

---

## Problem
Managing self-hosted HAProxy or Nginx servers requires managing their failover (VRRP/Keepalived), OS security patches, and capacity scaling.

---

## Prediction
An ALB provisions managed reverse-proxy nodes across multiple subnets, scaling horizontally automatically to handle millions of connections.

---

## Why this matters
ALB is the primary Layer 7 traffic routing primitive for EC2, ECS containers, and microservices in AWS.

---

## First principles
An ALB consists of: (1) **Listeners** (ports/protocols to listen on: HTTP 80, HTTPS 443), (2) **Rules** (path/host routing logic: `/api/*` -> Target Group B), and (3) **Target Groups** (logical pools of registered IP/instance targets with health check parameters).

---

## Mental model
```text
ALB Component Hierarchy:
[ Internet ] ──► [ ALB (Public Multi-AZ) ]
                         │
                         ▼
                  [ Listener: Port 443 ]
                         │
        ┌────────────────┴────────────────┐
        │ Path: /api/*                    │ Default Path: /*
        ▼                                 ▼
[ Target Group: API ]             [ Target Group: Web ]
• Health: /api/health             • Health: /health
• Targets: [Task 1, Task 2]       • Targets: [EC2-A, EC2-B]
```

---

## Architecture before AWS
F5 BIG-IP hardware pairs or Nginx Plus reverse proxy clusters.

---

## Build the primitive
```python
# Target Group Health Check Parameters
tg_config = {
    "HealthCheckProtocol": "HTTP",
    "HealthCheckPath": "/health",
    "HealthCheckIntervalSeconds": 30,
    "HealthyThresholdCount": 2,
    "UnhealthyThresholdCount": 2,
    "TargetResponseTimeoutSeconds": 5
}
print("ALB Health Configuration:", tg_config)
```

---

## Use AWS
```bash
aws elbv2 create-load-balancer --name lab-alb --subnets $PUB_SUBNET_1 $PUB_SUBNET_2 --security-groups $ALB_SG_ID --tag-specifications 'ResourceType=load-balancer,Tags=[{Key=Project,Value=aws-from-scratch}]'
```

---

## Inspect it
```bash
aws elbv2 describe-target-health --target-group-arn $TG_ARN --output table
```

---

## Measure it
Measure HTTP 502 Bad Gateway vs HTTP 504 Gateway Timeout behavior.

---

## Break it
Change the health check path from `/health` to `/nonexistent`.

---

## Diagnose it
All targets fail health checks (HTTP 404); ALB returns HTTP 503 Service Unavailable.

---

## Recover it
Restore the correct health check path.

---

## Security
Enforce HTTPS with ACM TLS certificates; set security group to accept traffic only from trusted sources.

---

## Cost
### Cost Warning
ALB charges ~$0.0225/hour + $0.008 per LCU-hour. Delete immediately after testing!

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
aws elbv2 delete-load-balancer --load-balancer-arn $ALB_ARN
```

---

## Verify cleanup
```bash
echo 'ALB deleted.'
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-23-evidence.md`.

---

## Questions for mastery
1. What is the difference between an HTTP 502 Bad Gateway and an HTTP 504 Gateway Timeout on an ALB?
2. Why must an ALB be deployed in at least two Availability Zones?
3. What is an LCU (Load Balancer Capacity Unit) and how is it calculated?

---

## When to use this
Use ALB for HTTP/HTTPS web applications, microservice path-based routing, and ECS container services.

---

## When not to use this
Do not use ALB for raw TCP/UDP workloads, gaming protocols, or VoIP (use Network Load Balancer).

---

## What comes next
Phase 24: Multi-AZ Application — Combining ALB and EC2 into a true fault-tolerant architecture.
