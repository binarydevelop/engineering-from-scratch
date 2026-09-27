# Lesson 08: Ethernet From First Principles

> **Motto**: Ethernet solves the local multi-access medium problem by framing bits with source/destination MAC addresses and error checks.

---

## Motto
"Ethernet solves the local multi-access medium problem by framing bits with source/destination MAC addresses and error checks."

## Problem
When multiple devices share an electrical wire or switch, how does a NIC know which frames are meant for it?

## Prediction
The NIC checks the destination MAC address; if it matches its burned-in address or broadcast, it raises an interrupt.

## Why this matters
Ignorance of this mechanism causes engineers to guess blindly when systems fail. Understanding the mechanical interaction at this layer transforms mysterious outages into transparent, debuggable states.

## First principles
Deriving from ground truth: communication requires a sender, a receiver, an encoding scheme, and a physical medium. When processes run on separate machines, the operating system kernel must package state into standardized wire formats governed by mathematical and physical constraints.

## Mental model
```text
[ Preamble | Dst MAC | Src MAC | EtherType | Payload | FCS ]
```

## Build / simulate it
Review the associated implementation or simulation:
```bash
tcpdump -i eth0 -e -nn
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
tcpdump -i eth0 -e -nn
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
Having understood ethernet from first principles, we next discover its inherent boundaries and transition to the next layer of abstraction.
