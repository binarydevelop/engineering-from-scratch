# Lesson 90: Keepalive at Different Layers

> **Motto**: Differentiating HTTP Keep-Alive, TCP Keepalive probes, and application-level heartbeats.

---

## Motto
"Differentiating HTTP Keep-Alive, TCP Keepalive probes, and application-level heartbeats."

## Problem
Why does enabling TCP keepalive not keep an idle HTTP/1.1 persistent connection from closing?

## Prediction
HTTP Keep-Alive governs application idle reuse; TCP SO_KEEPALIVE detects dead sockets; heartbeats check process health.

## Why this matters
Ignorance of this mechanism causes engineers to guess blindly when systems fail. Understanding the mechanical interaction at this layer transforms mysterious outages into transparent, debuggable states.

## First principles
Deriving from ground truth: communication requires a sender, a receiver, an encoding scheme, and a physical medium. When processes run on separate machines, the operating system kernel must package state into standardized wire formats governed by mathematical and physical constraints.

## Mental model
```text
L7: Connection: keep-alive | L4: SO_KEEPALIVE (ACK probes) | App: Ping/Pong Heartbeats
```

## Build / simulate it
Review the associated implementation or simulation:
```bash
cat docs/mental-models.md
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
cat docs/mental-models.md
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
Having understood keepalive at different layers, we next discover its inherent boundaries and transition to the next layer of abstraction.
