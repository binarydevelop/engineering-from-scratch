# Lesson 15: Same Subnet or Different Subnet?

> **Motto**: The fundamental routing decision: if destination IP shares the local subnet prefix, deliver directly via ARP; otherwise, send to default gateway.

---

## Motto
"The fundamental routing decision: if destination IP shares the local subnet prefix, deliver directly via ARP; otherwise, send to default gateway."

## Problem
How does a host decide whether to broadcast an ARP request for the destination or for the router?

## Prediction
The host applies its subnet mask to both local and destination IPs; mismatch triggers gateway forwarding.

## Why this matters
Ignorance of this mechanism causes engineers to guess blindly when systems fail. Understanding the mechanical interaction at this layer transforms mysterious outages into transparent, debuggable states.

## First principles
Deriving from ground truth: communication requires a sender, a receiver, an encoding scheme, and a physical medium. When processes run on separate machines, the operating system kernel must package state into standardized wire formats governed by mathematical and physical constraints.

## Mental model
```text
Dest in local subnet? YES -> ARP for Dest MAC | NO -> ARP for Gateway MAC
```

## Build / simulate it
Review the associated implementation or simulation:
```bash
ip route get 10.0.1.50 && ip route get 8.8.8.8
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
ip route get 10.0.1.50 && ip route get 8.8.8.8
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
Having understood same subnet or different subnet?, we next discover its inherent boundaries and transition to the next layer of abstraction.
