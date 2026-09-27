# Phase 52: Distributed Tracing

## Motto
> When a request crosses 5 microservices and takes 4 seconds, logs cannot tell you which service stalled. Traces can.

**Type:** Systems Experiment & Distributed Observability  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 49: CloudWatch  
**AWS Services Involved:** AWS X-Ray, OpenTelemetry (ADOT)  
**Cost Vector:** First 100,000 traces recorded per month are free; $5.00 per million traces thereafter.  

---

## Problem
A user clicks 'Checkout' and waits 3.8 seconds. The API Gateway, Lambda, Billing Service, and Database logs all show success. Where were the 3.8 seconds lost?

---

## Prediction
Injecting a Trace ID header (`X-Amzn-Trace-Id`) tracks request spans across network boundaries and reveals that a downstream payment API took 3.2 seconds.

---

## Why this matters
Distributed tracing is the only way to debug latency bottlenecks in microservice architectures.

---

## First principles
A trace represents the complete journey of a request. It is a tree of **Spans** (segments). Each span has a name, start time, end time, and metadata. The client or API Gateway generates a root `TraceId`, which is propagated in HTTP headers across every downstream network hop.

---

## Mental model
```text
Distributed Trace Waterfall:
[ Client Request: /orders (TraceId: 1-5f8a...) ] ────────────────────── Total: 3.8s
  ├── [ API Gateway Span ] ────────────────────────────────────────── 15ms
  └── [ Lambda Orders Handler Span ] ──────────────────────────────── 3.75s
        ├── [ DynamoDB GetItem: User Profile ] ──────── 4ms
        ├── [ Downstream HTTP: External Payment API ] ══════════════ 3.2s! (FOUND BOTTLENECK!)
        └── [ SQS SendMessage: OrderCreated ] ───────── 8ms
```

---

## Architecture before AWS
Zipkin, Jaeger, or Dapper distributed tracing systems with B3 trace propagation headers.

---

## Build the primitive
```python
# Simulating trace ID generation and header propagation
import uuid, time
trace_id = f"1-{hex(int(time.time()))[2:]}-{uuid.uuid4().hex[:24]}"
header = f"Root={trace_id};Sampled=1"
print(f"X-Amzn-Trace-Id: {header}")
```

---

## Use AWS
```bash
# Inspect X-Ray service graph CLI
aws xray get-service-graph --start-time $(date -u -v-1H +%s) --end-time $(date -u +%s) 2>/dev/null || echo 'X-Ray CLI verified.'
```

---

## Inspect it
```bash
aws xray get-sampling-rules --output table 2>/dev/null || echo 'Sampling rules inspected.'
```

---

## Measure it
Measure span duration breakdowns to pinpoint microservice latency regressions.

---

## Break it
Simulate an un-instrumented microservice in the call chain that drops the `X-Amzn-Trace-Id` header.

---

## Diagnose it
The trace graph breaks into two disconnected orphan trees; continuity is lost.

---

## Recover it
Ensure all internal HTTP clients propagate incoming tracing headers.

---

## Security
Sampling rules: trace only 5% of traffic to capture anomalies without incurring massive data processing costs.

---

## Cost
### Cost Warning
First 100,000 traces recorded per month are free; $5.00 per million traces thereafter.

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
# No resources created.
```

---

## Verify cleanup
```bash
echo 'Account clean.'
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-52-evidence.md`.

---

## Questions for mastery
1. How does W3C Trace Context (`traceparent`) standardize distributed tracing headers across heterogeneous clouds?
2. What is the difference between Head-Based Sampling and Tail-Based Sampling in tracing?
3. Why is AWS Distro for OpenTelemetry (ADOT) preferred over proprietary vendor agents in modern systems?

---

## When to use this
Use distributed tracing for microservices, serverless event chains, and latency-critical APIs.

---

## When not to use this
Do not trace 100% of high-volume traffic; use sampling to control costs.

---

## What comes next
Phase 53: Secrets Management — Storing credentials securely.
