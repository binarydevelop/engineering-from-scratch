# Incident Simulation 01: Deployment Error Spike

## Incident Metadata
* **Severity**: SEV-1
* **Service**: `checkout-service`
* **Trigger**: Deployment of `checkout-service:v1.4.2` at 14:10 UTC

---

## 1. The Pager Alert
At 14:14 UTC, Alertmanager dispatches a critical alarm:
```text
[FIRING] CheckoutSLOCriticalBurnRate1h (checkout-service, tier-1)
Summary: Checkout error budget exhausting rapidly (14.4x burn rate)
Description: 28% of checkout requests are failing with HTTP 500 error.
Runbook: https://runbooks.internal/checkout/error-spike
```

## 2. Incomplete Evidence Presented to Responders
1. **RED Dashboard**:
   - Total RPS remains stable at ~45 RPS.
   - HTTP 500 error rate jumped from 0.01% to 28.4% starting at 14:10 UTC.
   - Latency for successful 200 requests is unaffected (25ms).
2. **Distributed Traces**:
   - Trace waterfalls for failed requests show child span `payment.charge` returning HTTP 500.
3. **Structured Logs**:
   ```json
   {"timestamp": "2026-09-25T14:12:05Z", "level": "ERROR", "service": "payment-service", "message": "AttributeError: 'NoneType' object has no attribute 'token_id'"}
   ```
4. **Recent Changes**:
   - CI/CD log shows `checkout-service:v1.4.2` was deployed 4 minutes prior to the alert.

---

## 3. Triage & Mitigation Protocol
1. **Declare Incident**: Open war room `#inc-20260925-checkout-500` and appoint Incident Commander.
2. **First Rule of Triage**: *What changed?* A release went out at 14:10.
3. **Action**: Do NOT attempt to debug the python code in production. Immediately execute rollback:
   ```bash
   # Mitigation Command
   make rollback SERVICE=checkout-service VERSION=v1.4.1
   ```
4. **Verify Recovery**: Confirm error rate returns below 0.05% within 2 minutes of rollback.
5. **Postmortem**: Author blameless postmortem using `POSTMORTEM_TEMPLATE.md`.
