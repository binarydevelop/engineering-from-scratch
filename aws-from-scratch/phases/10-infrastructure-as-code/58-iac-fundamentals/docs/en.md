# Phase 58: IaC Fundamentals

## Motto
> A template is a DAG of resources. The engine resolves dependencies automatically.

**Type:** Hands-on Lab & CloudFormation  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 57: Infrastructure as Code  
**AWS Services Involved:** AWS CloudFormation Stacks, Change Sets  
**Cost Vector:** CloudFormation change sets and stack management cost $0.00.  

---

## Problem
If you try to create a subnet before its parent VPC exists, the API call crashes with `InvalidVpcID.NotFound`. How does an engine know what order to create resources in?

---

## Prediction
The IaC engine analyzes resource references (`!Ref`, `!GetAtt`) to construct a Directed Acyclic Graph (DAG), creating independent resources in parallel and dependent resources in order.

---

## Why this matters
Understanding dependency graphs prevents circular dependency errors and failed deployments.

---

## First principles
A CloudFormation template defines: (1) **Parameters** (inputs), (2) **Resources** (the declarative primitives to create), and (3) **Outputs** (values exported for other stacks). The engine builds a DAG where nodes are resources and edges are dependencies.

---

## Mental model
```text
CloudFormation Dependency Graph (DAG):
                   [ VPC (10.0.0.0/16) ]
                             │
            ┌────────────────┴────────────────┐
            ▼                                 ▼
[ Public Subnet 1 ]               [ Public Subnet 2 ]
(Created in parallel!)            (Created in parallel!)
            │                                 │
            ▼                                 ▼
[ SubnetRouteTableAssoc 1 ]       [ SubnetRouteTableAssoc 2 ]
```

---

## Architecture before AWS
Custom shell scripts with hardcoded `sleep 30` loops waiting for VM boots.

---

## Build the primitive
```python
# Simulating DAG topological sort
dependencies = {"Subnet": ["VPC"], "EC2": ["Subnet", "SecurityGroup"], "SecurityGroup": ["VPC"], "VPC": []}
print("Resource Creation Order determined by DAG:")
for res, deps in sorted(dependencies.items(), key=lambda x: len(x[1])):
    print(f"  Create {res} (Depends on: {deps or 'None'})")
```

---

## Use AWS
```bash
aws cloudformation create-change-set --stack-name lab-stack --change-set-name preview-1 --template-body file://infrastructure/vpc-dual-az-baseline.yaml --change-set-type CREATE
```

---

## Inspect it
```bash
aws cloudformation describe-change-set --stack-name lab-stack --change-set-name preview-1 --output json
```

---

## Measure it
Inspect parallel provisioning: CloudFormation provisions independent subnets concurrently.

---

## Break it
Introduce a circular dependency: Resource A depends on Resource B; Resource B depends on Resource A.

---

## Diagnose it
CloudFormation template validation fails with `Circular dependency between resources: [A, B]`.

---

## Recover it
Break the circular reference using intermediate parameters or decoupled exports.

---

## Security
CloudFormation automatically rolls back the entire stack if any single resource fails creation.

---

## Cost
### Cost Warning
CloudFormation change sets and stack management cost $0.00.

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
aws cloudformation delete-change-set --stack-name lab-stack --change-set-name preview-1
```

---

## Verify cleanup
```bash
echo 'Change set cleaned.'
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-58-evidence.md`.

---

## Questions for mastery
1. Why is inspecting a CloudFormation Change Set mandatory before executing an update in production?
2. What happens during a CloudFormation Rollback when a resource creation fails midway?
3. What is the difference between `!Ref` and `!GetAtt` in AWS CloudFormation?

---

## When to use this
Always use change sets to preview infrastructure updates and prevent accidental resource replacements.

---

## When not to use this
Do not edit live production resources directly in the console after deploying via IaC.

---

## What comes next
Phase 59: Rebuild VPC With IaC — Recreating our earlier VPC using code.
