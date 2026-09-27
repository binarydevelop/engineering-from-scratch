# Lesson 69: Cryptography Prerequisites

> **Motto**: Understanding symmetric encryption (AES/ChaCha20), asymmetric key exchange (ECDHE), and digital signatures.

---

## Motto
"Understanding symmetric encryption (AES/ChaCha20), asymmetric key exchange (ECDHE), and digital signatures."

## Problem
Why can asymmetric encryption not be used to encrypt the entire application data stream?

## Prediction
Asymmetric math is computationally expensive; TLS uses asymmetric exchange to establish a shared symmetric session key.

## Why this matters
Ignorance of this mechanism causes engineers to guess blindly when systems fail. Understanding the mechanical interaction at this layer transforms mysterious outages into transparent, debuggable states.

## First principles
Deriving from ground truth: communication requires a sender, a receiver, an encoding scheme, and a physical medium. When processes run on separate machines, the operating system kernel must package state into standardized wire formats governed by mathematical and physical constraints.

## Mental model
```text
Asymmetric ECDHE (Key Exchange) -> Shared Secret -> Symmetric AES-GCM (Bulk Data Encryption)
```

## Build / simulate it
Review the associated implementation or simulation:
```bash
python3 -c 'import hashlib; print(hashlib.sha256(b"hello").hexdigest())'
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
python3 -c 'import hashlib; print(hashlib.sha256(b"hello").hexdigest())'
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
Having understood cryptography prerequisites, we next discover its inherent boundaries and transition to the next layer of abstraction.
