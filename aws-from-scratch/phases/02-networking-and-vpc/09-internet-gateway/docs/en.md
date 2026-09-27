# Phase 09: Internet Gateway

## Motto
> An IGW is not a bottleneck appliance: it is a horizontally scaled 1-to-1 NAT routing gateway.

**Type:** Hands-on Lab & Internet Routing  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 08: Route Tables  
**AWS Services Involved:** Amazon VPC Internet Gateway (IGW)  
**Cost Vector:** Internet Gateways are completely free of charge. There are no hourly or setup fees.  

---

## Problem
Instances inside a private VPC cannot reach the public internet, and external clients cannot reach your web server. What connects the virtual network to the global internet?

---

## Prediction
Attaching an Internet Gateway to a VPC does NOT automatically make instances accessible to the internet until a default route (`0.0.0.0/0 -> igw-xxxx`) and public IPs are configured.

---

## Why this matters
Treating an IGW as a physical router creates misconceptions about bandwidth bottlenecks and packet loss.

---

## First principles
An Internet Gateway (IGW) is a horizontally scaled, redundant, software-defined VPC edge component. It performs two duties: (1) serves as a target in VPC route tables for traffic destined to the internet, and (2) performs 1-to-1 Network Address Translation (NAT) between private IPv4 addresses and allocated public IPv4 addresses.

---

## Mental model
```text
Internet Gateway 1-to-1 NAT:
[ Public Internet ] (Client: 198.51.100.22)
        │
        ▼ (Destination: Public IP 54.210.10.5)
┌───────────────────────────────────────────────┐
│ Internet Gateway (IGW)                        │
│ Maps Public IP 54.210.10.5 <==> 10.0.1.50     │
└───────┬───────────────────────────────────────┘
        │ (Destination rewritten to: 10.0.1.50)
        ▼
┌───────────────────────────────────────────────┐
│ VPC Public Subnet (EC2 Private IP: 10.0.1.50) │
└───────────────────────────────────────────────┘
```

---

## Architecture before AWS
Datacenters maintained high-throughput border routers with BGP peering to Tier 1 internet transit providers.

---

## Build the primitive
```python
# 1-to-1 NAT simulation
nat_table = {"54.210.10.5": "10.0.1.50"}
packet_in = {"src": "198.51.100.22", "dst": "54.210.10.5"}
packet_in["dst"] = nat_table[packet_in["dst"]]
print(f"IGW translated destination to private VPC IP: {packet_in['dst']}")
```

---

## Use AWS
```bash
aws ec2 create-internet-gateway --tag-specifications 'ResourceType=internet-gateway,Tags=[{Key=Project,Value=aws-from-scratch}]'
```

---

## Inspect it
```bash
aws ec2 describe-internet-gateways --filters 'Name=tag:Project,Values=aws-from-scratch' --output table
```

---

## Measure it
Verify network throughput: an IGW imposes zero bandwidth throttling (bandwidth is bounded strictly by the instance's network card).

---

## Break it
Detach the IGW from an active VPC while an instance is running.

---

## Diagnose it
All inbound and outbound public internet traffic drops instantly with `Network is unreachable`.

---

## Recover it
Reattach the IGW: `aws ec2 attach-internet-gateway --internet-gateway-id $IGW_ID --vpc-id $VPC_ID`.

---

## Security
An IGW alone does not expose your machines. A machine is only exposed if it has: (1) route to IGW, (2) public IP, and (3) permissive Security Group.

---

## Cost
### Cost Warning
Internet Gateways are completely free of charge. There are no hourly or setup fees.

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
IGW_ID=$(aws ec2 describe-internet-gateways --filters 'Name=tag:Project,Values=aws-from-scratch' --query 'InternetGateways[0].InternetGatewayId' --output text)
if [ "$IGW_ID" != "None" ]; then aws ec2 detach-internet-gateway --internet-gateway-id $IGW_ID --vpc-id $VPC_ID; aws ec2 delete-internet-gateway --internet-gateway-id $IGW_ID; fi
```

---

## Verify cleanup
```bash
aws ec2 describe-internet-gateways --filters 'Name=tag:Project,Values=aws-from-scratch' --query 'InternetGateways[]' --output text
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-09-evidence.md`.

---

## Questions for mastery
1. Why is an Internet Gateway considered horizontally scalable with zero maintenance, unlike a NAT Gateway?
2. Does an EC2 instance OS kernel know its own public IP address when running in a public subnet?
3. Can a single VPC have multiple Internet Gateways attached simultaneously?

---

## When to use this
Attach exactly one Internet Gateway to any VPC that needs public ingress or egress.

---

## When not to use this
Do not attach an IGW to strictly isolated VPCs intended for back-office batch processing or air-gapped workloads.

---

## What comes next
Phase 10: Public vs Private Subnets — Deriving subnet publicity from routing tables.
