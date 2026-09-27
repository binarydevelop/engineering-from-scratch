# Phase 57: Infrastructure as Code

## Motto
> Clicking in the console is for discovery. Infrastructure as Code is for production. If it isn't in code, it doesn't exist.

**Type:** Conceptual & Paradigm Transition  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 11: Security Groups  
**AWS Services Involved:** Declarative Infrastructure, AWS CloudFormation, Terraform  
**Cost Vector:** AWS CloudFormation is free. You pay only for the resources it provisions.  

---

## Problem
You spent 4 days clicking in the AWS console to set up a VPC, subnets, route tables, security groups, ALBs, and instances. The CTO asks: 'Can you reproduce this exact setup in `eu-central-1` for our European customers?' You have no documentation, no reproducibility, and configuration drift.

---

## Prediction
Writing infrastructure declaratively in text files allows version-controlling environments with Git, reviewing changes via Pull Requests, and deploying identical infrastructure across regions in minutes.

---

## Why this matters
Only after feeling the pain of manual creation in Phases 06-16 do we introduce IaC. You must understand the underlying resources before automating them.

---

## First principles
Imperative (CLI/Scripts): 'Create VPC A, then create Subnet B, then attach Gateway C.' Fragile; fails midway without state tracking. Declarative (IaC): 'I want a VPC with CIDR 10.0.0.0/16 and two subnets.' The IaC engine computes the dependency graph and reconciles desired state against current state.

---

## Mental model
```text
Imperative vs Declarative Infrastructure:
IMPERATIVE (Bash / CLI):
Step 1 ──► Step 2 ──► Step 3 (Fails halfway! Left in dirty state!)

DECLARATIVE (CloudFormation / Terraform):
[ Declarative Code ] ──► [ Graph Engine computes DAG ] ──► [ Reconciles to AWS APIs ]
                                                                 (Idempotent & Safe!)
```

---

## Architecture before AWS
Datacenter runbooks: 40-page Word documents detailing cable numbers and manual BIOS settings.

---

## Build the primitive
```python
# Simulating declarative state reconciliation
desired_state = {"vpc_cidr": "10.0.0.0/16", "subnets": 2}
current_state = {"vpc_cidr": "10.0.0.0/16", "subnets": 1}
plan = {}
for k, v in desired_state.items():
    if current_state.get(k) != v:
        plan[k] = f"CREATE/UPDATE from {current_state.get(k)} to {v}"
print("Execution Plan computed by IaC Engine:", plan)
```

---

## Use AWS
```bash
# Validate CloudFormation template syntax CLI
aws cloudformation validate-template --template-body file://infrastructure/vpc-dual-az-baseline.yaml --output table
```

---

## Inspect it
```bash
cat infrastructure/vpc-dual-az-baseline.yaml
```

---

## Measure it
Compare reproduction time: Manual console recreation (3 hours) vs automated IaC execution (3 minutes).

---

## Break it
Manually delete a subnet in the AWS console that is managed by an active CloudFormation stack.

---

## Diagnose it
The stack experiences **Configuration Drift**: desired state no longer matches physical cloud reality.

---

## Recover it
Run CloudFormation Drift Detection and re-import or update the stack.

---

## Security
IaC allows scanning infrastructure for security misconfigurations (e.g. `checkov`, `trivy`) in CI/CD before resources are created.

---

## Cost
### Cost Warning
AWS CloudFormation is free. You pay only for the resources it provisions.

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
# No resources created in Phase 57.
```

---

## Verify cleanup
```bash
echo 'Account clean.'
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-57-evidence.md`.

---

## Questions for mastery
1. Why is declarative infrastructure superior to writing shell scripts with the AWS CLI?
2. What is configuration drift and how does an IaC engine detect it?
3. Why did we mandate manual CLI/API configuration in Phases 06-16 before introducing IaC here?

---

## When to use this
Use Infrastructure as Code for all non-trivial cloud resources, pipelines, and environments.

---

## When not to use this
Do not use IaC for transient 5-minute exploratory prototyping where quick deletion is planned.

---

## What comes next
Phase 58: IaC Fundamentals — Stacks, parameters, outputs, and dependencies.
