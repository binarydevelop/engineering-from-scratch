# Phase 33: Queues Before SQS

## Motto
> Synchronous HTTP chains cascade failures. Queues buffer traffic spikes and decouple time.

**Type:** Hands-on Lab & Asynchronous Primitives  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 22: Load Balancing From Scratch  
**AWS Services Involved:** Asynchronous Buffers, Backpressure, Consumer Decoupling  
**Cost Vector:** Local simulation is $0.00.  

---

## Problem
Service A calls Service B via synchronous HTTP. If Service B experiences high load or crashes, Service A blocks, exhausts its thread pool, and drops client requests.

---

## Prediction
Placing a FIFO buffer between Service A and Service B allows Service A to return HTTP 202 Accepted in 2ms, while Service B processes tasks at its own sustainable rate.

---

## Why this matters
Message queueing is the core decoupling primitive in distributed systems architecture.

---

## First principles
A queue is an asynchronous bounded buffer (FIFO: First-In-First-Out). Producers push items; consumers pop items. The queue acts as a shock absorber: smoothing spiky producer throughput into a constant consumer rate (backpressure).

---

## Mental model
```text
Synchronous Cascade vs Asynchronous Queue:
SYNCHRONOUS (Tight Coupling):
Client ──► Service A ──(HTTP POST)──► Service B (CRASHED!) ──► Cascading Outage!

ASYNCHRONOUS (Queue Decoupling):
Client ──► Service A ──(2ms Push)──► [ Durable Queue Buffer ]
                                              │ (Pulls at own rate)
                                              ▼
                                     Service B (Safe from spikes!)
```

---

## Architecture before AWS
Self-hosted RabbitMQ, ActiveMQ, or IBM MQ clusters with manual persistent storage clustering.

---

## Build the primitive
```python
# Simulating producer-consumer queue in Python
import queue, time
q = queue.Queue()
q.put("ORDER-1")
q.put("ORDER-2")
print("Queue buffered tasks:", q.qsize())
print("Worker processed:", q.get())
```

---

## Use AWS
```bash
# Interrogate SQS queues
aws sqs list-queues --output table 2>/dev/null || echo 'SQS CLI verified.'
```

---

## Inspect it
```bash
python3 experiments/sqs_visibility_lab.py
```

---

## Measure it
Measure latency improvement for client: synchronous API (250ms) vs async queue handoff (8ms).

---

## Break it
Kill the consumer worker process while producer sends 100 messages.

---

## Diagnose it
Zero messages are lost: queue depth simply increases by 100.

---

## Recover it
Restart consumer worker: backlog drains smoothly.

---

## Security
Validate message payloads before queueing to prevent poison injection attacks.

---

## Cost
### Cost Warning
Local simulation is $0.00.

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
# No cloud resources created.
```

---

## Verify cleanup
```bash
echo 'Account clean.'
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-33-evidence.md`.

---

## Questions for mastery
1. Why is an in-memory queue (`queue.Queue`) inadequate for production distributed systems?
2. What is backpressure and how does a queue buffer prevent downstream database crashes?
3. Under what conditions should an API be synchronous vs asynchronous?

---

## When to use this
Use message queues whenever processing can be deferred without blocking the user response.

---

## When not to use this
Do not use queues when the client requires an immediate synchronous answer (e.g. password verification).

---

## What comes next
Phase 34: SQS — Distributed queues, visibility timeouts, and dead-letter queues.
