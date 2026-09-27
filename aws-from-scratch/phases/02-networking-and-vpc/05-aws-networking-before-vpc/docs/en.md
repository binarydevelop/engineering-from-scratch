# Phase 05: AWS Networking Before VPC

## Motto
> A network is just routers, routing tables, and IP addresses. VPC is software-defined packet encapsulation.

**Type:** Systems Experiment & Network Math  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 04: IAM Policies  
**AWS Services Involved:** IPv4, RFC 1918, CIDR Blocks  
**Cost Vector:** VPC CIDR allocations cost $0.00.  

---

## Problem
Engineers configure subnets like `10.0.1.0/24` without understanding binary masking, run out of private IP addresses 6 months into production, and find that AWS VPC CIDR blocks cannot be easily re-architected without rebuilding everything.

---

## Prediction
An IPv4 CIDR of `/24` provides 256 theoretical addresses, but AWS reserves exactly 5 addresses, leaving 251 usable for EC2 and ENIs.

---

## Why this matters
Every cloud resource (EC2, RDS, Lambda in VPC, ALB) consumes private IP addresses from your subnets. Miscalculating CIDRs leads to production scaling brick walls.

---

## First principles
An IPv4 address is 32 bits (4 octets of 8 bits). CIDR `/N` specifies that the first N bits represent the network prefix, while `32 - N` bits represent host addresses ($2^{32-N}$). In AWS, 5 IPs are always reserved: `.0` (Network), `.1` (VPC Router), `.2` (DNS resolver), `.3` (Future use), `.255` (Broadcast).

---

## Mental model
```text
CIDR Subnet Math:
10.0.1.0/24 = 32-bit address:
[ 00001010 . 00000000 . 00000001 ] [ 00000000 ]
<--------- Network Prefix (24 bits) -------> < Host (8 bits) >
Total IPs: 2^8 = 256
AWS Reserved:
  10.0.1.0   -> Network Address
  10.0.1.1   -> VPC Virtual Router
  10.0.1.2   -> Amazon Provided DNS (Route 53 Resolver)
  10.0.1.3   -> AWS Internal Reserved
  10.0.1.255 -> Broadcast (not used in VPC, but reserved)
Usable IPs: 251
```

---

## Architecture before AWS
Network engineers manually assigned VLANs on Cisco Catalyst switches, configured trunk ports (802.1Q), and set up physical DHCP servers.

---

## Build the primitive
```python
import ipaddress
net = ipaddress.IPv4Network("10.0.1.0/24")
print(f"Network: {net.network_address}")
print(f"Netmask: {net.netmask}")
print(f"Total Hosts: {net.num_addresses}")
print(f"Usable AWS IPs: {net.num_addresses - 5}")
```

---

## Use AWS
```bash
# Inspect default VPC CIDR allocation
aws ec2 describe-vpcs --query 'Vpcs[].[VpcId,CidrBlock,IsDefault]' --output table
```

---

## Inspect it
```bash
python3 -c "import ipaddress; print(list(ipaddress.IPv4Network('10.0.0.0/16').subnets(new_prefix=24))[:4])"
```

---

## Measure it
Calculate subnet exhaustion thresholds for container workloads deploying 500 tasks.

---

## Break it
Attempt to create a subnet with a `/29` mask (8 IPs) and try to launch 4 instances.

---

## Diagnose it
The 4th instance launch fails: 8 total IPs - 5 AWS reserved = only 3 usable IPs!

---

## Recover it
Design subnets with at least `/24` (251 usable IPs) or `/20` (4,091 usable IPs) for compute tiers.

---

## Security
RFC 1918 defines non-routable private address spaces (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`) to isolate private infrastructure from the public internet.

---

## Cost
### Cost Warning
VPC CIDR allocations cost $0.00.

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
# No resources created in Phase 05.
```

---

## Verify cleanup
```bash
echo 'Account clean.'
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-05-evidence.md`.

---

## Questions for mastery
1. Why does AWS reserve the `.2` address in every subnet instead of having a single global DNS IP across the entire VPC?
2. What happens if your on-premises corporate network uses `10.0.0.0/16` and your AWS VPC also uses `10.0.0.0/16` when you attempt to connect them via VPN?
3. Why is `/28` the smallest subnet mask AWS allows, and `/16` the largest single VPC CIDR?

---

## When to use this
Always plan CIDR blocks carefully before creating production VPCs.

---

## When not to use this
Never choose `172.31.0.0/16` for corporate VPCs as it collides with the AWS Default VPC.

---

## What comes next
Phase 06: Build a VPC From First Principles — Creating your own software-defined private cloud network.
