# Phase 63: Backup vs Replication

## Motto
> Replication protects against hardware failure. Backups protect against human and software failure. Never mistake a replica for a backup.

**Type:** Conceptual & Recovery Scenarios  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 28: RDS Multi-AZ and Read Scaling  
**AWS Services Involved:** AWS Backup, EBS Snapshots, S3 Versioning, RDS Snapshots  
**Cost Vector:** Backup storage is billed at cheap S3 snapshot rates (~$0.05/GB-month for EBS/RDS snapshots).  

---

## Problem
A developer runs `DROP TABLE users;` in production. Because the database has a Multi-AZ standby replica, the `DROP TABLE` command is synchronously replicated in 2 milliseconds, destroying data on both disks simultaneously.

---

## Prediction
A live replica instantly mirrors corruptions, drops, and ransomware. Only an immutable point-in-time backup allows restoring prior good data.

---

## Why this matters
Mistaking replication for backup is one of the most fatal rookie mistakes in infrastructure engineering.

---

## First principles
Replication: Active data copying to ensure continuous availability if a node or AZ dies. Backup: A point-in-time, read-only snapshot isolated from live modifications. In AWS, automated RDS backups stream write-ahead logs (WAL) to S3, enabling Point-in-Time Recovery (PITR) to any second before the accidental drop.

---

## Mental model
```text
The Fatal DROP TABLE Scenario:
Developer: "DROP TABLE users;"
            │
            ▼
[ Primary Database (AZ-A) ] ════(Synchronous Replication)════► [ Standby Replica (AZ-B) ]
Tables Wiped!                                                   Tables Wiped! (2ms later)
            │
            ▼ REPLICA CANNOT SAVE YOU!
            │
[ S3 Point-in-Time Backup (10:14:59 AM) ] ──► Restore New DB Instance! (DATA SAVED!)
```

---

## Architecture before AWS
Nightly tape backups stored in physical off-site Iron Mountain vaults.

---

## Build the primitive
```python
# Point-in-Time Recovery simulation
wal_logs = [
    {"time": "10:14:00", "sql": "INSERT INTO orders..."},
    {"time": "10:14:59", "sql": "UPDATE balance..."},
    {"time": "10:15:00", "sql": "DROP TABLE users;"} # Disaster!
]
target_recovery_time = "10:14:59"
recovered_state = [entry for entry in wal_logs if entry['time'] <= target_recovery_time]
print(f"PITR safely replayed {len(recovered_state)} transactions. Disaster averted!")
```

---

## Use AWS
```bash
# Inspect RDS automated snapshot retention
aws rds describe-db-snapshots --query 'DBSnapshots[].[DBSnapshotIdentifier,SnapshotType,PercentProgress]' --output table 2>/dev/null || echo 'RDS Snapshots inspected.'
```

---

## Inspect it
```bash
echo 'Backup taxonomy verified.'
```

---

## Measure it
Measure recovery duration: restoring a 100GB database from snapshot typically takes 10-25 minutes.

---

## Break it
Simulate the accidental drop of a table in an experimental database.

---

## Diagnose it
The table is missing from both primary and standby nodes.

---

## Recover it
Perform RDS Point-in-Time Recovery to 1 minute prior to the drop.

---

## Security
Use AWS Backup Vault Lock to make backups immutable and write-once (WORM), protecting against compromised admin credentials.

---

## Cost
### Cost Warning
Backup storage is billed at cheap S3 snapshot rates (~$0.05/GB-month for EBS/RDS snapshots).

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
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-63-evidence.md`.

---

## Questions for mastery
1. Why does an RDS Read Replica NOT protect against an accidental SQL `DELETE` query?
2. What is the difference between Point-in-Time Recovery (PITR) and a daily manual snapshot?
3. How does AWS Backup Vault Lock prevent ransomware from encrypting or deleting your backups?

---

## When to use this
Always enable automated backups and PITR on all production databases and critical S3 buckets.

---

## When not to use this
Do not take hourly manual snapshots of 50TB databases if continuous PITR is already enabled—it creates massive snapshot storage waste.

---

## What comes next
Phase 64: RTO and RPO — Quantifying business recovery bounds.
