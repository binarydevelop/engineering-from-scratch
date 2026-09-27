# Solution: LAB-14 — TIME_WAIT Socket Buildup

---

## 1. Failing Layer
**L4 (TCP State Machine)**

## 2. Root Cause Analysis
The failure occurs because:
> **Enable HTTP Keep-Alive / connection pooling instead of closing per request.**

When the client initiates communication, the expected protocol interaction fails at the L4 (TCP State Machine) boundary. 

## 3. Diagnostic Trace
Using `ss -tan state time-wait`, we observe the definitive proof of failure:
- **Diagnostic Command**:
  ```bash
  ss -tan state time-wait
  ```
- **Evidence**:
  The output directly confirms that the target endpoint or route cannot be reached or resolved due to a state mismatch.

## 4. Surgical Remediation
To permanently resolve this issue:
```bash
# Remediation:
Enable HTTP Keep-Alive / connection pooling instead of closing per request.
```

## 5. Production Connection
This incident pattern frequently manifests in production environments:
- **Cloud (AWS/GCP)**: Misconfigured Security Groups, missing VPC route table entries, or incorrect NAT gateways.
- **Containers (Docker/Kubernetes)**: Binding services to `127.0.0.1` inside containers, CNI routing table desynchronization, or kube-proxy iptables rules dropping packets.
- **Microservices**: DNS resolver timeouts, ephemeral port exhaustion during connection spikes, or stale client connection pools.
