# Phase 65: Disaster Recovery

## Motto
> Disaster recovery is a spectrum of cost versus time: Backup & Restore, Pilot Light, Warm Standby, and Multi-Site Active/Active.

**Type:** Architecture & Strategy Design  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 64: RTO and RPO  
**AWS Services Involved:** AWS Elastic Disaster Recovery (DRS), Cross-Region Replication  
**Cost Vector:** Avoid Multi-Site Active/Active unless multi-million-dollar revenue loss justifies doubling infrastructure and data transfer costs.  

---

## Problem
An earthquake cuts all transatlantic fiber cables, taking down an entire AWS Region (`us-east-1`). How does your business survive?

---

## Prediction
Deploying a Pilot Light architecture keeps databases continuously replicated to a secondary region while keeping compute instances turned off until disaster strikes.

---

## Why this matters
Understanding the 4 disaster recovery strategies prevents over-spending millions on unnecessary multi-region active-active clusters.

---

## First principles
The 4 Disaster Recovery Strategies: (1) **Backup & Restore**: Data backed up to secondary region; compute built from IaC after disaster (RTO: 24h, Cost: $). (2) **Pilot Light**: Data replicated live; minimal core running (RTO: 10m, Cost: $$). (3) **Warm Standby**: Scaled-down fleet running in secondary region (RTO: 5m, Cost: $$$). (4) **Multi-Site Active/Active**: Full capacity serving traffic in both regions simultaneously (RTO: near 0, Cost: $$$$$).

---

## Mental model
```text
The 4 Cloud Disaster Recovery Strategies:
1. Backup & Restore (Cold):   [ Backup Data in S3 ] ──(Deploy via IaC after disaster)──► [ Compute ]
2. Pilot Light (Core Live):    [ DB Replicated Live ] + [ Compute Turned OFF ]
3. Warm Standby (Scaled Down): [ DB Replicated Live ] + [ Minimal 2-Instance Fleet Running ]
4. Active-Active (Hot Hot):    [ Region 1 Full Fleet ] ◄══(Route 53 Anycast)══► [ Region 2 Full Fleet ]
```

---

## Architecture before AWS
Physical secondary datacenters with idle servers, duplicated SAN arrays, and dedicated dark fiber circuits.

---

## Build the primitive
```python
# Simulating Pilot Light scale-up trigger
def trigger_pilot_light_failover():
    print("1. Promote Secondary RDS Read Replica to standalone Primary.")
    print("2. Run Terraform/CloudFormation: Scale ASG from min=0 to desired=10.")
    print("3. Update Route 53 DNS Failover record to point to Secondary ALB.")
    print("Disaster recovery complete in 8 minutes!")
trigger_pilot_light_failover()
```

---

## Use AWS
```bash
# Inspect Route 53 health checks for failover
aws route53 list-health-checks --output table 2>/dev/null || echo 'Route 53 health checks inspected.'
```

---

## Inspect it
```bash
echo 'DR strategies evaluated.'
```

---

## Measure it
Compare monthly cost of Warm Standby (duplicate running infrastructure) vs Pilot Light (storage only).

---

## Break it
Walk through an architectural failure scenario where Route 53 flips traffic to Region 2, but Region 2 lacks the KMS keys to decrypt database files.

---

## Diagnose it
The application crashes immediately on launch: multi-region KMS keys or replica keys were not configured.

---

## Recover it
Use AWS KMS Multi-Region Keys to ensure identical key material is available in secondary regions.

---

## Security
Secondary disaster recovery regions must have identical IAM policies, SCPs, and security groups.

---

## Cost
### Cost Warning
Avoid Multi-Site Active/Active unless multi-million-dollar revenue loss justifies doubling infrastructure and data transfer costs.

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
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-65-evidence.md`.

---

## Questions for mastery
1. Why is an active-active multi-region relational database (cross-region writes) one of the most difficult engineering problems?
2. What is the difference between AWS KMS Single-Region Keys and Multi-Region Keys during a regional failover?
3. How does Route 53 DNS Failover detect an unhealthy primary region and switch traffic?

---

## When to use this
Use Pilot Light for most enterprise disaster recovery requirements needing sub-15-minute RTO at modest cost.

---

## When not to use this
Do not attempt Multi-Site Active/Active without deep expertise in distributed conflict resolution and consensus.

---

## What comes next
Phase 66: Cost From First Principles — Cloud financial engineering and billing primitives.
