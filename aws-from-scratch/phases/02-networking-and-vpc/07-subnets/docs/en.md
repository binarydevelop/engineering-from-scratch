# Phase 07: Subnets

## Motto
> A subnet lives in exactly one Availability Zone. Redundancy requires multiple subnets across multiple AZs.

**Type:** Hands-on Lab & Network Slicing  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 06: Build a VPC From First Principles  
**AWS Services Involved:** Amazon VPC Subnets  
**Cost Vector:** Subnets cost $0.00.  

---

## Problem
A VPC is a broad CIDR block (e.g. 10.0.0.0/16), but you cannot launch a virtual machine into a VPC directly: instances must attach to a specific physical datacenter. How do we carve the network into physical zones?

---

## Prediction
A subnet cannot span multiple Availability Zones. If you specify `us-east-1a`, that subnet's packets physically terminate in datacenter campus A.

---

## Why this matters
High availability requires deploying resources across at least two Availability Zones. This mandates creating at least two subnets.

---

## First principles
A subnet is a contiguous partition of a VPC's IP address space bound strictly to a single physical Availability Zone. While a VPC spans the entire Region, every subnet is physically tethered to one AZ's hardware switches and power domain.

---

## Mental model
```text
VPC to Subnets:
VPC: 10.0.0.0/16
├── us-east-1a (Physical DC 1)
│   └── Subnet A: 10.0.1.0/24 (251 usable IPs)
│
└── us-east-1b (Physical DC 2)
    └── Subnet B: 10.0.2.0/24 (251 usable IPs)
```

---

## Architecture before AWS
Network engineers mapped VLANs to physical access layer switches in Rack Row 1 and Rack Row 2.

---

## Build the primitive
```python
# Subnet planning verification
subnets = [
    {"name": "Subnet-A", "az": "us-east-1a", "cidr": "10.0.1.0/24"},
    {"name": "Subnet-B", "az": "us-east-1b", "cidr": "10.0.2.0/24"}
]
for s in subnets:
    print(f"Carved {s['name']} in {s['az']} with CIDR {s['cidr']}")
```

---

## Use AWS
```bash
aws ec2 create-subnet --vpc-id $VPC_ID --cidr-block 10.0.1.0/24 --availability-zone us-east-1a --tag-specifications 'ResourceType=subnet,Tags=[{Key=Project,Value=aws-from-scratch},{Key=Name,Value=subnet-az1}]'
```

---

## Inspect it
```bash
aws ec2 describe-subnets --filters 'Name=tag:Project,Values=aws-from-scratch' --query 'Subnets[].[SubnetId,AvailabilityZone,CidrBlock,AvailableIpAddressCount]' --output table
```

---

## Measure it
Observe the `AvailableIpAddressCount`: for a `/24`, it will show exactly `251` (not 256).

---

## Break it
Attempt to create a subnet with an overlapping CIDR (e.g. `10.0.1.128/25`) in the same VPC.

---

## Diagnose it
AWS rejects the API call with `InvalidSubnet.Conflict: The CIDR conflicts with another subnet`.

---

## Recover it
Choose a non-overlapping CIDR block (e.g. `10.0.2.0/24`).

---

## Security
Subnets provide the primary physical containment boundaries for multi-tier applications.

---

## Cost
### Cost Warning
Subnets cost $0.00.

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
for id in $(aws ec2 describe-subnets --filters 'Name=tag:Project,Values=aws-from-scratch' --query 'Subnets[].SubnetId' --output text); do aws ec2 delete-subnet --subnet-id $id; done
```

---

## Verify cleanup
```bash
aws ec2 describe-subnets --filters 'Name=tag:Project,Values=aws-from-scratch' --query 'Subnets[]' --output text
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-07-evidence.md`.

---

## Questions for mastery
1. Why did AWS design subnets to be strictly single-AZ rather than regional?
2. If an EC2 instance in Subnet A (us-east-1a) sends a packet to an instance in Subnet B (us-east-1b), what physical path does that packet take?
3. Can a subnet's CIDR block be modified or expanded after creation?

---

## When to use this
Create at least two subnets in two different AZs for every application tier (public, application, database).

---

## When not to use this
Do not create 50 tiny /28 subnets for individual microservices—it creates routing complexity with zero security benefit.

---

## What comes next
Phase 08: Route Tables — Deciding where packets travel when they leave a network interface.
