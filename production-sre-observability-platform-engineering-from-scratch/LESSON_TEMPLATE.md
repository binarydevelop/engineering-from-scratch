# Lesson [Number]: [Lesson Title]

> **Motto**: [Short, memorable operational principle embodying the lesson]

---

## Motto
"[Full motto or operational proverb]"

## Production Problem
[Explain the real-world operational failure, scaling cliff, or developer friction that makes this lesson necessary. Describe concrete symptoms: error rates, slow response times, noisy alarms, or deployment blockers.]

## Prediction
[State your operational hypothesis before taking any action. What do you predict will happen to latency, error count, queue depth, or resource saturation when traffic increases or failure is injected?]

## User Impact
[Detail exactly what the human or client experiences when this condition occurs: Did the user see a 504 Gateway Timeout? Did the checkout button hang? Did a payment charge succeed while the order failed?]

## Why This Matters
[Explain why ignoring this leads to production incidents, SLA breaches, developer burnout, high cloud bills, or degraded business outcomes.]

## First Principles
[Break down the fundamental physics/math/protocols: Operating system processes, TCP buffers, Little's Law, queueing theory, CPU throttling mechanics, context propagation headers, or time-series mathematics.]

## Mental Model
```text
[ASCII diagram showing the state transition, request lifecycle, or architectural interaction]
```

## Build the Simple Version
[Provide or walk through the minimal pure standard-library implementation (e.g. Python stdlib) demonstrating the mechanism without third-party frameworks.]

## Instrument It
[Add appropriate telemetry: structured logging with correlation IDs, Prometheus metric counters/gauges/histograms, or OpenTelemetry spans using current stable semantic conventions.]

## Observe It
[Query the signals: inspect the raw JSON log lines, run PromQL queries against Prometheus, or inspect trace timelines in Tempo/Jaeger.]

## Measure It
[Quantify the behavior with specific numbers: p50/p95/p99 latency, RPS, connection count, memory bytes, or error budget burn rate.]

## Break It
[Execute the controlled failure injection or load stress: kill a process, inject network latency, exhaust database connection pools, or send skewed traffic.]

## Detect It
[How is the condition discovered? Was it a symptom-based alert, an SLO burn rate breach, or a user filing a support ticket? Why was detection fast or slow?]

## Debug It
[Trace the causal chain using the signal selection framework: Start from the symptom alert -> inspect the trace waterfall -> isolate the offending span -> inspect the structured error log -> correlate with resource saturation.]

## Mitigate It
[What immediate operational action restores service health before finding the root cause? Roll back, enable circuit breaker, shed traffic, scale workers, or toggle a feature flag?]

## Recover It
[How is permanent stability restored? Schema migration, connection pool sizing, cache warming, or code bugfix.]

## Automate It
[How do we eliminate the human toil of detecting and mitigating this in the future? Automated rollback, self-healing probes, auto-remediation, or canary analysis?]

## Reliability Implication
[What does this teach about fault domains, dependencies, blast radius, error budgets, and cascade prevention?]

## Platform Implication
[How should the internal developer platform encapsulate this? Can we provide a golden path, safe default configuration, or automated guardrail so developers cannot make this mistake?]

## Evidence
```text
Lesson:
Date:
Service version:
Infrastructure:
Prediction:
User symptom:
Relevant SLI:
Load level:
Commands:
Telemetry collected:
Metrics:
Logs:
Trace:
Alert:
Measurements:
What did I intentionally break?
How was it detected?
Was detection user-centered?
How long until diagnosis?
Root/contributing cause:
Mitigation:
Recovery:
What would prevent recurrence?
What should be automated?
Platform opportunity:
Cost implication:
Artifact produced:
Explain the production mechanism in my own words:
Remaining questions:
```

## Questions for Mastery
1. [Deep operational question probing failure modes and tradeoffs]
2. [Question contrasting cause vs symptom]
3. [Question on platform design or architectural prevention]

## When Not to Use This
[Identify edge cases or contexts where this pattern introduces unnecessary complexity or negative tradeoffs.]

## What Comes Next
[Link to the subsequent lesson in the curriculum and preview how this concept builds into larger production architectures.]
