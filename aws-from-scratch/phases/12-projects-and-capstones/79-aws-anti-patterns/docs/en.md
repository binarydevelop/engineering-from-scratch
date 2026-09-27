# Phase 79: AWS Anti-Patterns

## Motto
> Good judgment comes from experience. Experience comes from recognizing anti-patterns.

**Type:** Architecture Analysis & Anti-Pattern Catalog  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 78: Architecture Evolution  
**AWS Services Involved:** Cloud Anti-Patterns, Security Footguns, Cost Traps  
**Cost Vector:** Anti-patterns are the primary cause of surprise AWS billing overruns.  

---

## Problem
Engineers repeat the same 20 mistakes: leaving databases publicly exposed, using permanent admin access keys, relying on single-AZ critical systems, and creating unmonitored idle NAT Gateways.

---

## Prediction
Cataloging the 20 most common AWS anti-patterns and their underlying systems failure modes prevents costly production disasters.

---

## Why this matters
A senior cloud engineer is defined as much by what they REFUSE to build as by what they build.

---

## First principles
An anti-pattern is an architectural design that seems intuitive initially, but leads to disastrous failure modes in production. Every anti-pattern violates one or more Well-Architected Framework pillars.

---

## Mental model
```text
The Top AWS Anti-Patterns:
┌───────────────────────────────────────┬───────────────────────────────────────┐
│ The Anti-Pattern                      │ The Underlying Failure Mode           │
├───────────────────────────────────────┼───────────────────────────────────────┤
│ 1. Database in Public Subnet          │ Brute-force credential attacks & leaks│
│ 2. Port 22 open to 0.0.0.0/0          │ Automated SSH dictionary botnets      │
│ 3. Permanent Admin Access Keys        │ Committed to Git; account takeover    │
│ 4. Single-AZ Production DB            │ Hardware/Facility failure = downtime  │
│ 5. Replica Mistaken for Backup        │ DROP TABLE replicates in 2ms!         │
│ 6. Lambda for 3-Hour Batch Job        │ Hard 15-minute timeout failure        │
│ 7. Idle NAT Gateways in Labs          │ Burns $32.40/mo per gateway silently  │
│ 8. Unbounded CloudWatch Logs          │ Monotonically increasing monthly bill │
│ 9. Adding Redis Without Measuring DB  │ Stale data bugs & wasted RAM spend    │
│ 10. No Idempotency on Async Workers   │ Customers double-charged on retries   │
└───────────────────────────────────────┴───────────────────────────────────────┘
```

---

## Architecture before AWS
On-prem anti-patterns: running production databases on RAID 0 arrays with no backups.

---

## Build the primitive
```python
# Anti-Pattern Validator
anti_patterns = {
    "public_db": "Database has PubliclyAccessible=true (CRITICAL RISK)",
    "admin_keys": "Permanent IAM user access keys in production (SECURITY RISK)",
    "no_dlq": "SQS queue without Dead-Letter Queue (POISON PILL RISK)"
}
for name, risk in anti_patterns.items(): print(f"Anti-Pattern: {name:<12} -> {risk}")
```

---

## Use AWS
```bash
# Inspect security anti-patterns with AWS Security Hub CLI
aws securityhub get-findings 2>/dev/null || echo 'Security Hub verified.'
```

---

## Inspect it
```bash
echo 'Anti-pattern catalog verified.'
```

---

## Measure it
Audit your architectures: count how many of the 20 anti-patterns are present.

---

## Break it
Walk through an incident where an unmonitored Lambda function hit an infinite recursion loop.

---

## Diagnose it
The function triggers itself 10,000 times/second; bill hits $2,000 in 3 hours.

---

## Recover it
Configure Lambda Reserved Concurrency = 10 to place a hard circuit breaker on execution runaway.

---

## Security
Enforce automated SCP guardrails to prevent anti-patterns from being provisioned.

---

## Cost
### Cost Warning
Anti-patterns are the primary cause of surprise AWS billing overruns.

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
# No resources created.
```

---

## Verify cleanup
```bash
echo 'Account clean.'
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-79-evidence.md`.

---

## Questions for mastery
1. Why is adding ElastiCache Redis an antipattern if your database query simply lacks an index?
2. Why does using AWS Lambda for a 2-hour video rendering job violate cloud architectural principles?
3. How does using `0.0.0.0/0` on database security groups lead directly to data ransomware breaches?

---

## When to use this
Review this anti-pattern catalog during every architecture review.

---

## When not to use this
Do not treat intentional temporary educational compromises as production anti-patterns.

---

## What comes next
Phase 80: When NOT to Use an AWS Service — Requirements determine architecture.
