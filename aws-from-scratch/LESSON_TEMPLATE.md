# Lesson Template

Every lesson in `aws-from-scratch` must follow this structure. Copy this file into your lesson directory at `phases/<phase>/<lesson>/docs/en.md` and complete every section.

Do not skip sections. If a section is not applicable to a purely conceptual lesson, explicitly document why rather than omitting the heading.

---

# [Phase-Lesson Number]: [Lesson Title]

## Motto
> [One-line motto summarizing the first-principles realization of this lesson]

**Type:** Conceptual | Hands-on Lab | Systems Experiment | Architecture Project  
**Time Estimate:** ~[X] minutes  
**Prerequisites:** [List prior lessons or concepts required]  
**AWS Services Involved:** [List relevant AWS primitives/services]  
**Cost Vector:** Free / Local Simulation / Billable (~$0.0X/hr while running)  

---

## Problem
*What real-world engineering problem forces this infrastructure need?*
Describe the concrete failure, bottleneck, or requirement that occurs when this infrastructure does not exist. (e.g., "Server A saturates because clients make synchronous HTTP calls directly to it.")

---

## Prediction
*Before running any code or provisioning any resource, formulate an explicit hypothesis.*
1. What do you expect will happen when traffic spikes or a component fails?
2. What network route or authorization rule do you expect will succeed or fail?
3. What metrics or logs do you expect to observe?

---

## Why this matters
Explain the production consequences of misunderstanding this concept. Show how treating this component as a black box leads to downtime, security vulnerabilities, or unbounded cloud spend.

---

## First principles
Derive the solution from computer science and physics fundamentals:
- Processes, memory, and sockets
- Network routing, CIDR blocks, and packet headers
- Storage media, block boundaries, and I/O operations
- Distributed consensus, synchronous vs asynchronous communication

---

## Mental model
Provide an ASCII diagram illustrating the underlying system dynamics, traffic paths, state locations, and isolation boundaries:

```text
[ Client ] ──(Request)──► [ Primitive Component ] ──(Process)──► [ Storage/State ]
```

---

## Architecture before AWS
How did software systems solve this problem before cloud APIs existed?
(e.g., Physical server in a rack, physical patch cable, software proxy like HAProxy/Nginx, on-prem tape backup).

---

## Build the primitive
Implement a minimal, working version of the primitive locally in Python or bash (e.g., a local reverse proxy, an in-memory queue, or a simple IAM policy evaluator).

```python
# Minimal runnable primitive demonstrating the core mechanism
```

---

## Use AWS
Show how AWS exposes this primitive as an API and managed resource. Provide explicit AWS CLI commands or declarative configurations.

```bash
# Explicit, non-destructive AWS CLI commands with required lab tags
aws ... \
  --tags Key=Project,Value=aws-from-scratch Key=Lesson,Value=lesson-id
```

---

## Inspect it
Do not assume AWS did what you asked. Interrogate the control plane and data plane:
- Check resource state via CLI queries (`--query` and `--output table`)
- Trace IP addresses, routing tables, and security group associations
- Inspect response headers and HTTP status codes

---

## Measure it
Quantify system behavior with real numbers:
- Latency (p50, p95, p99 via `curl -w` or benchmark tools)
- Throughput (requests/sec)
- CPU / Memory utilization
- Queue depth / message age

---

## Break it
Intentionally inject failure to observe the system under stress:
- Kill a process or instance
- Restrict an IAM policy to trigger `AccessDenied`
- Block an inbound port in a Security Group
- Induce network latency or partition

---

## Diagnose it
Follow a systematic diagnostic tree:
1. What was the exact error message or symptom?
2. What log stream, metric, or status check revealed the root cause?
3. How do you distinguish between network failure, authorization failure, and application failure?

---

## Recover it
Demonstrate the recovery mechanism:
- Health check eviction and traffic rerouting
- Dead-letter queue inspection and redrive
- IAM policy correction
- Automated healing or instance replacement

---

## Security
Analyze this component across the security pillar:
- Who is authenticated? What principal is authorized?
- What network perimeter or security group isolates it?
- Is data encrypted at rest and in transit?
- Does this violate least privilege?

---

## Cost
Analyze this component across the cost pillar:
- **Billing Metric:** Hourly compute / provisioned IOPS / per-request / data egress?
- **Idle Cost:** Does this charge money when zero traffic flows?
- **Surprise Factor:** What traffic pattern could cause an unexpected spike in cost?
- **Cheaper Alternative:** Can this be solved with a simpler or serverless primitive?

---

## Modify it
Extend or tune the configuration:
- Adjust timeout or retry policies
- Scale capacity up or down
- Introduce caching or compression

---

## Cleanup
The exact commands to terminate, delete, and release every cloud resource created during this lesson:

```bash
# Step 1: Terminate compute / services
aws ... delete-...

# Step 2: Delete networking / dependencies
aws ... delete-...
```

---

## Verify cleanup
The exact commands to verify that zero billable or orphaned resources remain:

```bash
# Must return empty output
aws ... describe-... --query '...'
```

---

## Evidence
Record your laboratory findings using the Evidence Template (`outputs/evidence-template.md`).

---

## Questions for mastery
Deep reasoning questions that require understanding tradeoffs rather than memorizing terminology:
1. *Scenario Question:* If X fails while Y is saturated, what happens to Z?
2. *Tradeoff Question:* Why would you choose A instead of B in this specific constraint?
3. *Failure Mode Question:* What is the silent failure mode of this design?

---

## When to use this
Clear criteria for when this AWS primitive/service is the right tool for the job.

---

## When not to use this
Anti-patterns and scenarios where this service is an over-engineered, overly expensive, or inappropriate choice.

---

## What comes next
Connect this lesson to the next infrastructure primitive in the curriculum.
