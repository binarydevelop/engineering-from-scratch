# Phase 11: Security Groups

## Motto
> Security Groups are stateful virtual firewalls evaluated at the hypervisor ENI. If inbound is allowed, outbound return traffic is automatically allowed.

**Type:** Hands-on Lab & Firewall Experiments  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 10: Public vs Private Subnets  
**AWS Services Involved:** Amazon EC2 Security Groups  
**Cost Vector:** Security Groups are completely free.  

---

## Problem
Once an instance has an IP address, port scanners on the public internet can immediately probe open ports (SSH 22, Redis 6379, DB 5432). How do we enforce zero-trust packet filtering?

---

## Prediction
A Security Group with zero inbound rules will silently drop all incoming connection attempts, resulting in client TCP SYN timeouts.

---

## Why this matters
Security Groups are the primary defense perimeter for AWS compute. Understanding their stateful nature prevents opening unnecessary ports.

---

## First principles
A Security Group is a stateful distributed packet filter attached directly to an Elastic Network Interface (ENI). Stateful means the hypervisor tracks TCP connection states (`SYN`, `SYN-ACK`, `ESTABLISHED`). When an inbound connection is allowed, return traffic is automatically allowed regardless of outbound rules.

---

## Mental model
```text
Stateful Security Group Mechanics:
Client ────────(TCP SYN Port 80)────────► [ ENI Security Group ] ──► Allowed!
Client ◄──────(TCP SYN-ACK Return)────── [ ENI Security Group ] ◄── AUTO-ALLOWED!
                                         (Tracked in Connection State Table)
```

---

## Architecture before AWS
System administrators configured Linux `iptables` / `nftables` or physical ASA firewall appliances.

---

## Build the primitive
```python
# Simulating stateful connection table
state_table = set()
def handle_packet(src_ip, dst_port, is_inbound, rule_allowed):
    conn_key = (src_ip, dst_port)
    if is_inbound:
        if rule_allowed:
            state_table.add(conn_key)
            return "ALLOW (Rule matched)"
        return "DROP (No rule)"
    else: # outbound return
        if conn_key in state_table:
            return "ALLOW (Stateful return recognized)"
        return "EVALUATE_OUTBOUND"

print(handle_packet("198.51.100.1", 80, is_inbound=True, rule_allowed=True))
print(handle_packet("198.51.100.1", 80, is_inbound=False, rule_allowed=False))
```

---

## Use AWS
```bash
aws ec2 create-security-group --group-name lab-web-sg --description 'Lab Web Security Group' --vpc-id $VPC_ID --tag-specifications 'ResourceType=security-group,Tags=[{Key=Project,Value=aws-from-scratch}]'
```

---

## Inspect it
```bash
aws ec2 describe-security-groups --filters 'Name=tag:Project,Values=aws-from-scratch' --output json
```

---

## Measure it
Measure connection timeout duration when SYN packets are silently discarded (typically 30-60s).

---

## Break it
Remove the inbound rule for port 80 and attempt to connect with curl.

---

## Diagnose it
curl hangs with `Connection timed out` (NOT `Connection refused`).

---

## Recover it
Authorize inbound traffic: `aws ec2 authorize-security-group-ingress --group-id $SG_ID --protocol tcp --port 80 --cidr 0.0.0.0/0`.

---

## Security
Never use `0.0.0.0/0` on SSH port 22 or database port 5432. Reference other security groups by ID for microservice communication.

---

## Cost
### Cost Warning
Security Groups are completely free.

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
for id in $(aws ec2 describe-security-groups --filters 'Name=tag:Project,Values=aws-from-scratch' --query 'SecurityGroups[?GroupName!=`default`].GroupId' --output text); do aws ec2 delete-security-group --group-id $id; done
```

---

## Verify cleanup
```bash
echo 'Security groups cleaned.'
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-11-evidence.md`.

---

## Questions for mastery
1. Why does a dropped packet in a Security Group cause a 'Connection timed out' while an inactive service causes a 'Connection refused'?
2. What is the architectural advantage of referencing a Security Group ID as a source instead of an IP address CIDR?
3. Can a Security Group have an explicit 'Deny' rule?

---

## When to use this
Use Security Groups as your primary firewall for all ENIs, EC2 instances, ALBs, and RDS databases.

---

## When not to use this
Security Groups cannot perform Layer 7 HTTP payload inspection or SQL injection filtering (use AWS WAF for Layer 7).

---

## What comes next
Phase 12: Network ACLs — Subnet-level stateless defense-in-depth packet filtering.
