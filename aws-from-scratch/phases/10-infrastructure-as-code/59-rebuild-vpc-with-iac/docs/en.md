# Phase 59: Rebuild VPC With IaC

## Motto
> Automate what you have understood. Turn hours of manual networking into a 3-minute template deployment.

**Type:** Hands-on Lab & Network Automation  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 58: IaC Fundamentals  
**AWS Services Involved:** CloudFormation, VPC, Subnets, Route Tables, IGW  
**Cost Vector:** This Dual-AZ baseline VPC incurs exactly $0.00/month while idle because it avoids expensive NAT Gateways.  

---

## Problem
In Phases 06 through 10, we manually created a VPC, attached an Internet Gateway, created subnets across 2 AZs, and configured route tables. Doing this manually takes 20 CLI commands and is prone to typos.

---

## Prediction
Deploying `infrastructure/vpc-dual-az-baseline.yaml` will provision the entire multi-AZ network in under 2 minutes with zero human error.

---

## Why this matters
Comparing the pain of manual learning in Phase 06 vs automated reproducibility in Phase 59 proves the value of IaC.

---

## First principles
The CloudFormation template `infrastructure/vpc-dual-az-baseline.yaml` defines the VPC, IGW attachment, 2 public subnets, 2 private subnets, and route associations as code. It provisions a production-ready network with ZERO ongoing hourly NAT Gateway costs.

---

## Mental model
```text
Template Architecture:
infrastructure/vpc-dual-az-baseline.yaml
  ├── AWS::EC2::VPC (10.0.0.0/16)
  ├── AWS::EC2::InternetGateway
  ├── AWS::EC2::Subnet (Public AZ-1, Public AZ-2)
  ├── AWS::EC2::Subnet (Private AZ-1, Private AZ-2)
  └── AWS::EC2::RouteTable (Default Route 0.0.0.0/0 -> IGW)
```

---

## Architecture before AWS
Network cabling diagrams and manual switch VLAN configuration.

---

## Build the primitive
```python
# Inspect our validated baseline template
with open('infrastructure/vpc-dual-az-baseline.yaml') as f:
    lines = [line.strip() for line in f if 'Type: AWS::EC2::' in line]
print(f"Template contains {len(lines)} declarative networking primitives:")
for l in lines: print(f"  - {l}")
```

---

## Use AWS
```bash
aws cloudformation deploy --template-file infrastructure/vpc-dual-az-baseline.yaml --stack-name aws-from-scratch-vpc --parameter-overrides ProjectName=aws-from-scratch
```

---

## Inspect it
```bash
aws cloudformation describe-stacks --stack-name aws-from-scratch-vpc --query 'Stacks[0].Outputs' --output table
```

---

## Measure it
Measure deployment duration: complete Dual-AZ VPC deploys in ~45 seconds.

---

## Break it
Attempt to delete the stack while an active EC2 instance is still running in one of the subnets.

---

## Diagnose it
Stack deletion halts with `DELETE_FAILED: Subnet has dependent network interfaces (ENIs)`.

---

## Recover it
Terminate the EC2 instance first, then retry stack deletion.

---

## Security
The template keeps private subnets completely dark to the public internet.

---

## Cost
### Cost Warning
This Dual-AZ baseline VPC incurs exactly $0.00/month while idle because it avoids expensive NAT Gateways.

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
aws cloudformation delete-stack --stack-name aws-from-scratch-vpc
```

---

## Verify cleanup
```bash
aws cloudformation wait stack-delete-complete --stack-name aws-from-scratch-vpc
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-59-evidence.md`.

---

## Questions for mastery
1. Why did we intentionally omit a NAT Gateway from `infrastructure/vpc-dual-az-baseline.yaml`?
2. How does `!Select [0, !GetAZs '']` make CloudFormation templates portable across any AWS region?
3. How would you update the template to add a third Availability Zone?

---

## When to use this
Use this baseline VPC template as the starting network foundation for all your learning projects.

---

## When not to use this
Do not delete and recreate VPCs in production environments where IP addresses are referenced by client firewalls.

---

## What comes next
Phase 60: Rebuild Application Stack With IaC — Deploying compute and databases via code.
