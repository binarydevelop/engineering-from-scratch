# Solution: LAB-09 — Firewall Drops SYN-ACK

---

## 1. Failing Layer
**L4 (Packet Filter)**

## 2. Root Cause Analysis
The failure occurs because:
> **Ensure stateful return rule exists: ctstate ESTABLISHED,RELATED ACCEPT.**

When the client initiates communication, the expected protocol interaction fails at the L4 (Packet Filter) boundary. 

## 3. Diagnostic Trace
Using `tcpdump on both sides`, we observe the definitive proof of failure:
- **Diagnostic Command**:
  ```bash
  tcpdump on both sides
  ```
- **Evidence**:
  The output directly confirms that the target endpoint or route cannot be reached or resolved due to a state mismatch.

## 4. Surgical Remediation
To permanently resolve this issue:
```bash
# Remediation:
Ensure stateful return rule exists: ctstate ESTABLISHED,RELATED ACCEPT.
```

## 5. Production Connection
This incident pattern frequently manifests in production environments:
- **Cloud (AWS/GCP)**: Misconfigured Security Groups, missing VPC route table entries, or incorrect NAT gateways.
- **Containers (Docker/Kubernetes)**: Binding services to `127.0.0.1` inside containers, CNI routing table desynchronization, or kube-proxy iptables rules dropping packets.
- **Microservices**: DNS resolver timeouts, ephemeral port exhaustion during connection spikes, or stale client connection pools.
