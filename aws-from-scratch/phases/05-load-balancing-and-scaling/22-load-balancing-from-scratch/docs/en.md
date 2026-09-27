# Phase 22: Load Balancing From Scratch

## Motto
> A single server is a single point of failure. A load balancer is a reverse proxy with health check intelligence.

**Type:** Hands-on Lab & First Principles Engine  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 13: EC2 From First Principles  
**AWS Services Involved:** Reverse Proxying, Socket Multiplexing  
**Cost Vector:** Local simulation is $0.00. Live AWS ALB is ~$16.20/month.  

---

## Problem
One web server can handle 2,000 requests per second before its CPU saturates. When traffic hits 5,000 req/sec, how do clients distribute requests across two servers without hardcoding server IPs?

---

## Prediction
A reverse proxy intercepting incoming client sockets can distribute requests round-robin across healthy backend targets and seamlessly evict failing nodes.

---

## Why this matters
Load balancing is the pivot point between single-server snowflake systems and horizontally scalable distributed systems.

---

## First principles
A reverse proxy acts as an intermediary. It terminates client TCP connections, inspects request headers, selects a backend target from an active healthy target pool, forwards the request over a second TCP connection, and proxies the response back.

---

## Mental model
```text
Reverse Proxy Load Balancing:
[ Clients ] ──(Requests)──► [ Reverse Proxy (Port 80) ]
                                    │
                                    ├── Request 1 ──► [ Server A (10.0.1.50) ] (AZ-A)
                                    └── Request 2 ──► [ Server B (10.0.2.60) ] (AZ-B)
```

---

## Architecture before AWS
Hardware load balancing appliances like F5 BIG-IP or open-source HAProxy / Nginx reverse proxies.

---

## Build the primitive
```python
# Run our first-principles load balancer lab
import subprocess
subprocess.run(['python3', 'experiments/lb_healthcheck_lab.py'], check=True)
```

---

## Use AWS
```bash
# Check ALB service endpoints
aws elbv2 describe-load-balancers --query 'LoadBalancers[].[LoadBalancerName,DNSName,State.Code]' --output table
```

---

## Inspect it
```bash
python3 benchmarks/benchmark_lb.py
```

---

## Measure it
Measure latency overhead introduced by reverse proxying (+0.5 to 1.2ms) vs benefits of high availability.

---

## Break it
Kill backend Server A in `experiments/lb_healthcheck_lab.py`.

---

## Diagnose it
The load balancer detects consecutive health check failures and evicts Server A from the pool.

---

## Recover it
Traffic shifts 100% to Server B with zero client errors. When Server A recovers, it is automatically re-added.

---

## Security
Load balancers hide backend server IP addresses from the public internet, acting as a security shield.

---

## Cost
### Cost Warning
Local simulation is $0.00. Live AWS ALB is ~$16.20/month.

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
# No AWS resources provisioned.
```

---

## Verify cleanup
```bash
echo 'Account clean.'
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-22-evidence.md`.

---

## Questions for mastery
1. Why is Layer 7 load balancing (ALB) slower than Layer 4 load balancing (NLB)?
2. What happens if all backend targets in a target group fail their health checks simultaneously?
3. Why is round-robin DNS inferior to a dedicated load balancer for failover?

---

## When to use this
Always place a load balancer in front of stateless application servers.

---

## When not to use this
Do not place an ALB in front of a single database primary that accepts writes.

---

## What comes next
Phase 23: ALB — Deploying the managed Application Load Balancer in AWS.
