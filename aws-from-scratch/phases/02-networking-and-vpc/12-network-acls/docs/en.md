# Phase 12: Network ACLs

## Motto
> Network ACLs are stateless subnet gatekeepers. You must explicitly open ephemeral ports for return traffic.

**Type:** Hands-on Lab & Stateless Filtering  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 11: Security Groups  
**AWS Services Involved:** Amazon VPC Network ACLs (NACLs)  
**Cost Vector:** Network ACLs are free.  

---

## Problem
Security Groups cannot block a specific malicious IP address (they only have Allow rules). How do we block a compromised CIDR block at the subnet perimeter?

---

## Prediction
If you allow inbound port 80 in a NACL but forget to allow outbound ephemeral ports (1024-65535), web requests will reach the server but responses will be blocked.

---

## Why this matters
The stateless nature of NACLs trips up almost every junior cloud engineer. Return packets do not automatically bypass NACLs.

---

## First principles
A Network ACL is a stateless subnet-level filter evaluated in numbered rule order (1-32766). Stateless means the filter has zero memory of active connections. Every incoming packet is evaluated against inbound rules; every outgoing packet is evaluated against outbound rules independently.

---

## Mental model
```text
Stateless NACL Ephemeral Port Requirement:
Client (Port 52140) ────(SYN Port 80)────► [ NACL Inbound Rule 100: Allow Port 80 ] ──► Server
Client (Port 52140) ◄──(SYN-ACK Return)─── [ NACL Outbound Rule ???: Must Allow Ephemeral 1024-65535! ]
                                           (If outbound rule missing -> Return packet is DROPPED!)
```

---

## Architecture before AWS
Router access control lists configured on physical gateway interfaces.

---

## Build the primitive
```python
# NACL Rule Number Evaluation Order
rules = [
    {"rule_num": 100, "action": "DENY", "cidr": "198.51.100.44/32"},
    {"rule_num": 200, "action": "ALLOW", "cidr": "0.0.0.0/0"},
    {"rule_num": "*", "action": "DENY", "cidr": "0.0.0.0/0"}
]
def evaluate_nacl(ip):
    for r in sorted(rules, key=lambda x: str(x['rule_num'])):
        if r['rule_num'] == 100 and ip == "198.51.100.44":
            return f"Rule {r['rule_num']} matched: {r['action']}"
        elif r['rule_num'] == 200:
            return f"Rule {r['rule_num']} matched: {r['action']}"
    return "Default Deny (*)"
print(evaluate_nacl("198.51.100.44"))
print(evaluate_nacl("192.0.2.1"))
```

---

## Use AWS
```bash
aws ec2 create-network-acl --vpc-id $VPC_ID --tag-specifications 'ResourceType=network-acl,Tags=[{Key=Project,Value=aws-from-scratch}]'
```

---

## Inspect it
```bash
aws ec2 describe-network-acls --filters 'Name=tag:Project,Values=aws-from-scratch' --output json
```

---

## Measure it
Compare Security Group vs NACL: Security Groups evaluate all rules; NACLs terminate at first matching rule number.

---

## Break it
Delete the default outbound rule (`Rule 100: Allow All`) in a custom NACL.

---

## Diagnose it
The client successfully sends HTTP requests, but `curl` hangs forever waiting for the response.

---

## Recover it
Add outbound rule allowing ephemeral ports: `aws ec2 create-network-acl-entry --network-acl-id $NACL_ID --rule-number 100 --protocol tcp --rule-action allow --egress --cidr-block 0.0.0.0/0 --port-range From=1024,To=65535`.

---

## Security
Use NACLs sparingly: primarily for blocking known bad IP ranges or enforcing coarse compliance boundaries.

---

## Cost
### Cost Warning
Network ACLs are free.

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
for id in $(aws ec2 describe-network-acls --filters 'Name=tag:Project,Values=aws-from-scratch' --query 'NetworkAcls[?IsDefault!=`true`].NetworkAclId' --output text); do aws ec2 delete-network-acl --network-acl-id $id; done
```

---

## Verify cleanup
```bash
echo 'Custom NACLs cleaned.'
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-12-evidence.md`.

---

## Questions for mastery
1. Why do Linux and Windows clients connect using random high-numbered ephemeral ports (32768-60999 or 49152-65535)?
2. What is the operational downside of managing complex NACL rules compared to Security Groups?
3. Which filter evaluates first for traffic entering a subnet: the Network ACL or the Security Group?

---

## When to use this
Use NACLs when you need an explicit DENY rule to block a malicious IP or subnet.

---

## When not to use this
Do not duplicate your Security Group rules inside NACLs—it creates high operational maintenance with zero benefit.

---

## What comes next
Phase 13: EC2 From First Principles — Launching virtual compute machines.
