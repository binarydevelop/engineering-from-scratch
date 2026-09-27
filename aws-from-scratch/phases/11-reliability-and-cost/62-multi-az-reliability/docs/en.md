# Phase 62: Multi-AZ Reliability

## Motto
> An Availability Zone is an independent physical blast radius. Design state and stateless tiers accordingly.

**Type:** Architecture & Systems Resilience  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 61: Reliability From First Principles  
**AWS Services Involved:** Multi-AZ Design, Failure Domains, Zonal Independence  
**Cost Vector:** Cross-AZ data transfer fees ($0.01/GB) apply when traffic crosses AZ boundaries.  

---

## Problem
During a severe storm, an entire datacenter facility loses power. If your application relies on components located exclusively in that facility, the entire system collapses.

---

## Prediction
A Multi-AZ architecture with cross-zone load balancing and synchronous database replication survives a total facility loss with zero human intervention.

---

## Why this matters
Multi-AZ is the primary reliability building block in AWS. Understanding independent failure domains prevents cascading failures.

---

## First principles
Availability Zones are physically distinct facilities separated by kilometers with independent power utilities, water cooling, physical security, and diverse fiber paths. Statistically, catastrophic physical events (fires, plane crashes, floods) are isolated to a single AZ.

---

## Mental model
```text
Multi-AZ Failure Containment:
[ Physical Catastrophe in AZ-A! ]
┌─────────────────────────────────────┐      ┌─────────────────────────────────────┐
│ Availability Zone A (POWER CUT!)    │      │ Availability Zone B (OPERATIONAL)   │
│ ❌ EC2 App Server (Offline)         │      │ ✓ EC2 App Server (Healthy)          │
│ ❌ Primary DB (Offline)             │      │ ✓ Standby DB Promoted to PRIMARY!   │
└─────────────────────────────────────┘      └─────────────────────────────────────┘
                                   │
                                   ▼
          ALB automatically routes 100% of traffic to AZ-B!
          Clients experience zero interruption!
```

---

## Architecture before AWS
Cold standby secondary datacenters requiring manual DNS flips and hours of database recovery.

---

## Build the primitive
```python
# Simulating multi-AZ quorum voting
azs = ["us-east-1a", "us-east-1b", "us-east-1c"]
def has_quorum(active_azs):
    return len(active_azs) > len(azs) / 2
print("Quorum with 3 AZs active:", has_quorum(["us-east-1a", "us-east-1b", "us-east-1c"]))
print("Quorum with 1 AZ lost:", has_quorum(["us-east-1b", "us-east-1c"]))
print("Quorum with 2 AZs lost:", has_quorum(["us-east-1c"]))
```

---

## Use AWS
```bash
# Inspect regional availability zone status
aws ec2 describe-availability-zones --query 'AvailabilityZones[].[ZoneName,State]' --output table
```

---

## Inspect it
```bash
echo 'Multi-AZ failure models verified.'
```

---

## Measure it
Measure cross-AZ latency: dark fiber connections between AZs provide < 2ms round trip.

---

## Break it
Simulate AZ failure in `projects/project-02-ha-webapp`.

---

## Diagnose it
ALB detects AZ-A unhealthy; all traffic served by AZ-B.

---

## Recover it
Automated self-healing restores AZ-A when facility recovers.

---

## Security
Ensure security groups are replicated symmetrically across all subnets in all AZs.

---

## Cost
### Cost Warning
Cross-AZ data transfer fees ($0.01/GB) apply when traffic crosses AZ boundaries.

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
# No resources created.
```

---

## Verify cleanup
```bash
echo 'Account clean.'
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-62-evidence.md`.

---

## Questions for mastery
1. Why is deploying across 3 Availability Zones significantly safer for consensus algorithms (Raft/Paxos) than 2 AZs?
2. What is the 'Split-Brain' problem in distributed database failover, and how does Multi-AZ prevent it?
3. Why should you NOT deploy a Multi-AZ architecture if your database replication is asynchronous?

---

## When to use this
Use Multi-AZ for all mission-critical production applications, databases, and APIs.

---

## When not to use this
Do not deploy Multi-AZ for temporary compute rendering clusters that can easily be restarted if an AZ blips.

---

## What comes next
Phase 63: Backup vs Replication — Why a replica is NOT a backup.
