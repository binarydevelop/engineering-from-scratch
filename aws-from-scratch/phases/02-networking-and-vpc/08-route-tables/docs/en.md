# Phase 08: Route Tables

## Motto
> Packets don't think: they look up the longest prefix match in the route table.

**Type:** Hands-on Lab & Routing Mechanics  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 07: Subnets  
**AWS Services Involved:** Amazon VPC Route Tables, Local Route  
**Cost Vector:** Route tables and routing rules cost $0.00.  

---

## Problem
An instance sends an IP packet to `10.0.2.50`. How does the hypervisor virtual switch know whether to route it internally, forward it to a gateway, or drop it?

---

## Prediction
Every route table contains an immutable default route for the VPC CIDR (`10.0.0.0/16 -> local`) that cannot be deleted.

---

## Why this matters
A misconfigured route table is the #1 cause of 'Connection timed out' errors in AWS. If there is no route for a destination, packets are dropped immediately.

---

## First principles
A route table contains a list of rules: `Destination CIDR -> Target Next-Hop`. Routing decisions follow the **Longest Prefix Match** rule. If a packet matches both `10.0.0.0/16 -> local` and `0.0.0.0/0 -> igw-xxxx`, the more specific `/16` route wins for internal traffic, while `/0` matches all external traffic.

---

## Mental model
```text
Route Table Evaluation:
Packet Destination: 10.0.2.88
Route Table Rules:
┌─────────────────┬─────────────┬──────────────────────────────────────────┐
│ Destination     │ Target      │ Match Evaluation                         │
├─────────────────┼─────────────┼──────────────────────────────────────────┤
│ 10.0.0.0/16     │ local       │ MATCH (/16 prefix = 16 bits match!)     │
│ 0.0.0.0/0       │ igw-xxxx    │ MATCH (/0 prefix = 0 bits match)         │
└─────────────────┴─────────────┴──────────────────────────────────────────┘
Result: 10.0.0.0/16 wins (Longest Prefix Match)! Forwarded internally.
```

---

## Architecture before AWS
Network engineers configured static routes and dynamic routing protocols (OSPF, BGP) on Cisco/Juniper hardware routers.

---

## Build the primitive
```python
# Longest prefix match simulation
import ipaddress
routes = [
    (ipaddress.IPv4Network("10.0.0.0/16"), "local"),
    (ipaddress.IPv4Network("0.0.0.0/0"), "internet-gateway")
]
target = ipaddress.IPv4Address("10.0.2.88")
matches = [r for r in routes if target in r[0]]
winner = max(matches, key=lambda r: r[0].prefixlen)
print(f"Target {target} routes to: {winner[1]} (Prefix length: /{winner[0].prefixlen})")
```

---

## Use AWS
```bash
aws ec2 create-route-table --vpc-id $VPC_ID --tag-specifications 'ResourceType=route-table,Tags=[{Key=Project,Value=aws-from-scratch},{Key=Name,Value=custom-rt}]'
```

---

## Inspect it
```bash
aws ec2 describe-route-tables --filters 'Name=tag:Project,Values=aws-from-scratch' --query 'RouteTables[].[RouteTableId,Routes]' --output json
```

---

## Measure it
Inspect route propagation attributes and route state (`active` vs `blackhole`).

---

## Break it
Target an unattached or deleted gateway in a route rule.

---

## Diagnose it
The route state transitions to `blackhole` and traffic to that destination silently disappears.

---

## Recover it
Update the route with `aws ec2 replace-route` to point to a valid active target.

---

## Security
Private subnets are isolated by omitting any route to an Internet Gateway.

---

## Cost
### Cost Warning
Route tables and routing rules cost $0.00.

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
for id in $(aws ec2 describe-route-tables --filters 'Name=tag:Project,Values=aws-from-scratch' --query 'RouteTables[?Associations[0].Main!=`true`].RouteTableId' --output text); do aws ec2 delete-route-table --route-table-id $id; done
```

---

## Verify cleanup
```bash
echo 'Custom route tables cleaned.'
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-08-evidence.md`.

---

## Questions for mastery
1. Why does AWS prevent you from deleting or modifying the `10.0.0.0/16 -> local` route in a route table?
2. If a subnet is not explicitly associated with a route table, which route table does it use by default?
3. How does Longest Prefix Match behave if you add a route for `10.0.1.0/24 -> vpc-peering-connection`?

---

## When to use this
Create dedicated route tables for public and private subnets to enforce explicit routing separation.

---

## When not to use this
Do not create a separate route table for every single subnet if multiple subnets share the exact same routing rules.

---

## What comes next
Phase 09: Internet Gateway — Connecting your VPC routing table to the public IPv4 internet.
