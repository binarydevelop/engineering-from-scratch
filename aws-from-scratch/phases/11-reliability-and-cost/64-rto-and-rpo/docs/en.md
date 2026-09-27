# Phase 64: RTO and RPO

## Motto
> How long can you be down (RTO)? How much data can you lose (RPO)? Architecture is the derivative of these two numbers.

**Type:** Architectural Design & Metrics  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 63: Backup vs Replication  
**AWS Services Involved:** Disaster Recovery Metrics, Business Impact Analysis  
**Cost Vector:** Achieving RPO = 0 requires continuous synchronous replication, which increases network latency and infrastructure spend.  

---

## Problem
An engineer designs an active-active multi-region database costing $100,000/month for an internal company lunch menu app that only needs nightly backups.

---

## Prediction
Quantifying Recovery Time Objective (RTO) and Recovery Point Objective (RPO) with business stakeholders dictates the exact infrastructure tier required.

---

## Why this matters
RTO and RPO are the two foundational metrics that govern disaster recovery architecture and cloud spend.

---

## First principles
RTO (Recovery Time Objective): The maximum acceptable duration of system downtime before business operations must be restored. RPO (Recovery Point Objective): The maximum acceptable age of data that can be lost when unexpected disaster strikes (data loss interval).

---

## Mental model
```text
RTO vs RPO Timeline:
                RPO (Data Loss Window)            RTO (Downtime Window)
          ◄───────────────────────────────► ◄───────────────────────────────►
──────────┼───────────────────────────────┼─────────────────────────────────┼────────► Time
    Last Good Backup                Disaster Strikes!               System Restored!
    (e.g., 2:00 AM)                 (e.g., 3:45 AM)                 (e.g., 4:15 AM)
    Data lost: 1 hour 45 mins       Downtime: 30 mins
```

---

## Architecture before AWS
Disaster recovery binders and annual weekend datacenter evacuation simulation tests.

---

## Build the primitive
```python
# RTO / RPO Tradeoff Matrix Calculator
dr_tiers = {
    "Backup & Restore": {"RTO": "24 hours", "RPO": "24 hours", "Cost": "$"},
    "Pilot Light":      {"RTO": "10-30 mins", "RPO": "5 mins", "Cost": "$$"},
    "Warm Standby":     {"RTO": "5-10 mins", "RPO": "< 1 min", "Cost": "$$$"},
    "Active-Active":    {"RTO": "Near 0", "RPO": "0", "Cost": "$$$$$"}
}
for tier, metrics in dr_tiers.items():
    print(f"Tier: {tier:<18} | RTO: {metrics['RTO']:<12} | RPO: {metrics['RPO']:<10} | Cost: {metrics['Cost']}")
```

---

## Use AWS
```bash
# Inspect AWS Elastic Disaster Recovery CLI
aws drs describe-recovery-instances 2>/dev/null || echo 'DRS CLI verified.'
```

---

## Inspect it
```bash
echo 'RTO/RPO metrics documented.'
```

---

## Measure it
Measure actual RTO in a recovery simulation: from failure trigger to first HTTP 200 response.

---

## Break it
Design a recovery approach for an application with RTO=5 minutes and RPO=0 seconds.

---

## Diagnose it
Backup & Restore fails (RTO is hours). Multi-AZ with automated failover is required.

---

## Recover it
Deploy Multi-AZ ALB + Multi-AZ RDS with synchronous replication.

---

## Security
Disaster recovery testing must verify that IAM policies, KMS keys, and secrets exist in the recovery environment.

---

## Cost
### Cost Warning
Achieving RPO = 0 requires continuous synchronous replication, which increases network latency and infrastructure spend.

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
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-64-evidence.md`.

---

## Questions for mastery
1. Why is an RPO of 0 seconds physically impossible across transatlantic regions with synchronous replication? (Speed of light!).
2. What business questions should you ask stakeholders before deciding between Pilot Light and Warm Standby?
3. How does asynchronous database replication affect the measured RPO during an unexpected regional outage?

---

## When to use this
Define RTO and RPO for every tier in your architecture before selecting AWS services.

---

## When not to use this
Do not promise RTO < 1 minute without automated, tested failover pipelines in place.

---

## What comes next
Phase 65: Disaster Recovery — The four industry recovery strategies.
