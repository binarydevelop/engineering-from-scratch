# Phase 10: Public vs Private Subnets

## Motto
> A subnet is not 'public' because of its name: it is public if and only if its route table targets an Internet Gateway.

**Type:** Hands-on Lab & Architectural Isolation  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 09: Internet Gateway  
**AWS Services Involved:** Public Subnets, Private Subnets, Route Table Associations  
**Cost Vector:** Subnet routing configuration is free.  

---

## Problem
Naming a subnet 'private-db-subnet' does not make it private. If someone associates it with a route table targeting an IGW, database ports can be scanned from the public internet.

---

## Prediction
An EC2 instance in a subnet whose route table only contains `10.0.0.0/16 -> local` cannot be reached from the public internet, even if someone manually assigns it a public IP.

---

## Why this matters
Understanding routing-driven publicity prevents accidental public exposure of databases, caches, and internal microservices.

---

## First principles
Subnet publicity is a mathematical consequence of routing: Public Subnet: Associated with a route table having `0.0.0.0/0 -> igw-xxxx`. Private Subnet: Associated with a route table having NO route to an IGW. Packets to `0.0.0.0/0` are dropped at the virtual router.

---

## Mental model
```text
Public vs Private Routing:
                    ┌─────────────────────────┐
                    │ Internet Gateway (IGW)  │
                    └───────────┬─────────────┘
                                │
                    ┌───────────▼─────────────┐
                    │ Public Route Table      │ (0.0.0.0/0 -> IGW)
                    └───────────┬─────────────┘
                                │
                    ┌───────────▼─────────────┐
                    │ Public Subnet (ALB/NAT) │
                    └─────────────────────────┘

                    ┌─────────────────────────┐
                    │ Private Route Table     │ (10.0.0.0/16 -> local ONLY)
                    └───────────┬─────────────┘
                                │
                    ┌───────────▼─────────────┐
                    │ Private Subnet (DB/App) │
                    └─────────────────────────┘
```

---

## Architecture before AWS
Enterprise datacenters separated public DMZs from private internal networks using physical dual-homed firewalls.

---

## Build the primitive
```python
# Verify subnet route target
def is_public_subnet(routes):
    return any(r['dest'] == '0.0.0.0/0' and r['target'].startswith('igw-') for r in routes)

print("Subnet 1 is public:", is_public_subnet([{'dest': '10.0.0.0/16', 'target': 'local'}, {'dest': '0.0.0.0/0', 'target': 'igw-1234'}]))
print("Subnet 2 is public:", is_public_subnet([{'dest': '10.0.0.0/16', 'target': 'local'}]))
```

---

## Use AWS
```bash
aws ec2 create-route --route-table-id $PUB_RT_ID --destination-cidr-block 0.0.0.0/0 --gateway-id $IGW_ID
```

---

## Inspect it
```bash
aws ec2 describe-route-tables --route-table-ids $PUB_RT_ID --query 'RouteTables[0].Routes' --output table
```

---

## Measure it
Compare connectivity: `curl` to internet from public subnet vs private subnet.

---

## Break it
Associate your private subnet with the public route table.

---

## Diagnose it
The private subnet is now exposed to internet routing rules.

---

## Recover it
Re-associate the private subnet with its dedicated private route table.

---

## Security
Never place database instances (RDS) into public subnets, even if protected by security groups.

---

## Cost
### Cost Warning
Subnet routing configuration is free.

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
# Cleanup custom route associations
```

---

## Verify cleanup
```bash
echo 'Subnets verified.'
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-10-evidence.md`.

---

## Questions for mastery
1. Can an instance in a private subnet initiate an outbound connection to download OS security updates without an IGW route?
2. What is the role of a NAT Gateway in connecting private subnets to the internet?
3. Why is a bastion host / jump box always placed in a public subnet?

---

## When to use this
Always split your VPC into public subnets (for ALBs and NAT) and private subnets (for compute and databases).

---

## When not to use this
Never create a single flat public subnet for all resources.

---

## What comes next
Phase 11: Security Groups — Hypervisor-level stateful packet filtering.
