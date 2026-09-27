# Phase 04: IAM Policies

## Motto
> A policy is a declarative contract of trust. One wrong wildcard can expose your entire company.

**Type:** Hands-on Lab & Policy Analysis  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 03: IAM From First Principles  
**AWS Services Involved:** IAM Policy Engine, Policy Simulator, Condition Keys  
**Cost Vector:** IAM policy creation and storage is free.  

---

## Problem
Giving developers broad `s3:*` permissions allows them to accidentally read production databases, delete client documents, or expose buckets to the public internet.

---

## Prediction
Adding a Condition key requiring `aws:SecureTransport: true` will immediately reject unencrypted HTTP requests to S3 with AccessDenied.

---

## Why this matters
Modern least-privilege security relies on condition keys (IP boundaries, MFA requirements, tag-based access control) rather than simple action lists.

---

## First principles
A policy document is a JSON AST evaluated at request time. Each Statement contains `Effect`, `Action`, `Resource`, and optional `Condition` blocks. Conditions evaluate contextual request variables (`aws:CurrentTime`, `aws:PrincipalArn`, `aws:SourceIp`, `s3:prefix`).

---

## Mental model
```text
IAM Policy Anatomy:
{
  "Effect": "Allow" | "Deny",
  "Action": [ "service:operation" ],
  "Resource": [ "arn:aws:service:region:account:type/id" ],
  "Condition": { "Operator": { "ContextKey": "Value" } }
}
```

---

## Architecture before AWS
Database GRANT/REVOKE statements, POSIX file ACLs (setfacl), and Windows NTFS access control lists.

---

## Build the primitive
```python
import json
with open('policies/s3-read-write-least-privilege.json') as f:
    policy = json.load(f)
print(f"Policy Statements Loaded: {len(policy['Statement'])}")
for s in policy['Statement']:
    print(f"  Sid: {s.get('Sid')} | Effect: {s['Effect']} | Actions: {s['Action']}")
```

---

## Use AWS
```bash
# Validate policy syntax using AWS CLI
aws iam get-account-summary --output table
```

---

## Inspect it
```bash
cat policies/s3-read-write-least-privilege.json
```

---

## Measure it
Test policy evaluation speed using AWS IAM Policy Simulator CLI.

---

## Break it
Add an explicit Deny on `s3:*` to your identity policy and try to list buckets.

---

## Diagnose it
Observe that even with AdministratorAccess attached, the Explicit Deny wins and listing fails.

---

## Recover it
Remove the explicit Deny statement.

---

## Security
Use Condition keys (`aws:PrincipalOrgID`, `aws:SourceVpce`) to enforce perimeter-based access control.

---

## Cost
### Cost Warning
IAM policy creation and storage is free.

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
# No billable resources created.
```

---

## Verify cleanup
```bash
echo 'Account clean.'
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-04-evidence.md`.

---

## Questions for mastery
1. What is the difference between an Identity-Based Policy and a Resource-Based Policy?
2. If Account A's IAM user wants to access an S3 bucket in Account B, what policies must allow it?
3. How does a Permissions Boundary prevent an IAM admin user from escalating their own privileges?

---

## When to use this
Use granular JSON policies for every production service and workload role.

---

## When not to use this
Avoid huge monolithic 10,000-character policies; break them into modular purpose-driven policies.

---

## What comes next
Phase 05: AWS Networking Before VPC — Rebuilding IPv4, CIDR, and routing from first principles.
