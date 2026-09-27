# Solution: LAB-20 — DNAT Port Forwarding Mismatch

---

## 1. Failing Layer
**L3 / L4 (NAT)**

## 2. Root Cause Analysis
The failure occurs because:
> **Correct DNAT target port to match application listener.**

When the client initiates communication, the expected protocol interaction fails at the L3 / L4 (NAT) boundary. 

## 3. Diagnostic Trace
Using `iptables -t nat -L`, we observe the definitive proof of failure:
- **Diagnostic Command**:
  ```bash
  iptables -t nat -L
  ```
- **Evidence**:
  The output directly confirms that the target endpoint or route cannot be reached or resolved due to a state mismatch.

## 4. Surgical Remediation
To permanently resolve this issue:
```bash
# Remediation:
Correct DNAT target port to match application listener.
```

## 5. Production Connection
This incident pattern frequently manifests in production environments:
- **Cloud (AWS/GCP)**: Misconfigured Security Groups, missing VPC route table entries, or incorrect NAT gateways.
- **Containers (Docker/Kubernetes)**: Binding services to `127.0.0.1` inside containers, CNI routing table desynchronization, or kube-proxy iptables rules dropping packets.
- **Microservices**: DNS resolver timeouts, ephemeral port exhaustion during connection spikes, or stale client connection pools.
