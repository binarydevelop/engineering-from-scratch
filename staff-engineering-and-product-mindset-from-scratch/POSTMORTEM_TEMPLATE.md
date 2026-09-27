# Blameless Postmortem Template

A postmortem is an organizational learning artifact, not a performance management tool. Its purpose is to understand the systemic conditions, organizational pressures, and technical designs that allowed an incident to occur and spread, and to introduce durable defenses that prevent recurrence.

---

# Incident Postmortem: [Incident Title / Severity Level]

* **Date of Incident:** YYYY-MM-DD
* **Incident Lead / Commander:** [Name]
* **Scribe / Communications Lead:** [Name]
* **Primary Technical Investigators:** [Names]
* **Postmortem Owner:** [Staff Engineer]
* **Severity Level:** SEV-1 / SEV-2
* **Total Incident Duration:** [Hours : Minutes]
* **Time to Detection (TTD):** [Minutes]
* **Time to Mitigation (TTM):** [Minutes]

---

## 1. Executive Summary
A 3-sentence summary of what happened, what users and business operations were impacted, how the system was stabilized, and the core systemic repair agreed upon.

## 2. Customer & Business Impact
* **Users Affected:** Number of active users experiencing degraded service or total failure.
* **Transaction Impact:** Number of dropped transactions, failed checkouts, or lost requests.
* **Financial & SLA Impact:** Direct revenue loss, SLA breach penalty liabilities, or customer support ticket spikes.

## 3. Incident Timeline (All times in UTC)
Chronological record of events from trigger to detection, triage, mitigation, and resolution:
* **HH:MM** - Change deployed (PR #1234 merged to production).
* **HH:MM** - Latency begins increasing on `/checkout` endpoint.
* **HH:MM** - Automated alert fires: `CheckoutErrorRateExceeded`.
* **HH:MM** - Incident declared; war room opened; Incident Commander assigned.
* **HH:MM** - Rollback initiated.
* **HH:MM** - Service restored; error rates return to baseline.

## 4. Detection & Observability
* How was the incident detected? (Automated threshold alert, customer support escalation, executive notification).
* If automated alerting was delayed or absent, why did our telemetry fail to catch the degradation early?

## 5. Technical Root Cause
The immediate physical mechanism of failure:
* Specific query, thread pool starvation, deadlock, memory leak, or invalid configuration that triggered the failure.

## 6. Contributing Conditions & Systemic Factors
Moving beyond simplistic "human error" to investigate the systemic conditions that made the error possible:
* Why was the bad change not caught in pre-merge tests or staging?
* What architectural coupling allowed a local error in Service A to cascade and take down Service B?
* What schedule, deadline, or organizational pressures influenced the deployment decision?
* Why was rollback slow or complex?

## 7. What Went Well
* Did automated health checks isolate traffic?
* Did on-call engineers communicate effectively and follow runbooks?
* Was stakeholder communication timely and clear?

## 8. Where We Got Lucky
* What circumstances prevented the incident from being significantly worse?

## 9. Corrective Actions (Preventing Recurrence)
Avoid vague action items like "be more careful" or "write more documentation." Focus on systemic architectural and process defenses:
| Action Item | Category (Prevent / Detect / Mitigate) | Priority (P0 / P1 / P2) | Single Accountable Owner | Target Due Date |
| :--- | :--- | :--- | :--- | :--- |
| Implement automated canary deployment rollback | Mitigate | P0 | [Name] | YYYY-MM-DD |
| Add circuit breaker to downstream recommendation API | Prevent | P0 | [Name] | YYYY-MM-DD |
| Add p99 latency SLO alert for checkout path | Detect | P1 | [Name] | YYYY-MM-DD |
