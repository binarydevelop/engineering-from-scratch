# Lesson 115: Firewall Failure Lab

> **Motto**: Diagnose silent packet drops versus administrative TCP RST rejections using iptables.

---

## Motto
"Diagnose silent packet drops versus administrative TCP RST rejections using iptables."

## Problem
Differentiate an iptables -j DROP rule (silent timeout) from an iptables -j REJECT rule (immediate reset).

## Prediction
iptables -L -n -v shows packet drop counters incrementing in real time.

## Why this matters
Ignorance of this mechanism causes engineers to guess blindly when systems fail. Understanding the mechanical interaction at this layer transforms mysterious outages into transparent, debuggable states.

## First principles
Deriving from ground truth: communication requires a sender, a receiver, an encoding scheme, and a physical medium. When processes run on separate machines, the operating system kernel must package state into standardized wire formats governed by mathematical and physical constraints.

## Mental model
```text
iptables -L -n -v -> Observe drop counter incrementing on target port -> Add ACCEPT rule
```

## Build / simulate it
Review the associated implementation or simulation:
```bash
cd broken-networks/lab-08-firewall-drops-inbound-syn && cat README.md
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
cd broken-networks/lab-08-firewall-drops-inbound-syn && cat README.md
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
Having understood firewall failure lab, we next discover its inherent boundaries and transition to the next layer of abstraction.
