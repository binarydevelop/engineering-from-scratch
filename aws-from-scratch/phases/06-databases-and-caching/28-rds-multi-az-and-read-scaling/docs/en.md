# Phase 28: RDS Multi-AZ and Read Scaling

## Motto
> Multi-AZ is for availability (synchronous). Read Replicas are for performance (asynchronous). Never conflate the two.

**Type:** Hands-on Lab & Database Replication  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 27: RDS Connectivity  
**AWS Services Involved:** Amazon RDS Multi-AZ, Read Replicas  
**Cost Vector:** Multi-AZ exactly doubles the hourly instance and storage cost because AWS provisions two physical database servers.  

---

## Problem
Engineers enable Read Replicas thinking it gives them zero-downtime failover, or enable Multi-AZ thinking it will double their read throughput.

---

## Prediction
Multi-AZ uses synchronous block-level replication to an invisible standby node (no read traffic allowed). Read Replicas use asynchronous engine replication and can serve read queries.

---

## Why this matters
Conflating replication mechanisms leads to architectural failure: trying to read from a Multi-AZ standby fails because it has no separate DNS endpoint.

---

## First principles
Multi-AZ: Synchronous physical EBS replication to a standby node in AZ-B. Writes are only committed when flushed to both disks. Failover flips the DNS CNAME to the standby in 60-120s. Read Replica: Asynchronous PostgreSQL streaming replication to an active database node with its own DNS endpoint.

---

## Mental model
```text
Multi-AZ vs Read Replicas:
[ Amazon RDS Multi-AZ ] (High Availability)
Primary DB (AZ-A) ════(Synchronous EBS Replication)════► Standby DB (AZ-B)
• Accepts Reads & Writes                                  • INVISIBLE (No DNS endpoint)
• Automatic DNS Failover                                  • Zero queries served!

[ Amazon RDS Read Replica ] (Read Scaling)
Primary DB (AZ-A) ────(Asynchronous WAL Stream)────► Read Replica (AZ-B/Anywhere)
• Accepts Writes                                      • Has independent DNS endpoint!
                                                      • Serves read-only queries (SELECT)
```

---

## Architecture before AWS
PostgreSQL streaming replication with Pacemaker / Corosync heartbeats for automated virtual IP failover.

---

## Build the primitive
```python
# Simulating replication lag
wal_sent_lsn = 1000500
wal_replay_lsn = 1000420
lag_bytes = wal_sent_lsn - wal_replay_lsn
print(f"Read Replica replication lag: {lag_bytes} bytes behind primary")
```

---

## Use AWS
```bash
aws rds reboot-db-instance --db-instance-identifier lab-db --force-failover
```

---

## Inspect it
```bash
aws rds describe-db-instances --db-instance-identifier lab-db --query 'DBInstances[0].[DBInstanceStatus,SecondaryAvailabilityZone]' --output table
```

---

## Measure it
Measure failover time: application reconnection delay during failover (typically 60-90 seconds).

---

## Break it
Trigger a force-failover on a Multi-AZ database while a script is executing continuous SELECT queries.

---

## Diagnose it
The script experiences a transient connection drop for ~60 seconds while DNS propagates to the standby IP.

---

## Recover it
The application connection pool reconnects automatically once the new primary completes recovery.

---

## Security
Read Replicas can reside in different AWS regions, enabling cross-region disaster recovery and localized read latency.

---

## Cost
### Cost Warning
Multi-AZ exactly doubles the hourly instance and storage cost because AWS provisions two physical database servers.

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
# Cleanup database
```

---

## Verify cleanup
```bash
echo 'Database cleaned.'
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-28-evidence.md`.

---

## Questions for mastery
1. Why does a Multi-AZ deployment NOT increase read performance for your application?
2. What happens if an application writes an order to the Primary and immediately attempts to read it from an asynchronous Read Replica? (Hint: Replication Lag).
3. Under what conditions can a Read Replica be promoted to a standalone primary database?

---

## When to use this
Use Multi-AZ for mission-critical databases requiring automated failover with zero committed data loss.

---

## When not to use this
Do not use Multi-AZ for development or staging environments where a 15-minute restore from backup is acceptable.

---

## What comes next
Phase 29: DynamoDB From First Principles — Distributed NoSQL key-value storage.
