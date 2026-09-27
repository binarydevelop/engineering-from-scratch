# Service Level Objective (SLO) Document

# Service
[Service name, e.g. `checkout-service`]

## User Journey
[Describe the real user journey from the user's perspective, e.g. "A registered customer submits payment details to complete an order and expects immediate confirmation."]

## SLI
[Specify the Service Level Indicator in clear mathematical terms, e.g. "Ratio of successful checkout HTTP POST requests (HTTP response < 500) with latency under 500ms to total valid checkout attempts."]

## Good Event
[Define precisely what constitutes a successful event, e.g. `http.response.status_code < 500 AND duration_seconds <= 0.500`]

## Total Event
[Define the denominator, including what requests are eligible, e.g. `http.request.method == 'POST' AND http.route == '/api/v1/orders' AND http.response.status_code != 400 AND http.response.status_code != 401 AND http.response.status_code != 422`]

## Measurement Source
[Prometheus metric query, OTel span count, or server access logs, e.g. `sum(rate(http_requests_total{service="checkout",route="/api/v1/orders",status!~"5..|429"}[5m])) / sum(rate(http_requests_total{service="checkout",route="/api/v1/orders"}[5m]))`]

## Target
[The target percentage, e.g. `99.9%` (three nines)]

## Window
[The compliance measurement time period, e.g. `Rolling 30 days` or `Rolling 7 days`]

## Exclusions
[Explicit edge cases excluded from the SLI calculation, e.g. "Malformed client requests (HTTP 400 Bad Request, 401 Unauthorized), scheduled DR exercises announced 7 days prior, synthetic health probes from orchestrators."]

## Error Budget
[The allowable unreliability over the rolling window, e.g. `100% - 99.9% = 0.1% allowed failures`. For 10,000,000 monthly requests, error budget is 10,000 failed or slow requests.]

## Alert Strategy
[Multi-window multi-burn-rate alerting rules:
- 14.4x burn rate (2% budget consumed in 1 hour) -> Page on-call immediately
- 6x burn rate (5% budget consumed in 6 hours) -> Page on-call
- 1x burn rate (10% budget consumed in 3 days) -> Ticket to owning team next business day]

## Ownership
[Team name, Slack/Teams channel, tech lead, on-call roster link]

## Review Cadence
[Bi-weekly or monthly review of error budget consumption, recurring outage patterns, and balance of feature velocity vs reliability work.]

## Why This SLO Matters
[Direct business and customer impact: A broken checkout means immediate lost revenue, customer distrust, and credit card processing anomalies.]

## What This SLO Does NOT Measure
[Explicitly acknowledge blind spots: E.g., This SLO does not measure whether the notification email was sent 5 minutes later, whether third-party fraud scoring delayed checkout by 100ms, or whether the user's local browser network dropped.]
