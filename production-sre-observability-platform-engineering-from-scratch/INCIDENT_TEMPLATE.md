Incident: [Short title describing the operational symptom, e.g. "Elevated 500 error rate on Checkout API"]

Severity: [SEV-1 (Critical customer outage) / SEV-2 (Degraded core journey) / SEV-3 (Internal or non-critical feature)]

Start time: [ISO-8601 Timestamp, e.g. 2026-09-25T14:15:00Z]

User impact: [Quantified customer symptom, e.g. "Approximately 35% of checkout requests in US-East are failing with HTTP 500. Users see 'Payment Processing Unavailable'."]

Systems affected: [Services, databases, and dependencies involved, e.g. `api-gateway`, `checkout-service`, `payment-service`, `postgres`]

Incident lead: [Name of Incident Commander / Lead Responder]

Current hypothesis: [Evidence-based hypothesis, e.g. "Recent deployment v1.4.2 to payment-service introduced connection pool exhaustion when calling third-party stripe mock."]

Mitigations attempted:
1. Scaled checkout-service replicas from 3 to 6 (Did not resolve: Database connection bottleneck worsened)
2. Rolled back payment-service to v1.4.1 at 14:32Z (In progress)

Current mitigation: [Active mitigation step being executed to restore customer experience before finding root cause]

Timeline:
- 14:15Z - Prometheus burn-rate alert fired for checkout_slo (14.4x burn).
- 14:18Z - On-call engineer acknowledged page and opened incident channel #inc-checkout-20260925.
- 14:22Z - Triage revealed HTTP 500 errors originating from checkout-service downstream calls to payment-service.
- 14:25Z - Trace inspection revealed 30s timeouts on span `stripe.charge`.
- 14:30Z - Correlated with deployment event of payment-service v1.4.2 at 14:10Z.
- 14:32Z - Incident Commander ordered immediate rollback of payment-service to v1.4.1.
- 14:36Z - Rollback completed. Error rate dropped to 0.02%.
- 14:40Z - Service restored to healthy baseline.

Next update: [Scheduled time for next stakeholder communication, e.g. "Incident mitigated. Postmortem draft scheduled within 48 hours."]

Resolution: [State when customer experience returned to baseline and criteria used to confirm recovery, e.g. "Error rate < 0.05% for 15 consecutive minutes across all regions."]

Follow-up: [Action items: Postmortem meeting scheduled, runbook updated, rollback automation ticket filed]
