# Phase 26: RDS From First Principles

## Motto
> RDS is not a new database engine: it is PostgreSQL or MySQL on managed EC2 with automated operations.

**Type:** Hands-on Lab & Relational Storage  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 15: EBS  
**AWS Services Involved:** Amazon RDS (PostgreSQL/MySQL), Parameter Groups  
**Cost Vector:** `db.t4g.micro` costs ~$0.018/hour (~$13/month). Storage costs ~$0.115/GB-month. Delete immediately after testing!  

---

## Problem
Self-hosting PostgreSQL on EC2 means you must manually configure automated WAL backups, point-in-time recovery, OS security patching, and failover scripts. A disk failure at 3 AM requires manual intervention.

---

## Prediction
Amazon RDS will automate OS patching, automated daily backups, and point-in-time recovery, but locks away SSH root access to the underlying host.

---

## Why this matters
Understanding what RDS abstracts (and what it doesn't) prevents treating the database as a magic box that never runs out of connections or IOPS.

---

## First principles
RDS runs standard open-source database binaries inside an AWS-managed EC2 instance backed by EBS storage. AWS manages the control plane: automating EBS volume expansion, taking periodic snapshots to S3, and streaming transaction logs (WAL) to provide Point-in-Time Recovery (PITR) to any second within the retention window.

---

## Mental model
```text
Amazon RDS Architecture:
AWS Managed Control Plane
┌────────────────────────────────────────────────────────┐
│ Amazon RDS DB Instance (`db.t4g.micro`)                │
│ • Runs standard open-source PostgreSQL 16 engine       │
│ • No SSH root access (Managed OS & engine patching)    │
│ └── Dedicated EBS gp3 Storage (Database Data & WAL)    │
└──────────────────────────┬─────────────────────────────┘
                           │ Continuous WAL Stream & Daily Snapshots
┌──────────────────────────▼─────────────────────────────┐
│ Amazon S3 (Point-in-Time Recovery up to 35 Days)       │
└────────────────────────────────────────────────────────┘
```

---

## Architecture before AWS
Database administrators manually scheduled `pg_dump` cron jobs, configured WAL archiving, and managed physical replica servers.

---

## Build the primitive
```python
# Estimating connection RAM limits
max_connections = 100
ram_per_conn_mb = 10
total_conn_ram_mb = max_connections * ram_per_conn_mb
print(f"PostgreSQL {max_connections} connections consume ~{total_conn_ram_mb}MB RAM before query buffers!")
```

---

## Use AWS
```bash
aws rds create-db-instance --db-instance-identifier lab-db --db-instance-class db.t4g.micro --engine postgres --allocated-storage 20 --master-username postgres --master-user-password 'LabPassword2026!' --no-publicly-accessible --tags Key=Project,Value=aws-from-scratch
```

---

## Inspect it
```bash
aws rds describe-db-instances --db-instance-identifier lab-db --query 'DBInstances[].[DBInstanceIdentifier,DBInstanceStatus,Endpoint.Address,EngineVersion]' --output table
```

---

## Measure it
Measure commit latency: RDS synchronous write to EBS gp3 (typically 1-3ms).

---

## Break it
Exhaust PostgreSQL connection pool by opening 150 concurrent client connections on a `db.t4g.micro`.

---

## Diagnose it
Database logs: `FATAL: remaining connection slots are reserved for non-replicated superuser connections`.

---

## Recover it
Deploy Amazon RDS Proxy or configure application-level connection pooling (e.g. SQLAlchemy QueuePool / PgBouncer).

---

## Security
Always set `PubliclyAccessible: false`. Never place production database instances in public subnets.

---

## Cost
### Cost Warning
`db.t4g.micro` costs ~$0.018/hour (~$13/month). Storage costs ~$0.115/GB-month. Delete immediately after testing!

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
aws rds delete-db-instance --db-instance-identifier lab-db --skip-final-snapshot
```

---

## Verify cleanup
```bash
aws rds describe-db-instances --query 'DBInstances[?DBInstanceIdentifier==`lab-db`]' --output text
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-26-evidence.md`.

---

## Questions for mastery
1. Why does AWS RDS forbid direct SSH or root access to the underlying operating system?
2. What is the difference between an RDS automated backup (snapshot + WAL) and a manual DB snapshot?
3. Why does a serverless architecture (Lambda) easily overwhelm traditional relational database connection limits?

---

## When to use this
Use RDS for structured relational schemas, ACID transactions, complex SQL JOINs, and legacy applications.

---

## When not to use this
Do not use RDS for high-frequency unstructured key-value caching (use DynamoDB or Redis).

---

## What comes next
Phase 27: RDS Connectivity — Database subnet groups and security group chaining.
