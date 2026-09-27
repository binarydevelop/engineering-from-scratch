# Phase 51: Metrics and Alarms

## Motto
> Metric != Alarm. A metric is raw data. An alarm is a state machine that acts when data violates expectations.

**Type:** Hands-on Lab & Alerting Systems  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 50: CloudWatch Logs  
**AWS Services Involved:** Amazon CloudWatch Alarms  
**Cost Vector:** Standard resolution alarms cost $0.10 per alarm per month. Free tier includes 10 alarms.  

---

## Problem
Engineers discover that production is down only when customers start complaining on social media.

---

## Prediction
A CloudWatch Alarm evaluating an error metric will transition to `ALARM` state when the threshold is breached and immediately notify an SNS topic.

---

## Why this matters
Automated alerting and self-healing are mandatory for high-reliability systems.

---

## First principles
A CloudWatch Alarm is a three-state state machine: `OK`, `ALARM`, and `INSUFFICIENT_DATA`. It evaluates $M$ out of $N$ evaluation periods against a threshold (e.g. ErrorRate > 5% for 3 consecutive 1-minute periods). When state changes, it dispatches an action (SNS alert, EC2 reboot, Auto Scaling policy).

---

## Mental model
```text
CloudWatch Alarm State Machine:
┌──────────────┐
│      OK      │ ◄── Metric values within normal bounds
└──────┬───────┘
       │
       │ Threshold Breached for N consecutive periods!
       ▼
┌──────────────┐
│    ALARM     │ ──► Triggers Action: Publish to SNS topic: "on-call-pager"
└──────┬───────┘
       │
       │ Metric returns below threshold
       ▼
┌──────────────┐
│      OK      │
└──────────────┘
```

---

## Architecture before AWS
Nagios / Zabbix polling daemons sending email alerts via local SMTP.

---

## Build the primitive
```python
# Alarm evaluation logic simulation
def evaluate_alarm(datapoints, threshold, periods_needed):
    breaches = sum(1 for dp in datapoints[-periods_needed:] if dp > threshold)
    return "ALARM" if breaches >= periods_needed else "OK"
print("Alarm State (1 breach out of 3):", evaluate_alarm([10, 80, 20], threshold=50, periods_needed=3))
print("Alarm State (3 breaches out of 3):", evaluate_alarm([60, 70, 80], threshold=50, periods_needed=3))
```

---

## Use AWS
```bash
aws cloudwatch put-metric-alarm --alarm-name lab-error-alarm --metric-name 5XXError --namespace AWS/ApplicationELB --statistic Sum --period 60 --threshold 5 --comparison-operator GreaterThanThreshold --evaluation-periods 1 --tags Key=Project,Value=aws-from-scratch
```

---

## Inspect it
```bash
aws cloudwatch describe-alarms --alarm-names lab-error-alarm --output json
```

---

## Measure it
Measure time to alert: period duration + evaluation evaluation latency (typically 1-2 minutes).

---

## Break it
Manually trigger the alarm state: `aws cloudwatch set-alarm-state --alarm-name lab-error-alarm --state-value ALARM --state-reason 'Testing chaos'`.

---

## Diagnose it
The alarm transitions to ALARM; SNS email notification is dispatched within seconds.

---

## Recover it
Reset alarm state: `aws cloudwatch set-alarm-state --alarm-name lab-error-alarm --state-value OK --state-reason 'Restored'`.

---

## Security
Configure alarms for root account login, unauthorized API calls, and security group modifications.

---

## Cost
### Cost Warning
Standard resolution alarms cost $0.10 per alarm per month. Free tier includes 10 alarms.

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
aws cloudwatch delete-alarms --alarm-names lab-error-alarm
```

---

## Verify cleanup
```bash
echo 'Alarm deleted.'
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-51-evidence.md`.

---

## Questions for mastery
1. Why is 'M out of N' evaluation periods used rather than a single 1-minute spike to avoid flapping alarms?
2. What does the `INSUFFICIENT_DATA` alarm state mean, and how should it be treated?
3. How do Anomaly Detection alarms differ from static threshold alarms?

---

## When to use this
Set alarms on error rates, latency p99, queue dead-letter depth, and billing thresholds.

---

## When not to use this
Do not create 500 uncalibrated alarms that trigger daily false alarms—this causes 'alert fatigue' where real outages are ignored.

---

## What comes next
Phase 52: Distributed Tracing — Tracking request spans across microservices.
