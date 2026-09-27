# Phase 81: Build a Tiny Cloud Simulator

## Motto
> The cloud is not magic: it is ordinary software exposing hardware primitives over HTTP APIs. Let's build one.

**Type:** Capstone 1 & Systems Software  
**Time Estimate:** ~120 minutes  
**Prerequisites:** Phase 02: AWS CLI, APIs, and Console  
**AWS Services Involved:** VM Registry, Object Storage, Load Balancer, Queue, IAM Engine  
**Cost Vector:** 100% Free ($0.00). Runs entirely on your local machine.  

---

## Problem
Engineers treat AWS services as proprietary black magic because they have never seen how simple the underlying software abstractions are.

---

## Prediction
Building a working mini-cloud in pure Python (VMRegistry, ObjectStorage, LoadBalancer, MessageQueue) proves that cloud APIs are clean software wrappers over computer science primitives.

---

## Why this matters
This is Capstone 1: the ultimate demystification of cloud computing.

---

## First principles
Every cloud service exposes standard CRUD APIs over an internal state machine: EC2 maintains an instance state dictionary; S3 maintains a hash table of byte arrays; SQS maintains an in-memory queue with visibility timers; ALB maintains a list of target IPs and probes health checks.

---

## Mental model
```text
Capstone 1: Tiny Cloud Simulator:
┌────────────────────────────────────────────────────────┐
│ TinyCloud API Facade (`projects/.../tiny_cloud.py`)    │
├───────────────────┬────────────────────────────────────┤
│ Service Primitive │ Internal Data Structure            │
├───────────────────┼────────────────────────────────────┤
│ cloud.run_vm()    │ Dict[str, Instance] (State Machine)│
│ cloud.put_object()│ Dict[str, S3Object] (Hash Table)   │
│ cloud.forward()   │ Reverse Proxy + Health Check Loop  │
│ cloud.send_msg()  │ List[Message] + Visibility Timers  │
│ cloud.evaluate()  │ Boolean Policy Reduction Engine    │
└───────────────────┴────────────────────────────────────┘
```

---

## Architecture before AWS
Developing internal private cloud management tools like OpenStack or CloudStack.

---

## Build the primitive
```python
# Run our complete Tiny Cloud Simulator (Capstone 1)
import subprocess
subprocess.run(['python3', 'projects/project-07-tiny-cloud-simulator/tiny_cloud.py'], check=True)
```

---

## Use AWS
```bash
# Local capstone execution: make test-simulators
```

---

## Inspect it
```bash
python3 projects/project-07-tiny-cloud-simulator/tiny_cloud.py
```

---

## Measure it
Measure simulation execution speed: provisioning 2 VMs, writing S3 objects, and routing traffic completes in < 5ms!

---

## Break it
Stop all backend targets in the Tiny Cloud load balancer.

---

## Diagnose it
The simulator returns `HTTP 503 Service Unavailable: No healthy targets`—exactly like a real AWS ALB!

---

## Recover it
Launch a new running instance in the simulator.

---

## Security
Our simulated IAM policy engine evaluates Explicit Deny > Allow > Default Deny.

---

## Cost
### Cost Warning
100% Free ($0.00). Runs entirely on your local machine.

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
cloud.terminate_instances() automatically cleans local state.
```

---

## Verify cleanup
```bash
python3 -m unittest discover -s tests -p 'test_simulators.py'
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-81-evidence.md`.

---

## Questions for mastery
1. How does building a local object store demystify S3's lack of true filesystem directories?
2. How does our simulated load balancer mirror the exact health check eviction mechanics of an AWS ALB?
3. Why is an SQS message queue fundamentally different from a simple Python list in terms of visibility timeouts?

---

## When to use this
Use Capstone 1 to build deep intuition for how cloud control planes and data planes operate.

---

## When not to use this
This is an educational simulator: do not use it as a production cloud runtime!

---

## What comes next
Phase 82: Production-Like AWS Capstone — Capstone 2: Comprehensive enterprise cloud synthesis.
