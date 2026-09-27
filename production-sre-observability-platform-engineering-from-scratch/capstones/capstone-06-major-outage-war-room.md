# The Major Outage War Room

> **Part XXII Capstone Challenge**

## Objective
Simulated multi-system SEV-1 incident with incomplete evidence.

## Architecture & Scenario
1. **Design & Implementation**: Build the production components according to strict reliability SLAs.
2. **Failure Injection**: Inject chaos and verify that automatic fallbacks or circuit breakers activate.
3. **Observability Verification**: Verify that OpenTelemetry spans, Prometheus metrics, and Alertmanager routing correctly report the state.
4. **Postmortem & Deliverable**: Produce an operational review and architectural scorecard.
