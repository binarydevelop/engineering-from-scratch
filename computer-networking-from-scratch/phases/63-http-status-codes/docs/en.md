# Lesson 63: HTTP Status Codes

> **Motto**: HTTP status code families convey the semantic outcome of request processing (2xx, 3xx, 4xx, 5xx).

---

## Motto
"HTTP status code families convey the semantic outcome of request processing (2xx, 3xx, 4xx, 5xx)."

## Problem
Why is returning 200 OK with an error message inside JSON an architectural antipattern?

## Prediction
Proxies, load balancers, and monitoring systems rely on status code families (4xx client error, 5xx server fault).

## Why this matters
Ignorance of this mechanism causes engineers to guess blindly when systems fail. Understanding the mechanical interaction at this layer transforms mysterious outages into transparent, debuggable states.

## First principles
Deriving from ground truth: communication requires a sender, a receiver, an encoding scheme, and a physical medium. When processes run on separate machines, the operating system kernel must package state into standardized wire formats governed by mathematical and physical constraints.

## Mental model
```text
1xx Informational | 2xx Success | 3xx Redirect | 4xx Client Error | 5xx Server Error
```

## Build / simulate it
Review the associated implementation or simulation:
```bash
curl -I http://127.0.0.1:8080/nonexistent
```

## Configure the network
Ensure an isolated laboratory environment is active:
```bash
# Verify host or namespace isolation
./scripts/check-environment.sh
```

## Send traffic
Generate real or simulated traffic across the network interface:
```bash
# Execute test command
curl -I http://127.0.0.1:8080/nonexistent
```

## Capture it
Inspect the actual wire frames or socket states:
```bash
sudo tcpdump -i any -nn -c 4 2>/dev/null || ss -tan
```

## Measure it
Quantify performance metrics:
- Latency / Round-Trip Time
- Serialization Delay
- Packet Drop / Retransmission Count

## Break it
Inject an intentional failure to observe divergence from expected behavior:
```bash
# Fault injection example: close listening port, corrupt route, or alter MTU
```

## Trace it
Isolate the failing layer without guessing:
```bash
ip route show
ss -tulpn
```

## Debug it
Formulate your hypothesis, gather proving evidence, and restore configuration to verify recovery.

## Modify it
Challenge: Alter a parameter (e.g. timeout duration, prefix length, buffer size) and predict the resulting behavioral shift before testing.

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What exact state or error proves whether this layer succeeded or failed?
2. What happens to in-flight packets if intermediate network state is lost?
3. How does this mechanism scale when traffic increases by 100x?

## Production connection
How this manifests in cloud architectures (AWS VPC, Security Groups), container platforms (Docker, Kubernetes CNI), and distributed datastores (PostgreSQL, Redis, Kafka).

## What comes next
Having understood http status codes, we next discover its inherent boundaries and transition to the next layer of abstraction.
