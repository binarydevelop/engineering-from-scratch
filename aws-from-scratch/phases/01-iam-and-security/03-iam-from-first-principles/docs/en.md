# Phase 03: IAM From First Principles

## Motto
> Identity is cryptographic proof of who you are. Authorization is boolean logic determining what you can do.

**Type:** Hands-on Lab & First Principles Engine  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 02: AWS CLI, APIs, and Console  
**AWS Services Involved:** AWS IAM, AWS STS  
**Cost Vector:** AWS IAM is a foundational control plane service offered at zero charge.  

---

## Problem
When microservices or developers share hardcoded root credentials, any leak grants full destructive access to the entire AWS account. There is no auditability of who deleted a database.

---

## Prediction
A request without an explicit Allow will evaluate to Default Deny and immediately fail with HTTP 403 AccessDenied.

---

## Why this matters
IAM is the single most critical security primitive in AWS. Every single API call is evaluated against IAM authorization boundaries.

---

## First principles
Authorization is a boolean reduction function: `evaluate(Principal, Action, Resource, Context) -> {ALLOW, DENY}`. By default, access is closed (Default Deny). An explicit Allow opens access. Any explicit Deny immediately terminates evaluation with rejection.

---

## Mental model
```text
IAM Evaluation Precedence:
[ API Request ] ──► Any Matching Explicit Deny? ──YES──► [ REJECT: DENIED ]
                           │ NO
                           ▼
                    Any Matching Explicit Allow? ──NO──► [ REJECT: DENIED (Default) ]
                           │ YES
                           ▼
                    [ AUTHORIZED: ALLOW ]
```

---

## Architecture before AWS
UNIX sudoers files, LDAP/Active Directory groups, and Kerberos ticket-granting services.

---

## Build the primitive
```python
# Run our first-principles IAM evaluator simulation
import subprocess
subprocess.run(['python3', 'experiments/iam_simulator.py'], check=True)
```

---

## Use AWS
```bash
aws iam get-user || aws sts get-caller-identity
```

---

## Inspect it
```bash
aws iam list-roles --max-items 5 --output table
```

---

## Measure it
Measure STS token assumption latency (`aws sts assume-role`).

---

## Break it
Attempt an action not granted by your policy (e.g., `aws dynamodb list-tables`).

---

## Diagnose it
Inspect the error: 'User is not authorized to perform: dynamodb:ListTables on resource: *'.

---

## Recover it
Attach a scoped policy granting `dynamodb:ListTables` to the identity.

---

## Security
Never grant `*` permissions. Always scope actions and resource ARNs to the minimum needed.

---

## Cost
### Cost Warning
AWS IAM is a foundational control plane service offered at zero charge.

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
# No billable resources created in Phase 03.
```

---

## Verify cleanup
```bash
echo 'Account clean.'
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-03-evidence.md`.

---

## Questions for mastery
1. Why does an Explicit Deny statement in an SCP override an Explicit Allow in an IAM User policy?
2. What is the difference between an IAM User and an IAM Role?
3. Why are temporary credentials (`ASIA...`) cryptographically safer than permanent access keys (`AKIA...`)?

---

## When to use this
Always use IAM Roles for applications running on EC2, ECS, and Lambda.

---

## When not to use this
Never create IAM Users with permanent access keys for workload-to-workload communication.

---

## What comes next
Phase 04: IAM Policies — Constructing granular JSON policies and condition keys.
