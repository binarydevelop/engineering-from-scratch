# Lab Evidence Record

Use this template to record empirical proof and observational reasoning for each lesson and laboratory experiment. Do not mark a lesson complete until every section has been empirically validated.

---

### Meta Information
- **Lesson**: 
- **Date**: 
- **Platform** (Native Linux / WSL2 / Linux VM / Docker): 
- **Network Namespace / Lab Topology**: 

---

### Step 1: Hypothesis & Packet Prediction
- **Source Host / Process**: 
- **Destination Host / Process**: 
- **Source IP**: 
- **Destination IP**: 
- **Protocol (L4 / L7)**: 
- **Source Port**: 
- **Destination Port**: 
- **Route Used (from `ip route get <dest>`)**: 
- **Next Hop Gateway**: 
- **Packets Expected (frame types, flags, sequence)**: 

---

### Step 2: Execution & Raw Observation
- **Commands Executed**:
  ```bash
  
  ```
- **Packet Capture Output (`tcpdump` snippet)**:
  ```text
  
  ```
- **Measurements (RTT, Throughput, Loss, Buffer Fill)**:
  ```text
  
  ```
- **What Actually Happened?**: 

---

### Step 3: Failure Injection & Layer Isolation
- **What did I intentionally break?**: 
- **At which layer did it fail? (Physical, Link, Network, Transport, Application)**: 
- **What evidence proved that? (ICMP code, TCP RST, SYN retransmits, DNS RCODE, HTTP status)**: 
- **How did I fix it?**: 

---

### Step 4: First-Principles Reflection
- **Artifact Produced (script, pcap, log, config)**: 
- **Explain the networking concept in my own words**: 
- **How does this matter in production systems? (AWS VPC, Kubernetes CNI, Docker, Databases, Microservices)**: 
- **Remaining questions**: 
