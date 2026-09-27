# Phase 50: CloudWatch Logs

## Motto
> Logs scattered across server filesystems are lost on termination. Centralize logs and always set retention.

**Type:** Hands-on Lab & Centralized Logging  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 49: CloudWatch  
**AWS Services Involved:** Amazon CloudWatch Logs, Log Groups, Log Streams, CloudWatch Logs Insights  
**Cost Vector:** Log ingestion: $0.50 per GB. Log storage: $0.03 per GB-month. Setting 7-30 day retention cuts long-term log costs by 95%!  

---

## Problem
When an autoscaled EC2 instance terminates, all local files in `/var/log/` are permanently wiped. If a customer reports a crash from yesterday, the evidence is gone.

---

## Prediction
Shipping logs to a CloudWatch Log Group centralizes application logs, enables serverless JSON querying, and preserves evidence after compute destruction.

---

## Why this matters
Unbounded log retention is a major hidden cloud cost. Default CloudWatch Log Groups have 'Never Expire', accruing storage charges for years.

---

## First principles
CloudWatch Logs hierarchy: (1) **Log Group**: Defines retention, IAM permissions, and metric filters (e.g. `/aws/lambda/orders`). (2) **Log Stream**: A sequence of log events from a single instance/container. (3) **Log Event**: Timestamp + message string.

---

## Mental model
```text
CloudWatch Logs Architecture:
Instance 1 (AZ-A) ──► Log Stream: i-001a ──┐
                                           ├──► [ Log Group: /app/production ]
Instance 2 (AZ-B) ──► Log Stream: i-002b ──┘      ├── Retention: 7 Days (Saves Cost!)
                                                  └── CloudWatch Logs Insights (SQL Queries)
```

---

## Architecture before AWS
Self-hosted ELK (Elasticsearch, Logstash, Kibana) or Rsyslog clusters with daily logrotate.

---

## Build the primitive
```python
import json, time
log_event = {
    "timestamp": int(time.time() * 1000),
    "message": json.dumps({"level": "ERROR", "error": "DatabaseTimeout", "user_id": 881})
}
print("Structured JSON log event:", log_event['message'])
```

---

## Use AWS
```bash
aws logs create-log-group --log-group-name /aws-from-scratch/app && aws logs put-retention-policy --log-group-name /aws-from-scratch/app --retention-in-days 7
```

---

## Inspect it
```bash
aws logs describe-log-groups --log-group-name-prefix /aws-from-scratch --output table
```

---

## Measure it
Execute CloudWatch Logs Insights query: `fields @timestamp, @message | filter level = 'ERROR' | limit 10`.

---

## Break it
Create a log group without setting a retention policy (default: Never Expire).

---

## Diagnose it
Log storage grows monotonically forever; monthly storage fees increase every single month.

---

## Recover it
Run `aws logs put-retention-policy --retention-in-days 14` to automatically expire old logs.

---

## Security
Ensure sensitive data (passwords, credit card numbers, JWTs) is scrubbed before writing to logs.

---

## Cost
### Cost Warning
Log ingestion: $0.50 per GB. Log storage: $0.03 per GB-month. Setting 7-30 day retention cuts long-term log costs by 95%!

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
aws logs delete-log-group --log-group-name /aws-from-scratch/app
```

---

## Verify cleanup
```bash
echo 'Log group deleted.'
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-50-evidence.md`.

---

## Questions for mastery
1. Why is structured JSON logging superior to unstructured plaintext string logging in CloudWatch?
2. What happens to your AWS bill if an application gets stuck in an infinite loop logging 10,000 errors per second?
3. How do Metric Filters turn log patterns (e.g. `[error=Exception]`) into CloudWatch metrics without writing code?

---

## When to use this
Use CloudWatch Logs for application logs, Lambda output, and compliance audit trails.

---

## When not to use this
Do not store high-volume verbose debug logs in CloudWatch permanently—archive to S3 Glacier for cheap long-term cold storage.

---

## What comes next
Phase 51: Metrics and Alarms — Automated alerting when thresholds breach.
