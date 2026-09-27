# Phase 40: Lambda Lifecycle

## Motto
> A cold start initializes the execution environment. A warm invoke reuses it. Design for container reuse.

**Type:** Systems Experiment & Lifecycle Measurement  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 39: Lambda From First Principles  
**AWS Services Involved:** Lambda Execution Environment, Cold Starts, Provisioned Concurrency  
**Cost Vector:** Init Duration is billed under standard Lambda pricing.  

---

## Problem
The first HTTP request to a serverless API experiences a 500ms latency spike, while subsequent requests take only 12ms. What is happening under the hood?

---

## Prediction
The initial invocation must download code, boot the micro-VM, and run static initialization (Cold Start). Subsequent invocations reuse the warm execution environment.

---

## Why this matters
Understanding cold vs warm execution environments prevents creating new database connection pools on every single request.

---

## First principles
The Lambda execution lifecycle has three phases: (1) `INIT`: Download code, start micro-VM, initialize runtime, run code outside handler. (2) `INVOKE`: Run handler function. (3) `SHUTDOWN`: Freeze environment for potential reuse; terminate if idle for 5-15 minutes.

---

## Mental model
```text
Lambda Execution Environment Lifecycle:
Phase 1: INIT (Cold Start Only)
[ Boot Micro-VM ] ──► [ Load Runtime ] ──► [ Run Static Code (Imports / DB Pool) ]
                                                   │
                                                   ▼
Phase 2: INVOKE (Fast Warm Execution)
               ┌───────────────────────────────────┤
               ▼                                   ▼
        [ First Invoke ]                   [ Subsequent Warm Invokes ]
        Handler runs (500ms total)         Handler runs (12ms total!)
```

---

## Architecture before AWS
FastCGI process pools or preforking Apache worker processes.

---

## Build the primitive
```python
# Demonstrating global state reuse in Lambda
import time
init_timestamp = time.time() # Runs ONCE during INIT phase
def lambda_handler(event, context):
    return {
        "init_time": init_timestamp,
        "invoke_time": time.time(),
        "is_warm": (time.time() - init_timestamp) > 0.1
    }
print(lambda_handler({}, None))
time.sleep(0.5)
print(lambda_handler({}, None)) # Warm invoke shares init_timestamp!
```

---

## Use AWS
```bash
aws lambda invoke --function-name lab-hello --log-type Tail out.json --query 'LogResult' --output text | base64 --decode
```

---

## Inspect it
```bash
cat out.json
```

---

## Measure it
Compare REPORT lines: Cold start contains `Init Duration: 185.42 ms`; warm invoke has zero Init Duration.

---

## Break it
Initialize a heavy 500MB machine learning model inside the `lambda_handler` function on every request.

---

## Diagnose it
Every request suffers a 2-second penalty; memory usage spikes and database connections exhaust.

---

## Recover it
Move initialization outside the handler into global scope so it executes only during the INIT phase.

---

## Security
Because warm environments are reused, never store client-specific sensitive state in global variables.

---

## Cost
### Cost Warning
Init Duration is billed under standard Lambda pricing.

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
# No additional resources created.
```

---

## Verify cleanup
```bash
echo 'Account clean.'
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-40-evidence.md`.

---

## Questions for mastery
1. Why is Python/Node.js cold start latency significantly faster than Java/JVM cold start latency in Lambda?
2. What is Provisioned Concurrency and how does it guarantee zero cold starts for latency-critical APIs?
3. Can two concurrent requests share the exact same Lambda execution environment simultaneously?

---

## When to use this
Use global scope for static caching, database connection pooling, and SDK client initialization.

---

## When not to use this
Do not assume an execution environment will ever be reused; Lambda can kill it at any time.

---

## What comes next
Phase 41: API Gateway + Lambda — Exposing serverless functions over public HTTPS.
