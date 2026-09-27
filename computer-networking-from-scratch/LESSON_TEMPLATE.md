# Lesson Template: <Phase>.<LessonNumber> — <Lesson Title>

> Follow this exact template for every lesson in `phases/`. Every section must be addressed with empirical rigor and deep first-principles reasoning.

---

## Motto
*A one-sentence mechanical truth capturing the core concept of this lesson.*

## Problem
*What concrete communication problem or limitation exists when processes or hosts need to interact? Frame it as a barrier before introducing protocol abstractions.*

## Prediction
*Before running any commands or writing code: What will happen? What exact packets will move across the interface? What headers and flags will be set? What errors will be observed if something fails?*

## Why this matters
*Why can an engineer not afford to treat this as invisible plumbing? How does ignorance of this mechanism lead to outages, security holes, or degraded performance?*

## First principles
*Derive the solution mathematically, physically, or logically from ground truth. Avoid starting with acronyms or standard definitions.*

## Mental model
*Provide an ASCII diagram illustrating the physical or logical relationships, state transitions, or memory/kernel data structures.*

```text
[ SOURCE ] ──(Interface/Header)──► [ NETWORK / HOP ] ──► [ DESTINATION ]
```

## Build / simulate it
*Provide or link to a standalone, executable Python simulation or socket script implementing the primitive from scratch.*

```python
# Minimal scratch implementation demonstrating the primitive
```

## Configure the network
*The explicit Linux namespace or virtual interface setup needed to isolate and reproduce the experiment safely.*

```bash
# Isolated namespace setup commands
```

## Send traffic
*The command or script used to trigger real communication over the virtual network stack.*

```bash
# Traffic generation (curl, nc, ping, python client)
```

## Capture it
*Run `tcpdump` on the relevant interface and inspect the actual wire bytes.*

```bash
# tcpdump capture command and annotated wire output
```

## Measure it
*Quantitative measurements: round-trip time, bandwidth, packet counts, socket buffer fill, or kernel counter increments.*

```bash
# Measurement commands and numerical outputs
```

## Break it
*Intentionally break one specific layer or parameter (e.g. drop ARP, alter MTU, close port, corrupt route, invalidate cert).*

```bash
# Fault injection command
```

## Trace it
*Step through the failure path. At what point does the packet get dropped, rejected, or timed out?*

```bash
# Tracing tools: ip route get, ss, traceroute, tcpdump, dmesg
```

## Debug it
*Formulate a hypothesis, collect proving evidence, and restore functionality systematically.*

## Modify it
*A hands-on challenge: change a parameter (e.g. window size, TTL, subnet mask, keep-alive timeout) and predict/observe the altered behavior.*

## Evidence
*Link to the completed evidence record in `outputs/` capturing the empirical results.*

## Questions for mastery
*Rigorous, reasoning-based questions testing deep causal understanding rather than rote recall.*
1. *Scenario question 1*
2. *Scenario question 2*
3. *Scenario question 3*

## Production connection
*How this exact layer and mechanism manifests in cloud architectures (AWS VPC, Security Groups), container platforms (Docker, Kubernetes CNI), and distributed datastores (PostgreSQL, Redis, Kafka).*

## What comes next
*Preview of the next lesson: what new bottleneck or communication requirement emerges from what we just built?*
