# Phase 06: Build a VPC From First Principles

## Motto
> A VPC is not a physical box: it is a private overlay network carved out of AWS's global hypervisor fabric.

**Type:** Hands-on Lab & Network Construction  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 05: AWS Networking Before VPC  
**AWS Services Involved:** Amazon VPC API  
**Cost Vector:** VPCs are completely free. You can create up to 5 VPCs per region with zero ongoing charges.  

---

## Problem
Relying on the AWS 'Default VPC' puts your production databases and backend servers into public subnets with default internet gateways, violating isolation principles.

---

## Prediction
Creating a custom VPC will create a virtual network with a default Route Table and a default Security Group, but zero subnets and zero internet connectivity.

---

## Why this matters
Every AWS workload lives inside a VPC. Understanding how to construct one from scratch without wizard defaults gives you total mastery over cloud network boundaries.

---

## First principles
A Virtual Private Cloud (VPC) is a logically isolated virtual network partition. Under the hood, AWS uses software-defined networking encapsulation protocols (Geneve / VXLAN) running on AWS Nitro network ASIC cards to tunnel private packets across physical datacenter fiber without cross-tenant interference.

---

## Mental model
```text
VPC Boundary:
AWS Region (us-east-1)
┌────────────────────────────────────────────────────────┐
│ Amazon VPC (CIDR: 10.0.0.0/16)                         │
│ • Completely isolated from other AWS accounts          │
│ • Completely isolated from the public internet         │
│ • Main Route Table (10.0.0.0/16 -> local)              │
│ • Default Security Group (Deny inbound from outside)   │
└────────────────────────────────────────────────────────┘
```

---

## Architecture before AWS
Network engineers provisioned isolated VLANs and configured virtual routing and forwarding (VRF) instances on physical core routers.

---

## Build the primitive
```python
# Template reference for custom VPC
print("VPC Architecture Specification:")
print("  VpcCIDR: 10.0.0.0/16")
print("  DNS Hostnames: Enabled")
print("  DNS Resolution: Enabled")
```

---

## Use AWS
```bash
aws ec2 create-vpc --cidr-block 10.0.0.0/16 --tag-specifications 'ResourceType=vpc,Tags=[{Key=Project,Value=aws-from-scratch},{Key=Lesson,Value=06-vpc}]' --output json
```

---

## Inspect it
```bash
aws ec2 describe-vpcs --filters 'Name=tag:Project,Values=aws-from-scratch' --output table
```

---

## Measure it
Inspect the default main route table automatically generated for your new VPC.

---

## Break it
Disable DNS hostnames and DNS resolution on the VPC and observe how internal service discovery breaks.

---

## Diagnose it
Instances fail to resolve internal AWS DNS names like `ip-10-0-1-50.ec2.internal`.

---

## Recover it
Run `aws ec2 modify-vpc-attribute --vpc-id <id> --enable-dns-hostnames`.

---

## Security
A newly created VPC has zero internet connectivity by default. It is completely dark to the public internet.

---

## Cost
### Cost Warning
VPCs are completely free. You can create up to 5 VPCs per region with zero ongoing charges.

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
VPC_ID=$(aws ec2 describe-vpcs --filters 'Name=tag:Project,Values=aws-from-scratch' --query 'Vpcs[0].VpcId' --output text)
if [ "$VPC_ID" != "None" ]; then aws ec2 delete-vpc --vpc-id "$VPC_ID"; fi
```

---

## Verify cleanup
```bash
aws ec2 describe-vpcs --filters 'Name=tag:Project,Values=aws-from-scratch' --query 'Vpcs[]' --output text
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-06-evidence.md`.

---

## Questions for mastery
1. Why does a VPC have a default Main Route Table created automatically?
2. What is the security difference between the AWS Default VPC and a custom VPC created from scratch?
3. Can two different VPCs in the same account have identical overlapping CIDR blocks (e.g. 10.0.0.0/16)? What breaks if they do?

---

## When to use this
Always build custom VPCs for any serious application or production environment.

---

## When not to use this
Do not create 15 separate VPCs for tiny microservices unless strict network isolation or regulatory boundaries demand it.

---

## What comes next
Phase 07: Subnets — Subdividing your VPC across physical Availability Zones.
