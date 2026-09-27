# Lesson 122: Project: HTTP Server

> **Motto**: Build an HTTP/1.1 web server from scratch directly on top of raw TCP sockets.

---

## Motto
"Build an HTTP/1.1 web server from scratch directly on top of raw TCP sockets."

## Problem
Parse HTTP request lines, headers, CRLF delimiters, status codes, and handle Keep-Alive persistent connections.

## Prediction
The server parses incoming ASCII requests and returns correctly formatted HTTP/1.1 status lines and headers.

## Why this matters
Ignorance of this mechanism causes engineers to guess blindly when systems fail. Understanding the mechanical interaction at this layer transforms mysterious outages into transparent, debuggable states.

## First principles
Deriving from ground truth: communication requires a sender, a receiver, an encoding scheme, and a physical medium. When processes run on separate machines, the operating system kernel must package state into standardized wire formats governed by mathematical and physical constraints.

## Mental model
```text
TCP Stream ──► Parse Request Line ──► Parse Headers ──► Route URI ──► Return Status & Body
```

## Build / simulate it
Review the associated implementation or simulation:
```bash
python3 projects/02-http-server/http_server.py & python3 projects/02-http-server/test_http.py
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
python3 projects/02-http-server/http_server.py & python3 projects/02-http-server/test_http.py
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
Having understood project: http server, we next discover its inherent boundaries and transition to the next layer of abstraction.
