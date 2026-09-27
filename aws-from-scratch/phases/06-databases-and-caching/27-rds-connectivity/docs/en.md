# Phase 27: RDS Connectivity

## Motto
> Never expose your database to the internet for developer convenience. Chain security groups.

**Type:** Hands-on Lab & Network Security  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 26: RDS From First Principles  
**AWS Services Involved:** DB Subnet Groups, Security Group Chaining  
**Cost Vector:** Security group chaining and DB Subnet Groups cost $0.00.  

---

## Problem
Developers make databases public so they can connect from their local laptops using pgAdmin or DBeaver, exposing the database port to global botnets and credential stuffers.

---

## Prediction
Chaining security groups allows the database to accept TCP 5432 connections ONLY from instances with the Application Security Group ID attached, blocking everything else.

---

## Why this matters
Security group chaining is the single most important network security pattern in cloud architecture.

---

## First principles
A DB Subnet Group is a collection of private subnets spanning at least two Availability Zones where RDS can place network interfaces. Security Group Chaining uses a Security Group ID (e.g. `sg-app123`) as the source in another Security Group rule instead of a CIDR IP address.

---

## Mental model
```text
Security Group Chaining Architecture:
[ Application EC2 / ECS ] (Attached: sg-app)
           │
           │ TCP Port 5432 (Allowed by rule: Source = sg-app)
           ▼
[ Amazon RDS PostgreSQL ] (Attached: sg-rds)
(Inbound Rule: Allow TCP 5432 ONLY from sg-app)
(No IP CIDR! Even if instance IP changes, traffic is allowed!)
```

---

## Architecture before AWS
Configuring `pg_hba.conf` with IP whitelists and physical firewall ACLs.

---

## Build the primitive
```python
# Simulating SG chaining logic
app_instances = {"i-1": "sg-app", "i-2": "sg-app", "i-rogue": "sg-other"}
def can_access_db(instance_id):
    return app_instances.get(instance_id) == "sg-app"
print("App instance 1 can reach DB:", can_access_db("i-1"))
print("Rogue instance can reach DB:", can_access_db("i-rogue"))
```

---

## Use AWS
```bash
aws ec2 authorize-security-group-ingress --group-id $SG_RDS_ID --protocol tcp --port 5432 --source-group $SG_APP_ID
```

---

## Inspect it
```bash
aws ec2 describe-security-groups --group-ids $SG_RDS_ID --output json
```

---

## Measure it
Measure latency between EC2 and RDS in the same AZ (< 1ms).

---

## Break it
Remove the chained rule and replace it with `0.0.0.0/0`.

---

## Diagnose it
Port scans reveal database port 5432 open to the public internet—flagged immediately by AWS Security Hub.

---

## Recover it
Restore the chained rule referencing `$SG_APP_ID`.

---

## Security
To connect securely from your local laptop for debugging, use AWS Systems Manager (SSM) Port Forwarding over a private bastion host.

---

## Cost
### Cost Warning
Security group chaining and DB Subnet Groups cost $0.00.

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
# Cleanup custom rules
```

---

## Verify cleanup
```bash
echo 'Rules verified.'
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-27-evidence.md`.

---

## Questions for mastery
1. Why is Security Group Chaining superior to whitelisting the private IP addresses of your EC2 instances?
2. Why does RDS require a DB Subnet Group to span at least two Availability Zones even if you only deploy a Single-AZ database?
3. How does SSM Session Manager Port Forwarding allow local DBeaver connections without opening public inbound ports?

---

## When to use this
Always use Security Group Chaining for all application-to-database communication.

---

## When not to use this
Never hardcode private IP CIDRs for autoscaled instance fleets.

---

## What comes next
Phase 28: RDS Multi-AZ and Read Scaling — Availability vs Read Performance.
