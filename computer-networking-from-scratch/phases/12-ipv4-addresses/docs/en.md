# Lesson 12: IPv4 Addresses

> **Motto**: An IPv4 address is an unsigned 32-bit integer formatted as four dotted-decimal octets for human readability.

---

## Motto
"An IPv4 address is an unsigned 32-bit integer formatted as four dotted-decimal octets for human readability."

## Problem
How do we provide globally routable, hierarchical addresses to billions of interconnected hosts?

## Prediction
32 bits allow up to 4.29 billion distinct addresses divided hierarchically into network and host portions.

## Why this matters
Ignorance of this mechanism causes engineers to guess blindly when systems fail. Understanding the mechanical interaction at this layer transforms mysterious outages into transparent, debuggable states.

## First principles
Deriving from ground truth: communication requires a sender, a receiver, an encoding scheme, and a physical medium. When processes run on separate machines, the operating system kernel must package state into standardized wire formats governed by mathematical and physical constraints.

## Mental model
```text
192.168.1.10 <-> 11000000.10101000.00000001.00001010
```

## Build / simulate it
Review the associated implementation or simulation:
```bash
python3 -c 'import socket, struct; print(bin(struct.unpack("!I", socket.inet_aton("192.168.1.10"))[0]))'
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
python3 -c 'import socket, struct; print(bin(struct.unpack("!I", socket.inet_aton("192.168.1.10"))[0]))'
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
Having understood ipv4 addresses, we next discover its inherent boundaries and transition to the next layer of abstraction.
