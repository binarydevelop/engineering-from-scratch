# Phases 64 – 72: Alerting Discipline & Alertmanager Architecture

> **Motto**: Understand it. Instrument it. Measure it. Break it. Detect it. Debug it. Recover it. Automate it. Improve it. Operate it.

---

## Phase 64: Why Alert?

### Motto
"An alert is an interruption of a human being's life. If an alert does not require immediate human intervention, it is an abuse of human attention."

### Problem
Organizations accumulate alerts over years. Every time an incident occurs, an engineer adds an alert for whatever metric looked weird during the outage. Soon, on-call engineers receive 50 pages a night, wake up exhausted, suffer burnout, and miss real critical outages.

---

## Phase 65: Symptom vs Cause Alerts

### The Diagnostic Lens
* **Cause Alert (Bad)**: `HostCPUAbove80Percent` -> Triggers during a routine batch compression job. Customer experience is unaffected. Result: False alarm.
* **Symptom Alert (Good)**: `CheckoutSLOHighBurnRate` -> Triggers when 5% of user checkout requests are failing. Direct customer harm. Result: High-priority page.

### Rule of Thumb
If the metric does not directly measure customer impairment, data loss, or imminent capacity collapse, it belongs in an email report, a Slack notification, or a dashboard—NOT on a pager.

---

## Phase 66: The Actionability Invariant

### The 4 Requirements for Paging
Every alert that triggers a pager MUST satisfy:
1. **Urgency**: Requires action within 15–30 minutes to prevent user harm.
2. **Impact**: User journey degraded or error budget rapidly burning.
3. **Actionable**: There is a clear operational step the engineer can take right now.
4. **Runbook**: Direct link to a validated operational playbook.

---

## Phase 67: Alertmanager Architecture

```text
[ Prometheus TSDB ]
         │ Evaluates rules every 5s
         ▼
[ Firing Alert ]  ──HTTP POST──►  [ Alertmanager ]
                                        │
                                        ├── 1. Deduplication (Group by Fingerprint)
                                        ├── 2. Grouping (Wait 10s, batch by service)
                                        ├── 3. Inhibition (Suppress downstream symptoms)
                                        ├── 4. Silencing (Check maintenance windows)
                                        └── 5. Routing (Dispatch to PagerDuty or Slack)
```

---

## Phase 68: Alert Grouping

### Scenario
A network switch fails, disconnecting a rack containing 40 Kubernetes pods.
Without grouping, 40 separate alerts dispatch 40 text messages to the on-call phone in 10 seconds.
With Alertmanager grouping:
```yaml
route:
  group_by: ['alertname', 'cluster', 'service']
  group_wait: 10s
  group_interval: 1m
```
Alertmanager waits 10 seconds, collects all 40 pod failure alerts, and sends **a single message**:
`[FIRING: 40] PodCrashLoopBackOff in cluster production-east (checkout-service)`.

---

## Phase 69: Inhibition

### Preventing Cascade Storms
When PostgreSQL crashes:
1. `DatabaseDown` fires.
2. 15 microservices fail with `DatabaseConnectionError`.
3. The API Gateway fails with `CheckoutHighErrorRate`.
4. Responders receive 17 different alarms simultaneously.

With Alertmanager Inhibition:
```yaml
inhibit_rules:
  - source_match:
      alertname: 'DatabaseDown'
    target_match:
      alertname: 'CheckoutHighErrorRate'
    equal: ['environment']
```
As long as `DatabaseDown` is firing, the downstream `CheckoutHighErrorRate` is automatically silenced. The on-call engineer receives exactly ONE page pointing directly to the root cause: the database!

---

## Phase 70: Silences & Maintenance Windows

### Safe Operational Silencing
When performing planned schema migrations:
1. Open Alertmanager UI at `http://localhost:9093/#/silences` or use CLI.
2. Create silence with explicit matchers (`service="checkout-service"`, `severity="warning"`).
3. Set an explicit expiration time (e.g. 1 hour).
4. Provide comment with ticket reference: `JIRA-4812: PostgreSQL 16 partition migration`.

---

## Phase 71: Alert Fatigue & Noise Reduction

### The Weekly On-Call Audit
Every Monday, the SRE team runs a page volume audit:
* How many pages fired last week?
* What percentage required human action?
* Any alert that fired > 3 times without requiring mitigation must either be:
  1. Tuned with a higher threshold or longer `for:` window.
  2. Demoted from Pager to Slack.
  3. Deleted permanently.

---

## Phase 72: Runbooks as Code

### Mandatory Runbook Structure
Every alert annotation links to a Markdown runbook in the repository containing:
1. **Symptom**: Exactly what customer experience is degraded.
2. **Blast Radius**: How many users or regions are affected.
3. **First 3 Triage Commands**: Exact shell commands to check logs, pods, and metrics.
4. **Mitigation**: One-command rollback or failover procedure.
5. **Escalation**: Secondary rotation contact if primary responder is blocked.
